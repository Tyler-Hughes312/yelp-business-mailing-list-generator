import pandas as pd
from typing import List, Dict, Optional
from datetime import datetime
import os
from config import EXCEL_COLUMNS

class ExcelGenerator:
    def __init__(self):
        """Initialize Excel generator."""
        pass
    
    def format_business_data(self, businesses: List[Dict]) -> List[Dict]:
        """
        Format business data for Excel export.
        
        Args:
            businesses: List of business dictionaries from Yelp API
            
        Returns:
            List of formatted business dictionaries
        """
        formatted_data = []
        
        for business in businesses:
            # Extract location information
            location = business.get('location', {})
            address = location.get('address1', '')
            city = location.get('city', '')
            state = location.get('state', '')
            zip_code = location.get('zip_code', '')
            
            # Combine address components
            full_address = f"{address}, {city}, {state} {zip_code}".strip()
            if full_address.startswith(', '):
                full_address = full_address[2:]
            
            # Extract categories
            categories = business.get('categories', [])
            business_type = ', '.join([cat.get('title', '') for cat in categories]) if categories else ''
            
            # Format phone number
            phone = business.get('phone', '')
            if phone:
                # Remove any non-digit characters except + for international numbers
                phone = ''.join(c for c in phone if c.isdigit() or c == '+')
            
            # Format price level
            price_level = business.get('price', '')
            if price_level:
                price_level = '$' * len(price_level)
            
            formatted_business = {
                'Business Name': business.get('name', ''),
                'Address': full_address,
                'City': city,
                'State': state,
                'ZIP Code': zip_code,
                'Phone': phone,
                'Website': business.get('url', ''),
                'Business Type': business_type,
                'Rating': business.get('rating', ''),
                'Review Count': business.get('review_count', ''),
                'Price Level': price_level,
                'Yelp URL': business.get('url', '')
            }
            
            formatted_data.append(formatted_business)
        
        return formatted_data
    
    def export_to_excel(self, 
                       businesses: List[Dict], 
                       filename: Optional[str] = None,
                       sheet_name: str = 'Business Mailing List') -> str:
        """
        Export business data to Excel file.
        
        Args:
            businesses: List of business dictionaries
            filename: Output filename (optional)
            sheet_name: Excel sheet name
            
        Returns:
            Path to the created Excel file
        """
        if not businesses:
            print("No businesses to export.")
            return ""
        
        # Format the data
        formatted_data = self.format_business_data(businesses)
        
        # Create DataFrame
        df = pd.DataFrame(formatted_data)
        
        # Reorder columns to match EXCEL_COLUMNS
        df = df[EXCEL_COLUMNS]
        
        # Generate filename if not provided
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"business_mailing_list_{timestamp}.xlsx"
        
        # Ensure .xlsx extension
        if not filename.endswith('.xlsx'):
            filename += '.xlsx'
        
        # Create output directory if it doesn't exist
        output_dir = 'output'
        os.makedirs(output_dir, exist_ok=True)
        
        filepath = os.path.join(output_dir, filename)
        
        # Export to Excel
        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name=sheet_name, index=False)
            
            # Get the workbook and worksheet
            workbook = writer.book
            worksheet = writer.sheets[sheet_name]
            
            # Auto-adjust column widths
            for column in worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter
                
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                
                adjusted_width = min(max_length + 2, 50)  # Cap at 50 characters
                worksheet.column_dimensions[column_letter].width = adjusted_width
        
        print(f"Excel file created: {filepath}")
        print(f"Total businesses exported: {len(formatted_data)}")
        
        return filepath
    
    def create_summary_sheet(self, 
                           businesses: List[Dict], 
                           filepath: str,
                           summary_sheet_name: str = 'Summary') -> None:
        """
        Create a summary sheet with statistics.
        
        Args:
            businesses: List of business dictionaries
            filepath: Path to the Excel file
            summary_sheet_name: Name for the summary sheet
        """
        if not businesses:
            return
        
        # Calculate statistics
        total_businesses = len(businesses)
        
        # Count by business type
        business_types = {}
        for business in businesses:
            categories = business.get('categories', [])
            for category in categories:
                cat_title = category.get('title', '')
                business_types[cat_title] = business_types.get(cat_title, 0) + 1
        
        # Count by city
        cities = {}
        for business in businesses:
            location = business.get('location', {})
            city = location.get('city', 'Unknown')
            cities[city] = cities.get(city, 0) + 1
        
        # Create summary data
        summary_data = {
            'Metric': [
                'Total Businesses',
                'Average Rating',
                'Businesses with Phone',
                'Businesses with Website',
                'Top Business Type',
                'Top City'
            ],
            'Value': [
                total_businesses,
                f"{sum(b.get('rating', 0) for b in businesses) / total_businesses:.1f}",
                sum(1 for b in businesses if b.get('phone')),
                sum(1 for b in businesses if b.get('url')),
                max(business_types.items(), key=lambda x: x[1])[0] if business_types else 'N/A',
                max(cities.items(), key=lambda x: x[1])[0] if cities else 'N/A'
            ]
        }
        
        # Add to existing Excel file
        with pd.ExcelWriter(filepath, engine='openpyxl', mode='a') as writer:
            summary_df = pd.DataFrame(summary_data)
            summary_df.to_excel(writer, sheet_name=summary_sheet_name, index=False) 