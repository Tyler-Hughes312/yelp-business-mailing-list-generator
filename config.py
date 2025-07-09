import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Yelp API Configuration
YELP_API_KEY = os.getenv('YELP_API_KEY')
YELP_BASE_URL = 'https://api.yelp.com/v3'

# Default search parameters
DEFAULT_LIMIT = 50  # Maximum results per request
MAX_RESULTS = 1000  # Maximum total results to collect

# Business categories for filtering
BUSINESS_CATEGORIES = {
    'restaurants': 'restaurants',
    'retail': 'shopping',
    'healthcare': 'health',
    'automotive': 'automotive',
    'professional': 'professional',
    'beauty': 'beautysvc',
    'fitness': 'active',
    'entertainment': 'arts',
    'real_estate': 'realestate',
    'legal': 'lawyers',
    'financial': 'financialservices',
    'education': 'education',
    'home_services': 'homeservices',
    'hotels': 'hotelstravel',
    'nightlife': 'nightlife',
    'pets': 'pets',
    'religious': 'religiousorgs',
    'local_services': 'localservices'
}

# Excel export settings
EXCEL_COLUMNS = [
    'Business Name',
    'Address',
    'City',
    'State',
    'ZIP Code',
    'Phone',
    'Website',
    'Business Type',
    'Rating',
    'Review Count',
    'Price Level',
    'Yelp URL'
] 