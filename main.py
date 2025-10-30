# main.py
"""
main.py
for flight price monitoring and notification

"""
from datetime import datetime, timedelta
from config import Config
from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager

def print_header(title):
    """print formatted header"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)

def send_api_failure_notification(notification_manager, data_manager, error_message):
    """send notification to users about API failure"""
    try:
        users = data_manager.get_user_emails()
        if users:
            message = (
                f"Flight price monitoring system notification\n\n"
                f"API call failed :<\n\n"
                f"The system encountered a problem when calling the Amadeus API：\n"
                f"{error_message}\n\n"
                f"possible reasons\n"
                f"• The API key has expired or become invalid\n"
                f"• Network connection issue\n"
                f"• The API service is temporarily unavailable\n"
                f"• The monthly API quota has been exhausted\n\n"
                f"Suggestion: Please try again later or check the API configuration.\n\n"
                f"— Flight price monitoring system"
            )
            notification_manager.send_email(message, users)
            print("An API failure notification has been sent to the user")
    except Exception as e:
        print(f"Failed to send notification: {e}")

def main():
    """main function for flight price monitoring and notification"""
    
    print_header("The flight price monitoring system has been activated!!")
    
    currency_symbol = Config.get_currency_symbol()
    
    # ===== Verifying the configuration =====
    print("\n verifying the configuration...")
    try:
        Config.validate()
        Config.setup_cache_dirs()
        print("Configuration verification passed")
    except Exception as e:
        print(f"Configuration error: {e}")
        print("\n Please check whether the.env file is configured correctly")
        exit(1)
    
    # ===== Initialization module =====
    print_header("Initialization module")
    try:
        data_manager = DataManager()
        print("The data manager has been initialized successfully!!")
        
        flight_search = FlightSearch()
        print("The flight search engine has been initialized successfully!!")
        
        notification_manager = NotificationManager()
        print("Notify the manager that the initialization was successful!!")
    except Exception as e:
        print(f"Failed to initialize: {e}")
        exit(1)
    
    # ===== Setting parameters =====
    origin = Config.ORIGIN_CITY_IATA
    search_start = datetime.now() + timedelta(days=1)
    search_end = datetime.now() + timedelta(days=10)
    
    print(f"\n Searchable configuration:")
    print(f"   Place of departure: {origin}")
    print(f"   Date: {search_start.strftime('%Y-%m-%d')} to {search_end.strftime('%Y-%m-%d')}")
    
    # ===== Obtain destination data =====
    print_header("Get the list of monitoring destinations")
    try:
        destinations = data_manager.get_destination_data()
        print(f"Succeed to obtain {len(destinations)} destination/s")
    except Exception as e:
        print(f"Fail to obtain destination: {e}")
        exit(1)
    
    # ===== Gettting IATA code =====
    print_header("Check and fill in the IATA airport code")
    api_failed = False
    
    for dest in destinations:
        if not dest.get("iataCode"):
            try:
                iata = flight_search.get_destination_code(dest["city"])
                if iata:
                    data_manager.update_destination_code(dest["id"], iata)
                    dest["iataCode"] = iata
                    print(f"{dest['city']} → {iata}")
            except Exception as e:
                print(f"API call failed: {e}")
                api_failed = True
                send_api_failure_notification(notification_manager, data_manager, str(e))
                break
    
    if api_failed:
        print("\n The program ended prematurely due to a failed API call")
        exit(1)
    
    # ===== Search flights =====
    print_header("Search for lowest priced flights")
    found_deals = []
    no_flights_found = []
    price_not_met = []
    skipped_destinations = []
    
    for dest in destinations:
        if not dest.get("iataCode"):
            print(f" Skip {dest['city']}(no IATA code)")
            skipped_destinations.append(dest['city'])
            continue
        
        print(f"\n  Searching for {dest['city']} ({dest['iataCode']})")
        
        try:
            flight = flight_search.search_flights(
                origin,
                dest["iataCode"],
                search_start,
                search_end
            )
            
            if flight is None:
                print(f"    No direct flight was found")
                no_flights_found.append(dest['city'])
            elif flight:
                print(f"   Price: {currency_symbol}{flight.price}")
                
                if flight.price < dest["lowestPrice"]:
                    print(f"    Lowest price found! (Target: {currency_symbol}{dest['lowestPrice']})")
                    found_deals.append({
                        "destination": dest["city"],
                        "flight": flight,
                        "target_price": dest["lowestPrice"]
                    })
                else:
                    print(f"    No flight under (Target: {currency_symbol}{dest['lowestPrice']})")
                    price_not_met.append({
                        "city": dest['city'],
                        "current_price": flight.price,
                        "target_price": dest["lowestPrice"]
                    })
        
        except Exception as e:
            print(f" API call failed: {e}")
            send_api_failure_notification(notification_manager, data_manager, str(e))
            break
    
    # ===== Send notifications to users =====
    print_header("Send notifications to users")
    
    try:
        users = data_manager.get_user_emails()
        if not users:
            print("  No users found, skipping notification sending")
        else:
            # send deal notifications
            if found_deals:
                print(f"\n Find {len(found_deals)} lowest priced flight/s")
                for deal in found_deals:
                    flight = deal["flight"]
                    
                    flight_type = "direct flight" if getattr(flight, 'stops', 0) == 0 else f"{getattr(flight, 'stops', 0)}次中转"
                    airline = getattr(flight, 'airline', 'N/A')
                    flight_number = getattr(flight, 'flight_number', '')
                    airline_info = f"{airline} {flight_number}".strip() if airline != 'N/A' else "N/A"
                    booking_link = getattr(flight, 'booking_link', 'https://www.google.com/flights')

                    message = (
                        f" Lowest priced air tickets discovered!!\n\n"
                        f" Destination: {deal['destination']}\n"
                        f" Current price: {currency_symbol}{flight.price}\n"
                        f" Target price: {currency_symbol}{deal['target_price']}\n"
                        f" Save: {currency_symbol}{(deal['target_price'] - flight.price):.2f}\n\n"
                        f" Departure: {flight.origin_airport}\n"
                        f" Destination: {flight.destination_airport}\n"
                        f" Date to outbound: {flight.out_date}\n"
                        f" Date to inbound: {flight.return_date}\n"
                        f" Airline: {airline_info}\n"
                        f" Flight type: {flight_type}\n\n"
                        f" Booking URL:\n{booking_link}\n\n"
                        f" Prices may change at any time. Please make your reservation as soon as possible!!\n\n"
                        f"— Flight price monitoring system"
                    )

                    notification_manager.send_email(message, users)
                    print(f"   Sended notification  ")
            
            # send summary report
            if price_not_met or no_flights_found or skipped_destinations:
                print(f"\n Send the query summary report...")
                
                summary_parts = [
                    f" Flight price monitoring report\n\n",
                    f" Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n",
                    f" Departure: {origin}\n\n"
                ]
                
                if found_deals:
                    summary_parts.append(f" Number of low price flight: {len(found_deals)} \n")
                    for deal in found_deals:
                        summary_parts.append(f"  • {deal['destination']}: {currency_symbol}{deal['flight'].price}\n")
                    summary_parts.append("\n")
                else:
                    summary_parts.append(f" No low-priced flights were found this time\n\n")
                
                if price_not_met:
                    summary_parts.append(f" Number of the price not reached the target : {len(price_not_met)} :\n")
                    for item in price_not_met:
                        diff = item['current_price'] - item['target_price']
                        summary_parts.append(
                            f"  • {item['city']}: {currency_symbol}{item['current_price']} "
                            f"(Target: {currency_symbol}{item['target_price']}, Gap: {currency_symbol}{diff:.2f})\n"
                        )
                    summary_parts.append("\n")
                
                if no_flights_found:
                    summary_parts.append(f" No direct flight was found. ({len(no_flights_found)}):\n")
                    for city in no_flights_found:
                        summary_parts.append(f"  • {city}\n")
                    summary_parts.append("\n")
                
                if skipped_destinations:
                    summary_parts.append(f" Skip number: ({len(skipped_destinations)} ):\n")
                    for city in skipped_destinations:
                        summary_parts.append(f"  • {city} (Need IATA code)\n")
                    summary_parts.append("\n")
                
                summary_parts.append(f" Suggestion: It is possible to consider adjusting the target price or monitoring other destinations.\n\n")
                summary_parts.append(f"— Flight price monitoring system")
                
                summary_message = "".join(summary_parts)
                notification_manager.send_email(summary_message, users)
                print(f"  The query summary has been sent")
    
    except Exception as e:
        print(f" Fail to notification: {e}")
    
    # ===== Finish =====
    print_header(" The program has completed running.")
    print(f"   Valid destination: {len(destinations)} ")
    print(f"   Lowest price: {len(found_deals)} \n")

if __name__ == "__main__":
    main()


#save