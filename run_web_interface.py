#!/usr/bin/env python3
"""
Web Interface Runner for Yelp Business Mailing List Generator

This script sets up and runs the web interface for the mailing list generator.
"""

import os
import sys
import subprocess
import webbrowser
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        import flask
        print("✅ Flask is installed")
    except ImportError:
        print("❌ Flask is not installed. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "flask>=2.3.0"])
        print("✅ Flask installed successfully")

def check_env_file():
    """Check if .env file exists with API key."""
    if not os.path.exists('.env'):
        print("❌ .env file not found!")
        print("Please create a .env file with your Yelp API key:")
        print("YELP_API_KEY=your_api_key_here")
        return False
    
    # Check if API key is in .env file
    with open('.env', 'r') as f:
        content = f.read()
        if 'YELP_API_KEY=' not in content:
            print("❌ YELP_API_KEY not found in .env file!")
            print("Please add your Yelp API key to the .env file:")
            print("YELP_API_KEY=your_api_key_here")
            return False
    
    print("✅ .env file found with API key")
    return True

def check_categories_file():
    """Check if yelp_categories.json exists."""
    if not os.path.exists('yelp_categories.json'):
        print("❌ yelp_categories.json not found!")
        print("This file is required for the web interface.")
        return False
    
    print("✅ yelp_categories.json found")
    return True

def main():
    """Main function to run the web interface."""
    print("🚀 Yelp Business Mailing List Generator - Web Interface")
    print("=" * 60)
    
    # Check dependencies
    check_dependencies()
    
    # Check required files
    if not check_env_file():
        return
    
    if not check_categories_file():
        return
    
    # Create templates directory if it doesn't exist
    templates_dir = Path('templates')
    templates_dir.mkdir(exist_ok=True)
    
    print("\n✅ All checks passed!")
    print("\n🌐 Starting web interface...")
    print("   The interface will be available at: http://localhost:8080")
    print("   Press Ctrl+C to stop the server")
    print("-" * 60)
    
    try:
        # Import and run the Flask app
        from app import app
        
        # Open browser automatically
        webbrowser.open('http://localhost:8080')
        
        # Run the Flask app
        app.run(debug=False, host='0.0.0.0', port=8080)
        
    except KeyboardInterrupt:
        print("\n👋 Web interface stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting web interface: {e}")
        print("Please check your setup and try again")

if __name__ == "__main__":
    main() 