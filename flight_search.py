# flight_search.py
"""
flight_search.py
use Amadeus API to search for flights
"""
import requests
# from datetime import datetime
from flight_data import FlightData
from config import Config
from cache_manager import CacheManager

class FlightSearch:
    """use Amadeus API to search for flights"""
    
    def __init__(self):
        """initialize flight search"""
        api_key = Config.AMADEUS_API_KEY
        api_secret = Config.AMADEUS_API_SECRET
        
        # if not api_key or not api_secret:
        #     raise ValueError(
        #         "Amadeus API is not configured\n"
        #         "please .env文件中设置：\n"
        #         "  - AMADEUS_API_KEY\n"
        #         "  - AMADEUS_API_SECRET"
        #     )
        
        self._api_key = api_key
        self._api_secret = api_secret
        
        # initialize cache manager
        self.cache_manager = CacheManager()
        
        # obtain access token
        self._token = self._get_new_token()
        
        # API endpoints
        self._search_endpoint = "https://test.api.amadeus.com/v2/shopping/flight-offers"
        self._city_search_endpoint = "https://test.api.amadeus.com/v1/reference-data/locations/cities"
    
    # get new access token
    def _get_new_token(self):
        """obtain new access token from Amadeus API"""
        print("Obtaining new access token from Amadeus API...")
        
        header = {"Content-Type": "application/x-www-form-urlencoded"}
        body = {
            "grant_type": "client_credentials",
            "client_id": self._api_key,
            "client_secret": self._api_secret
        }
        
        try:
            response = requests.post(
                url="https://test.api.amadeus.com/v1/security/oauth2/token",
                headers=header,
                data=body,
                timeout=10
            )
            response.raise_for_status()
            token = response.json()["access_token"]
            print("Succeed!")
            return token
        except Exception as e:
            raise Exception(f"Failed to obtain the token: {e}")
    
    def get_destination_code(self, city_name):
        """get IATA code for a city (with caching)"""
        # check cache first
        cached_code = self.cache_manager.load_iata_code(city_name)
        if cached_code:
            print(f"IATA code of {city_name}: {cached_code}")
            return cached_code
        
        print(f"Searching for IATA code of {city_name}...")
        
        headers = {"Authorization": f"Bearer {self._token}"}
        params = {
            "keyword": city_name,
            "max": "1",
            "include": "AIRPORTS"
        }
        # testing purpose: limit to 1 result
        try:
            response = requests.get(
                url=self._city_search_endpoint,
                headers=headers,
                params=params,
                timeout=10
            )
            response.raise_for_status()
            # parse response
            data = response.json()
            if data.get("data"):
                code = data["data"][0]["iataCode"]
                # save to cache
                self.cache_manager.save_iata_code(city_name, code)
                return code
            else:
                print(f"Fail to find IATA code of {city_name}")
                return None
                
        except Exception as e:
            print(f"Fail to find IATA code: {e}")
            raise  # for search exception handling
    
    def search_flights(self, origin_city_code, destination_city_code, from_time, to_time):
        """search for flights"""
        # check cache first
        cached_flight = self.cache_manager.load_flight_data(
            origin_city_code,
            destination_city_code
        )
        
        if cached_flight:
            # reconstruct FlightData object from cached data for return
            return FlightData(
                price=cached_flight["price"],
                origin_airport=cached_flight["origin_airport"],
                destination_airport=cached_flight["destination_airport"],
                out_date=cached_flight["out_date"],
                return_date=cached_flight["return_date"],
                airline=cached_flight.get("airline"),
                flight_number=cached_flight.get("flight_number"),
                stops=cached_flight.get("stops", 0),
                booking_link=cached_flight.get("booking_link")
            )
        
        print(f"Searching flight from {origin_city_code} to {destination_city_code} ...")
        # prepare request
        headers = {"Authorization": f"Bearer {self._token}"}
        params = {
            "originLocationCode": origin_city_code,
            "destinationLocationCode": destination_city_code,
            "departureDate": from_time.strftime("%Y-%m-%d"),
            "returnDate": to_time.strftime("%Y-%m-%d"),
            "adults": 1,
            "nonStop": "true",
            "currencyCode": Config.CURRENCY_CODE,
            "max": "1"
        }
        # testing purpose: limit to 1 result
        try:
            response = requests.get(
                url=self._search_endpoint,
                headers=headers,
                params=params,
                timeout=15
            )
            
            if response.status_code != 200:
                print(f"Fail to use API: {response.status_code}")
                raise Exception(f"API error: {response.status_code} - {response.text}")
            
            data = response.json()
            
            if not data.get("data"):
                print(f"No flights found from {origin_city_code} to {destination_city_code}")
                return None
            
            # parse flight data
            flight_info = data["data"][0]
            price = float(flight_info["price"]["total"])

            # information about outbound flight
            outbound = flight_info["itineraries"][0]
            first_segment = outbound["segments"][0]
            last_segment = outbound["segments"][-1]

            origin_airport = first_segment["departure"]["iataCode"]
            destination_airport = last_segment["arrival"]["iataCode"]
            out_date = first_segment["departure"]["at"].split("T")[0]

            # information about inbound flight
            inbound = flight_info["itineraries"][1]
            return_date = inbound["segments"][0]["departure"]["at"].split("T")[0]

            # get airline and flight number
            carrier_code = first_segment.get("carrierCode", "Unknown")
            flight_number = first_segment.get("number", "N/A")

            # number of stops
            stops = len(outbound["segments"]) - 1

            # URL for booking
            booking_link = (f"https://www.google.com/travel/flights?"
                            f"q=Flights%20from%20{origin_airport}%20to%20"
                            f"{destination_airport}%20on%20{out_date}")

            # create FlightData object
            flight_data = FlightData(
                price, 
                origin_airport, 
                destination_airport, 
                out_date, 
                return_date,
                airline=carrier_code,
                flight_number=flight_number,
                stops=stops,
                booking_link=booking_link
            )

            # save to cache
            self.cache_manager.save_flight_data(origin_city_code, destination_city_code, flight_data)

            return flight_data
            
        except Exception as e:
            print(f"Fail to search: {e}")
            raise  # for search exception handling
