# flight-search

A tool for automatically searching and notifying low-price flight deals.

## 1. Environment Setup & Project Initialization

### Clone or Download the Project

Download all project files to your local directory (such as `main.py`, `config.py`, etc.).

### Install Dependencies

Ensure you have Python installed (version 3.8+ recommended).

In the project directory, run:

pip install -r requirements.txt

Main dependencies include: `requests`, `python-dotenv`, `pandas`, and more.

### Configure API Keys & Parameters

Edit the `.env` file in your project root and fill in:

AMADEUS_API_KEY=your_API_key
AMADEUS_API_SECRET=your_API_secret
SHEETY_PRICES_ENDPOINT=your_Sheety_prices_API_endpoint
SHEETY_USERS_ENDPOINT=your_Sheety_users_API_endpoint
EMAIL_USER=email_account_for_notifications
EMAIL_PASS=email_password_for_notifications
ORIGIN_CITY_IATA=IATA_code_of_departure_city (e.g. SYD)
CURRENCY_CODE=Currency code (e.g. AUD, USD)

Refer to the official docs of each API provider to obtain the required keys and endpoints.

### Startup Verification

The program will verify your `.env` settings on startup. If anything is missing, it will display an error and exit.

---

## 2. User Operation Process

### Configure Monitored Destinations & Users

In the Sheety backend table, manually add user emails, monitored destinations, and target prices. See the Sheety integration instructions for details.

Example table format:

| City Name | IATA Code | Target Price (AUD) |
|-----------|-----------|-------------------|
| Melbourne | MEL       | 400               |

User emails are maintained in the Sheety user table, e.g. `user@example.com`.

### Run the Main Program

Navigate to your project directory and run:
python main.py

Main process:
- Verify parameter configuration and cache directory
- Initialize the data manager and query engine
- Retrieve monitoring destinations and user info from the Sheety table
- Automatically complete IATA airport codes
- Configure monitoring targets and recipient emails
- Send notifications

The system will automatically send flight deal alerts via email to all users based on the query results. It will also send alert emails in case of API/network issues.

---

## 3. Platforms and Related Links

- **Sheety**: Create your table in Google Sheets and get the API endpoint via [Sheety](https://sheety.com).
- **Amadeus API**: Register for an account and get your flight search API key & secret at [Amadeus developer portal](https://developers.amadeus.com/).
- **Email Notification**: The project supports email alerts; your email must use an app password if needed for authentication.

> The IATA code for the origin city can be set manually (e.g. SYD); other city info will be filled automatically. All processes are handled by `main.py`; in typical use, simply run the main script.

---

## 4. Further Customization & Extension

If you want to customize monitoring logic or extend data sources, please refer to the code comments and method docs in each module (such as `flight_search.py`, `data_manager.py`).

