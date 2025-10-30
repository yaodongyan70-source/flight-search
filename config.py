# config.py
"""
manage application configuration and environment variables
"""
import os
from dotenv import load_dotenv

# load .env file
load_dotenv()

class Config:
    """application configuration class"""
    
    # Sheety settings
    SHEETY_PRICES_ENDPOINT = os.getenv("SHEETY_PRICES_ENDPOINT")
    SHEETY_USERS_ENDPOINT = os.getenv("SHEETY_USERS_ENDPOINT")
    
    # Amadeus settings
    AMADEUS_API_KEY = os.getenv("AMADEUS_API_KEY")
    AMADEUS_API_SECRET = os.getenv("AMADEUS_API_SECRET")
    
    # Email settings
    EMAIL_USER = os.getenv("EMAIL_USER")
    EMAIL_PASS = os.getenv("EMAIL_PASS")
    
    # Origin city IATA code
    ORIGIN_CITY_IATA = os.getenv("ORIGIN_CITY_IATA", "SYD")
    
    # Currency settings
    CURRENCY_CODE = os.getenv("CURRENCY_CODE", "AUD")
    
    # Currency symbols mapping
    CURRENCY_SYMBOLS = {
        "AUD": "A$",
        "USD": "$",
        "GBP": "£",
        "EUR": "€",
        "JPY": "¥"
    }
    
    # Cache settings
    CACHE_DIR = "cache"
    FLIGHTS_CACHE_DIR = "cache/flights"
    IATA_CACHE_FILE = "cache/iata_codes.json"
    CACHE_EXPIRY_HOURS = 24
    
    @classmethod
    def validate(cls):
        """cheack required environment variables"""
        required = {
            "SHEETY_PRICES_ENDPOINT": cls.SHEETY_PRICES_ENDPOINT,
            "SHEETY_USERS_ENDPOINT": cls.SHEETY_USERS_ENDPOINT,
            "AMADEUS_API_KEY": cls.AMADEUS_API_KEY,
            "AMADEUS_API_SECRET": cls.AMADEUS_API_SECRET,
            "EMAIL_USER": cls.EMAIL_USER,
            "EMAIL_PASS": cls.EMAIL_PASS,
        }
        
        missing = [key for key, value in required.items() if not value]
        
        if missing:
            raise ValueError(f"Missing improtant value: {', '.join(missing)}")
        
        return True
    
    @classmethod
    def setup_cache_dirs(cls):
        """create cache directories if not exist"""
        os.makedirs(cls.CACHE_DIR, exist_ok=True)
        os.makedirs(cls.FLIGHTS_CACHE_DIR, exist_ok=True)
    
    @classmethod
    def get_currency_symbol(cls):
        """get currency symbol based on currency code"""
        return cls.CURRENCY_SYMBOLS.get(cls.CURRENCY_CODE, cls.CURRENCY_CODE)
