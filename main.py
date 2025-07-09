#!/usr/bin/env python3
"""
Yelp Business Mailing List Generator

This application uses the Yelp Fusion API to search for businesses
and generate mailing lists in Excel format.
"""

import sys
import os
import json
from typing import Optional
from yelp_api_client import YelpAPIClient
from excel_generator import ExcelGenerator
from config import BUSINESS_CATEGORIES
from difflib import get_close_matches

# Load all Yelp categories from JSON
CATEGORIES_FILE = 'yelp_categories.json'
def load_all_categories():
    try:
        with open(CATEGORIES_FILE, 'r') as f:
            categories = json.load(f)
        return categories
    except Exception as e:
        print(f"❌ Error loading categories: {e}")
        return []

ALL_YELP_CATEGORIES = load_all_categories()
CATEGORY_ALIASES = {cat['alias']: cat for cat in ALL_YELP_CATEGORIES}
CATEGORY_TITLES = {cat['title'].lower(): cat for cat in ALL_YELP_CATEGORIES}

class MailingListGenerator:
    def __init__(self):
        """Initialize the mailing list generator."""
        try:
            self.yelp_client = YelpAPIClient()
            self.excel_generator = ExcelGenerator()
            print("✅ Yelp API client initialized successfully")
        except ValueError as e:
            print(f"❌ Error: {e}")
            print("Please make sure your YELP_API_KEY is set in the .env file")
            sys.exit(1)
    
    def display_categories(self, limit=50):
        """Display a sample of available Yelp business categories."""
        print("\n📋 Sample of Yelp Business Categories (showing first {}):".format(limit))
        print("-" * 50)
        for i, cat in enumerate(ALL_YELP_CATEGORIES[:limit]):
            print(f"  {cat['title']} (alias: {cat['alias']})")
        print(f"...and {len(ALL_YELP_CATEGORIES) - limit} more. Type your business type or alias!")
        print("-" * 50)
    
    def match_category(self, user_input: str) -> Optional[str]:
        """Match user input to the closest Yelp category alias."""
        user_input = user_input.strip().lower()
        if not user_input:
            return None
        # Direct alias match
        if user_input in CATEGORY_ALIASES:
            return user_input
        # Direct title match
        if user_input in CATEGORY_TITLES:
            return CATEGORY_TITLES[user_input]['alias']
        # Fuzzy match alias or title
        all_keys = list(CATEGORY_ALIASES.keys()) + list(CATEGORY_TITLES.keys())
        matches = get_close_matches(user_input, all_keys, n=1, cutoff=0.7)
        if matches:
            match = matches[0]
            if match in CATEGORY_ALIASES:
                return match
            if match in CATEGORY_TITLES:
                return CATEGORY_TITLES[match]['alias']
        return None
    
    def get_user_input(self) -> dict:
        """Get user input for search parameters."""
        print("\n🎯 Yelp Business Mailing List Generator")
        print("=" * 50)
        
        # Location
        location = input("📍 Enter location (city, state, or ZIP code): ").strip()
        if not location:
            print("❌ Location is required!")
            sys.exit(1)
        
        # Business type
        self.display_categories()
        business_type = input("🏢 Enter business type or alias (or press Enter for all types): ").strip().lower()
        
        # Map user input to Yelp category alias
        yelp_category = self.match_category(business_type) if business_type else None
        if business_type and not yelp_category:
            print(f"⚠️  No exact match for '{business_type}'. Searching all types.")
            yelp_category = None
        elif yelp_category:
            print(f"✅ Matched to Yelp category alias: {yelp_category}")
        
        # Search radius
        radius_input = input("🔍 Enter search radius in miles (default: 25, max: 24.85): ").strip()
        try:
            radius_miles = int(radius_input) if radius_input else 25
            radius_meters = radius_miles * 1609  # Convert miles to meters
            if radius_meters > 40000:
                print("⚠️  Yelp API maximum radius is 24.85 miles (40,000 meters). Using 24.85 miles.")
                radius_meters = 40000
        except ValueError:
            print("⚠️  Invalid radius. Using default 25 miles.")
            radius_meters = 25 * 1609
        
        # Max results
        max_results_input = input("📊 Enter maximum number of results (default: 100): ").strip()
        try:
            max_results = int(max_results_input) if max_results_input else 100
        except ValueError:
            print("⚠️  Invalid number. Using default 100 results.")
            max_results = 100
        
        # Filename
        filename = input("📄 Enter output filename (or press Enter for auto-generated): ").strip()
        if filename and not filename.endswith('.xlsx'):
            filename += '.xlsx'
        
        return {
            'location': location,
            'business_type': yelp_category,
            'radius': radius_meters,
            'max_results': max_results,
            'filename': filename if filename else None
        }
    
    def search_and_export(self, params: dict) -> str:
        """
        Search for businesses and export to Excel.
        
        Args:
            params: Dictionary containing search parameters
            
        Returns:
            Path to the created Excel file
        """
        print(f"\n🔍 Searching for businesses in {params['location']}...")
        
        if params['business_type']:
            print(f"🏢 Business type: {params['business_type']}")
        
        print(f"📏 Search radius: {params['radius'] // 1609} miles")
        print(f"📊 Max results: {params['max_results']}")
        print("-" * 50)
        
        # Search for businesses
        businesses = self.yelp_client.search_businesses(
            location=params['location'],
            business_type=params['business_type'],
            radius=params['radius'],
            max_results=params['max_results']
        )
        
        if not businesses:
            print("❌ No businesses found matching your criteria.")
            return ""
        
        print(f"✅ Found {len(businesses)} businesses!")
        
        # Export to Excel
        print("\n📊 Exporting to Excel...")
        filepath = self.excel_generator.export_to_excel(
            businesses=businesses,
            filename=params['filename']
        )
        
        # Create summary sheet
        print("📈 Creating summary sheet...")
        self.excel_generator.create_summary_sheet(businesses, filepath)
        
        return filepath
    
    def run(self):
        """Run the main application."""
        try:
            # Get user input
            params = self.get_user_input()
            
            # Search and export
            filepath = self.search_and_export(params)
            
            if filepath:
                print(f"\n🎉 Success! Mailing list created: {filepath}")
                print(f"📁 File location: {os.path.abspath(filepath)}")
                
                # Show sample data
                if len(params) > 0:
                    print(f"\n📋 Sample of exported data:")
                    print("-" * 50)
                    # This would show sample data, but we'll keep it simple for now
                    print("Open the Excel file to view the complete mailing list.")
            else:
                print("\n❌ Failed to create mailing list.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Operation cancelled by user.")
        except Exception as e:
            print(f"\n❌ An error occurred: {e}")
            print("Please check your API key and try again.")

def main():
    """Main entry point."""
    generator = MailingListGenerator()
    generator.run()

if __name__ == "__main__":
    main() 