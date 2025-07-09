#!/usr/bin/env python3
"""
Web-based User Interface for Yelp Business Mailing List Generator

This Flask application provides a web interface for users to generate
business mailing lists without needing to install Python or run commands.
"""

from flask import Flask, render_template, request, send_file, jsonify, flash
import os
import tempfile
import json
from datetime import datetime
from main import MailingListGenerator
from yelp_api_client import YelpAPIClient
from excel_generator import ExcelGenerator

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-change-this')

# Load Yelp categories for the dropdown
def load_categories():
    try:
        with open('yelp_categories.json', 'r') as f:
            categories = json.load(f)
        return categories
    except Exception as e:
        print(f"Error loading categories: {e}")
        return []

@app.route('/')
def index():
    """Main page with the form."""
    categories = load_categories()
    return render_template('index.html', categories=categories)

@app.route('/generate', methods=['POST'])
def generate_mailing_list():
    """Handle form submission and generate the mailing list."""
    try:
        # Get form data
        location = request.form.get('location', '').strip()
        business_type = request.form.get('business_type', '').strip()
        radius_miles = request.form.get('radius', '25').strip()
        max_results = request.form.get('max_results', '100').strip()
        filename = request.form.get('filename', '').strip()
        
        # Validate required fields
        if not location:
            return jsonify({'error': 'Location is required'}), 400
        
        # Validate and convert radius
        try:
            radius_miles = int(radius_miles)
            if radius_miles <= 0 or radius_miles > 25:
                return jsonify({'error': 'Radius must be between 1 and 25 miles'}), 400
            radius_meters = radius_miles * 1609
        except ValueError:
            return jsonify({'error': 'Invalid radius value'}), 400
        
        # Validate max results
        try:
            max_results = int(max_results)
            if max_results <= 0 or max_results > 1000:
                return jsonify({'error': 'Max results must be between 1 and 1000'}), 400
        except ValueError:
            return jsonify({'error': 'Invalid max results value'}), 400
        
        # Generate filename if not provided
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"business_mailing_list_{timestamp}.xlsx"
        elif not filename.endswith('.xlsx'):
            filename += '.xlsx'
        
        # Initialize the mailing list generator
        generator = MailingListGenerator()
        
        # Search for businesses
        businesses = generator.yelp_client.search_businesses(
            location=location,
            business_type=business_type if business_type else None,
            radius=radius_meters,
            max_results=max_results
        )
        
        if not businesses:
            return jsonify({'error': 'No businesses found matching your criteria'}), 404
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp_file:
            temp_path = tmp_file.name
        
        # Export to Excel
        generator.excel_generator.export_to_excel(
            businesses=businesses,
            filename=temp_path
        )
        
        # Create summary sheet
        generator.excel_generator.create_summary_sheet(businesses, temp_path)
        
        # Return success response with file info
        return jsonify({
            'success': True,
            'message': f'Found {len(businesses)} businesses',
            'filename': filename,
            'file_path': temp_path,
            'business_count': len(businesses)
        })
        
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

@app.route('/download/<path:file_path>')
def download_file(file_path):
    """Download the generated Excel file."""
    try:
        # Security check - ensure file is in temp directory
        if not file_path.startswith('/tmp/') and not file_path.startswith(tempfile.gettempdir()):
            return jsonify({'error': 'Invalid file path'}), 400
        
        if not os.path.exists(file_path):
            return jsonify({'error': 'File not found'}), 404
        
        # Get filename from path
        filename = os.path.basename(file_path)
        
        # Send file and then delete it
        response = send_file(
            file_path,
            as_attachment=True,
            download_name=filename,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        
        # Schedule file deletion after response is sent
        @response.call_on_close
        def cleanup():
            try:
                if os.path.exists(file_path):
                    os.unlink(file_path)
            except:
                pass
        
        return response
        
    except Exception as e:
        return jsonify({'error': f'Download error: {str(e)}'}), 500

@app.route('/categories')
def get_categories():
    """API endpoint to get available categories."""
    categories = load_categories()
    return jsonify(categories)

@app.route('/health')
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    
    # Get port from environment variable (for cloud deployment)
    port = int(os.environ.get('PORT', 8080))
    
    # Run the Flask app
    app.run(debug=False, host='0.0.0.0', port=port) 