
"""
flight_data.py
save flight data structure
"""

class FlightData:
    """save flight data structure"""
    
    def __init__(self, price, origin_airport, destination_airport, out_date, return_date, 
                 airline=None, flight_number=None, stops=0, booking_link=None):
        """
        initialize flight data
        
        parameters:
            price: flight price
            origin_airport: origin airport code
            destination_airport: destination airport code
            out_date: outbound date
            return_date: return date
            airline: airline name
            flight_number: flight number        
        """
        self.price = price
        self.origin_airport = origin_airport
        self.destination_airport = destination_airport
        self.out_date = out_date
        self.return_date = return_date
        self.airline = airline
        self.flight_number = flight_number
        self.stops = stops
        self.booking_link = booking_link
    
    def __str__(self):
        """return string representation of flight data"""
        flight_type = "Direct flight" if self.stops == 0 else f"{self.stops} connecting flights"
        airline_info = f" | {self.airline}" if self.airline else ""
        
        return (f"Flight information: ${self.price}{airline_info} | "
                f"{self.origin_airport} → {self.destination_airport} | "
                f"{self.out_date} to {self.return_date} | {flight_type}")
    
    def get_google_flights_link(self):
        """return the Google Flights booking link"""
        # Google Flights URL format
        return (f"https://www.google.com/travel/flights?"
                f"q=Flights%20from%20{self.origin_airport}%20to%20"
                f"{self.destination_airport}%20on%20{self.out_date}")
