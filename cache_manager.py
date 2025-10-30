# cache_manager.py
"""
cache_manager to handle caching of flight data and IATA codes
"""
import json
import os
from datetime import datetime, timedelta
from config import Config

class CacheManager:
   
    
    def __init__(self):
        self.cache_dir = Config.FLIGHTS_CACHE_DIR
        self.iata_cache_file = Config.IATA_CACHE_FILE
        self.expiry_hours = Config.CACHE_EXPIRY_HOURS
    
    def _get_cache_filename(self, origin, destination):
        """create a cache filename based on origin and destination"""
        return f"{self.cache_dir}/{origin}_{destination}.json"
    
    def save_flight_data(self, origin, destination, flight_data):
        """save flight data to cache"""
        cache_file = self._get_cache_filename(origin, destination)
        # cache structure
        cache_data = {
            "timestamp": datetime.now().isoformat(),
            "origin": origin,
            "destination": destination,
            "data": {
                "price": flight_data.price,
                "origin_airport": flight_data.origin_airport,
                "destination_airport": flight_data.destination_airport,
                "out_date": flight_data.out_date,
                "return_date": flight_data.return_date,
                "airline": getattr(flight_data, 'airline', None),           
                "flight_number": getattr(flight_data, 'flight_number', None), 
                "stops": getattr(flight_data, 'stops', 0),                   
                "booking_link": getattr(flight_data, 'booking_link', None)   
            }
        }
    
        with open(cache_file, 'w') as f:
            json.dump(cache_data, f, indent=2)
        
        print(f"Saved: {origin} → {destination}")

    
    def load_flight_data(self, origin, destination):
        """load flight data from cache if is expired"""
        cache_file = self._get_cache_filename(origin, destination)
        
        if not os.path.exists(cache_file):
            return None
        
        with open(cache_file, 'r') as f:
            cache_data = json.load(f)
        
        # cheack whether cache is expired
        cached_time = datetime.fromisoformat(cache_data["timestamp"])
        if datetime.now() - cached_time > timedelta(hours=self.expiry_hours):
            print(f"Cache is expired: {origin} → {destination}")
            return None
        
        print(f"Useing the cache data: {origin} → {destination}")
        return cache_data["data"]
    
    def save_iata_code(self, city, iata_code):
        """save IATA code to cache"""
        if os.path.exists(self.iata_cache_file):
            with open(self.iata_cache_file, 'r') as f:
                iata_cache = json.load(f)
        else:
            iata_cache = {}
        
        iata_cache[city.lower()] = iata_code
        
        with open(self.iata_cache_file, 'w') as f:
            json.dump(iata_cache, f, indent=2)
    
    def load_iata_code(self, city):
        """load IATA code from cache"""
        if not os.path.exists(self.iata_cache_file):
            return None
        
        with open(self.iata_cache_file, 'r') as f:
            iata_cache = json.load(f)
        
        return iata_cache.get(city.lower())
