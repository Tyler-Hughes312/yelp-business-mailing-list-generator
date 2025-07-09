# Yelp Business Mailing List Generator

A Python application that uses the Yelp Fusion API to search for businesses and generate mailing lists in Excel format. Perfect for creating targeted business contact lists based on location, business type, and area.

## Features

- 🔍 **Yelp API Integration**: Uses Yelp Fusion API for accurate business data
- 📍 **Location-based Search**: Search by city, state, or ZIP code
- 🏢 **Business Type Filtering**: Filter by specific business categories
- 📏 **Customizable Radius**: Set search radius in miles
- 📊 **Excel Export**: Clean, formatted Excel files with auto-adjusted columns
- 📈 **Summary Statistics**: Additional sheet with business statistics
- 🎯 **Interactive Interface**: User-friendly command-line interface
- 🔧 **Programmatic API**: Use in your own scripts

## Prerequisites

- Python 3.7 or higher
- Yelp Fusion API key (free tier available)

## Installation

1. **Clone or download this project**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your Yelp API key**:
   - Get a free API key from [Yelp Fusion API](https://www.yelp.com/developers)
   - Create a `.env` file in the project root
   - Add your API key:
     ```
     YELP_API_KEY=your_api_key_here
     ```

## Usage

### Web Interface (Recommended)

For the easiest experience, use the web interface:

```bash
python run_web_interface.py
```

This will:
- Check all dependencies and install Flask if needed
- Verify your API key is set up correctly
- Start a web server at http://localhost:8080
- Open your browser automatically

**Features:**
- Beautiful, modern web interface
- Searchable business category dropdown
- Real-time validation
- Automatic file download
- Mobile-friendly design

### Deploy to the Internet

To make your app accessible to anyone:

```bash
python deploy_to_render.py
```

This will:
- Check your project setup
- Generate deployment configuration
- Show step-by-step deployment instructions

**Recommended platforms:**
- **Render** (Free) - Easiest for beginners
- **Railway** (Free) - Quick deployment
- **PythonAnywhere** (Free) - Python-focused
- **Vercel** (Free) - Modern platform

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

### Interactive Mode

Run the main application for an interactive experience:

```bash
python main.py
```

The application will prompt you for:
- Location (city, state, or ZIP code)
- Business type (optional)
- Search radius in miles
- Maximum number of results
- Output filename (optional)

### Programmatic Usage

Use the example script to see how to use the API programmatically:

```bash
python example.py
```

Or import and use in your own code:

```python
from yelp_api_client import YelpAPIClient
from excel_generator import ExcelGenerator
from config import BUSINESS_CATEGORIES

# Initialize clients
yelp_client = YelpAPIClient()
excel_generator = ExcelGenerator()

# Search for restaurants in Nashville
businesses = yelp_client.search_businesses(
    location="Nashville, TN",
    business_type=BUSINESS_CATEGORIES['restaurants'],
    radius=25 * 1609,  # 25 miles in meters
    max_results=100
)

# Export to Excel
filepath = excel_generator.export_to_excel(
    businesses=businesses,
    filename="nashville_restaurants.xlsx"
)
```

## Available Business Categories

The application supports these business categories:

- **Restaurants**: Food and dining establishments
- **Retail**: Shopping and retail stores
- **Healthcare**: Medical and health services
- **Automotive**: Car-related services
- **Professional**: Professional services
- **Beauty**: Beauty and personal care
- **Fitness**: Health and fitness
- **Entertainment**: Arts and entertainment
- **Real Estate**: Real estate services
- **Legal**: Legal services
- **Financial**: Financial services
- **Education**: Educational institutions
- **Home Services**: Home improvement and services
- **Hotels**: Hotels and travel
- **Nightlife**: Bars and nightlife
- **Pets**: Pet services
- **Religious**: Religious organizations
- **Local Services**: Local service providers

## Output Format

The generated Excel file includes:

### Main Sheet: Business Mailing List
- Business Name
- Address (full formatted address)
- City
- State
- ZIP Code
- Phone Number
- Website URL
- Business Type
- Rating
- Review Count
- Price Level
- Yelp URL

### Summary Sheet
- Total Businesses
- Average Rating
- Businesses with Phone Numbers
- Businesses with Websites
- Top Business Type
- Top City

## API Limits

- **Yelp Fusion API**: 5000 requests per day (free tier)
- **Rate Limiting**: Built-in rate limiting to respect API limits
- **Pagination**: Automatic handling of large result sets

## File Structure

```
TomProject/
├── main.py                 # Main interactive application
├── app.py                  # Flask web application
├── run_web_interface.py    # Web interface runner
├── deploy_to_render.py     # Deployment helper
├── example.py              # Example usage script
├── yelp_api_client.py      # Yelp API client
├── excel_generator.py      # Excel export functionality
├── config.py               # Configuration and constants
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── DEPLOYMENT.md          # Deployment instructions
├── Procfile               # Heroku deployment config
├── runtime.txt            # Python version for deployment
├── .env                   # API key (create this)
├── templates/             # Web interface templates
│   └── index.html         # Main web interface
└── output/                # Generated Excel files
```

## Error Handling

The application includes comprehensive error handling for:
- Missing API key
- API rate limits
- Network errors
- Invalid user input
- File creation issues

## Customization

### Adding New Business Categories

Edit `config.py` to add new business categories:

```python
BUSINESS_CATEGORIES = {
    'your_category': 'yelp_category_alias',
    # ... existing categories
}
```

### Modifying Excel Output

Edit `config.py` to change Excel columns:

```python
EXCEL_COLUMNS = [
    'Business Name',
    'Address',
    # ... add or remove columns
]
```

### Adjusting Search Parameters

Modify default values in `config.py`:

```python
DEFAULT_LIMIT = 50      # Results per request
MAX_RESULTS = 1000      # Maximum total results
```

## Troubleshooting

### Common Issues

1. **"API key is required" error**:
   - Make sure your `.env` file exists and contains `YELP_API_KEY=your_key`

2. **"No businesses found"**:
   - Check your location spelling
   - Try a larger search radius
   - Verify the business category exists

3. **Rate limit errors**:
   - The application automatically handles rate limits
   - Wait a few minutes and try again

4. **Excel file not created**:
   - Check that the `output` directory exists
   - Ensure you have write permissions

### Getting Help

- Check the Yelp Fusion API documentation
- Verify your API key is active
- Test with a simple location first

## License

This project is for educational and personal use. Please respect Yelp's terms of service and API usage guidelines.

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve this tool. 