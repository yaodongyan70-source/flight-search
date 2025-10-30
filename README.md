# flight-search
use for search the low price flightiness
I. Environmental Preparation and Project Initiation
• Clone/Download Project
Download all project files to the local directory, including main.py, config.py, etc.
• Install Dependencies
Ensure Python is installed (version 3.8 or above is recommended).
Dependencies for the project can be installed via the command: pip install -r requirements.txt
Dependencies include requests, python-dotenv, pandas, etc.
• Configure API keys and parameters
Edit the .env file in the project root directory and fill in the following information:
AMADEUS_API_KEY = Your API key
AMADEUS_API_SECRET = Your API secret
SHEETY_PRICES_ENDPOINT = Your Sheety price data endpoint
SHEETY_USERS_ENDPOINT = Your Sheety user data endpoint
EMAIL_USER = Email account for notifications
EMAIL_PASS = Password for notifications
ORIGIN_CITY_IATA = IATA code of the departure city (e.g. SYD)
CURRENCY_CODE = Currency (e.g. AUD, USD)
For obtaining API keys and configuring Sheety, please refer to their respective official websites.
Verification steps before the first startup
When the project starts, it will automatically detect the parameter configuration in the .env file. If there are any omissions, it will prompt an error and exit.
II. User operation process
• In the Sheety backend table (see the integration instructions on the Sheety website), you can manually add the user email and the destinations and target prices to be monitored.
Example format:
City name IATA code Expected price (AUD)
Melbourne MEL 400
The user email is maintained in the Sheety user table, such as user@example.com.
• Run the main program
Enter the project directory in the command line and start the main process: python main.py
After the main program starts, it will proceed with the following tasks in sequence:
- Checking parameter configuration and cache directory
- Initializing data manager and query engine
- Obtaining the list of monitoring destinations, and retrieving user and monitoring destination information from the Sheety table
- Automatically completing airport IATA codes
- Configuring monitoring targets and user email addresses
- Viewing and handling notifications
The system automatically sends email notifications to all users with low-cost flight information based on the query results. In case of API/network anomalies, it will also automatically send alarm emails.
III. Open platform and related web pages Sheety
Users need to create a table on the Google Sheet website and obtain the API Endpoint from Sheety for configuring the .env file.
Sheety official website: https://sheety.com  
Amadeus API
Register for a developer account to obtain the flight search API key and Secret for real-time flight ticket inquiries. 
Amadeus official website: https://developers.amadeus.com/  
Email Notification
Project Support: Email service is provided. The email configuration must support the authorization password for related applications. Note
Departure city IATA code can be set manually (e.g. SYD), and the other city items will be automatically completed.
All project processes are implemented in main.py. For regular use, only the main program needs to be run. All queries and notifications will be automatically executed without the need for manual intervention.
If you need to further customize the monitoring logic or extend the data sources, please refer to the comments and method descriptions of each module (such as flight_search.py, data_manager.py).
