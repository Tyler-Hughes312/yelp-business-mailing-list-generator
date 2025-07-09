#!/usr/bin/env python3
"""
Example usage of the Yelp Business Mailing List Generator

This script demonstrates how to use the mailing list generator
programmatically without the interactive interface.
"""

from yelp_api_client import YelpAPIClient
from excel_generator import ExcelGenerator
from config import BUSINESS_CATEGORIES

def example_nashville_restaurants():
    """Example: Search for restaurants in Nashville and export to Excel."""
    print("🍽️  Example: Nashville Restaurants Mailing List")
    print("=" * 50)
    
    # Initialize clients
    yelp_client = YelpAPIClient()
    excel_generator = ExcelGenerator()
    
    # Search parameters
    location = "Nashville, TN"
    business_type = BUSINESS_CATEGORIES['restaurants']
    radius = 25 * 1609  # 25 miles in meters
    max_results = 50
    
    print(f"📍 Location: {location}")
    print(f"🏢 Business Type: Restaurants")
    print(f"📏 Radius: 25 miles")
    print(f"📊 Max Results: {max_results}")
    print("-" * 50)
    
    # Search for businesses
    print("🔍 Searching for restaurants...")
    businesses = yelp_client.search_businesses(
        location=location,
        business_type=business_type,
        radius=radius,
        max_results=max_results
    )
    
    if not businesses:
        print("❌ No restaurants found.")
        return
    
    print(f"✅ Found {len(businesses)} restaurants!")
    
    # Export to Excel
    print("📊 Exporting to Excel...")
    filepath = excel_generator.export_to_excel(
        businesses=businesses,
        filename="nashville_restaurants.xlsx"
    )
    
    # Create summary sheet
    excel_generator.create_summary_sheet(businesses, filepath)
    
    print(f"🎉 Success! File created: {filepath}")
    return filepath

def example_healthcare_providers():
    """Example: Search for healthcare providers in a specific area."""
    print("\n🏥 Example: Healthcare Providers Mailing List")
    print("=" * 50)
    
    # Initialize clients
    yelp_client = YelpAPIClient()
    excel_generator = ExcelGenerator()
    
    # Search parameters
    location = "37203"  # Nashville ZIP code
    business_type = BUSINESS_CATEGORIES['healthcare']
    radius = 10 * 1609  # 10 miles in meters
    max_results = 100
    
    print(f"📍 Location: {location}")
    print(f"🏢 Business Type: Healthcare")
    print(f"📏 Radius: 10 miles")
    print(f"📊 Max Results: {max_results}")
    print("-" * 50)
    
    # Search for businesses
    print("🔍 Searching for healthcare providers...")
    businesses = yelp_client.search_businesses(
        location=location,
        business_type=business_type,
        radius=radius,
        max_results=max_results
    )
    
    if not businesses:
        print("❌ No healthcare providers found.")
        return
    
    print(f"✅ Found {len(businesses)} healthcare providers!")
    
    # Export to Excel
    print("📊 Exporting to Excel...")
    filepath = excel_generator.export_to_excel(
        businesses=businesses,
        filename="healthcare_providers.xlsx"
    )
    
    # Create summary sheet
    excel_generator.create_summary_sheet(businesses, filepath)
    
    print(f"🎉 Success! File created: {filepath}")
    return filepath

def example_all_businesses():
    """Example: Search for all types of businesses in an area."""
    print("\n🏢 Example: All Businesses Mailing List")
    print("=" * 50)
    
    # Initialize clients
    yelp_client = YelpAPIClient()
    excel_generator = ExcelGenerator()
    
    # Search parameters
    location = "Franklin, TN"
    business_type = None  # All types
    radius = 15 * 1609  # 15 miles in meters
    max_results = 200
    
    print(f"📍 Location: {location}")
    print(f"🏢 Business Type: All Types")
    print(f"📏 Radius: 15 miles")
    print(f"📊 Max Results: {max_results}")
    print("-" * 50)
    
    # Search for businesses
    print("🔍 Searching for all businesses...")
    businesses = yelp_client.search_businesses(
        location=location,
        business_type=business_type,
        radius=radius,
        max_results=max_results
    )
    
    if not businesses:
        print("❌ No businesses found.")
        return
    
    print(f"✅ Found {len(businesses)} businesses!")
    
    # Export to Excel
    print("📊 Exporting to Excel...")
    filepath = excel_generator.export_to_excel(
        businesses=businesses,
        filename="franklin_all_businesses.xlsx"
    )
    
    # Create summary sheet
    excel_generator.create_summary_sheet(businesses, filepath)
    
    print(f"🎉 Success! File created: {filepath}")
    return filepath

def main():
    """Run all examples."""
    print("🚀 Yelp Business Mailing List Generator - Examples")
    print("=" * 60)
    
    try:
        # Run examples
        example_nashville_restaurants()
        example_healthcare_providers()
        example_all_businesses()
        
        print("\n🎉 All examples completed successfully!")
        print("📁 Check the 'output' folder for the generated Excel files.")
        
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        print("Please check your API key and try again.")

if __name__ == "__main__":
    main() 