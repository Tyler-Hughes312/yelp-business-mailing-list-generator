import requests
import time
from typing import List, Dict, Optional
from config import YELP_API_KEY, YELP_BASE_URL, DEFAULT_LIMIT, MAX_RESULTS

class YelpAPIClient:
    def __init__(self, api_key: Optional[str] = None):
        """Initialize Yelp API client with API key."""
        self.api_key = api_key or YELP_API_KEY
        if not self.api_key:
            raise ValueError("Yelp API key is required. Set YELP_API_KEY environment variable.")
        
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
    
    def search_businesses(self, 
                         location: str,
                         business_type: Optional[str] = None,
                         radius: int = 40000,  # 40km radius
                         limit: int = DEFAULT_LIMIT,
                         max_results: int = MAX_RESULTS) -> List[Dict]:
        """
        Search for businesses using Yelp API.
        
        Args:
            location: City, state, or ZIP code
            business_type: Category of business to search for
            radius: Search radius in meters
            limit: Number of results per request
            max_results: Maximum total results to collect
            
        Returns:
            List of business dictionaries
        """
        businesses = []
        offset = 0
        
        while len(businesses) < max_results:
            # Prepare search parameters
            params = {
                'location': location,
                'radius': radius,
                'limit': min(limit, max_results - len(businesses)),
                'offset': offset
            }
            
            # Add category filter if specified
            if business_type:
                params['categories'] = business_type
            
            try:
                response = requests.get(
                    f'{YELP_BASE_URL}/businesses/search',
                    headers=self.headers,
                    params=params
                )
                
                if response.status_code == 200:
                    data = response.json()
                    new_businesses = data.get('businesses', [])
                    
                    if not new_businesses:
                        break  # No more results
                    
                    businesses.extend(new_businesses)
                    offset += len(new_businesses)
                    
                    # Rate limiting - Yelp allows 5000 requests per day
                    time.sleep(0.1)
                    
                elif response.status_code == 429:
                    print("Rate limit exceeded. Waiting before retrying...")
                    time.sleep(60)  # Wait 1 minute
                    continue
                else:
                    print(f"API Error: {response.status_code} - {response.text}")
                    break
                    
            except requests.exceptions.RequestException as e:
                print(f"Request error: {e}")
                break
        
        return businesses[:max_results]
    
    def get_business_details(self, business_id: str) -> Optional[Dict]:
        """
        Get detailed information for a specific business.
        
        Args:
            business_id: Yelp business ID
            
        Returns:
            Business details dictionary or None if error
        """
        try:
            response = requests.get(
                f'{YELP_BASE_URL}/businesses/{business_id}',
                headers=self.headers
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error getting business details: {response.status_code}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            return None
    
    def search_by_coordinates(self, 
                            latitude: float,
                            longitude: float,
                            business_type: Optional[str] = None,
                            radius: int = 40000,
                            limit: int = DEFAULT_LIMIT) -> List[Dict]:
        """
        Search for businesses using coordinates.
        
        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            business_type: Category of business to search for
            radius: Search radius in meters
            limit: Number of results per request
            
        Returns:
            List of business dictionaries
        """
        params = {
            'latitude': latitude,
            'longitude': longitude,
            'radius': radius,
            'limit': limit
        }
        
        if business_type:
            params['categories'] = business_type
        
        try:
            response = requests.get(
                f'{YELP_BASE_URL}/businesses/search',
                headers=self.headers,
                params=params
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get('businesses', [])
            else:
                print(f"API Error: {response.status_code} - {response.text}")
                return []
                
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            return [] 