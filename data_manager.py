# data_manager.py 
"""
data manager to interact with Google Sheets via Sheety API

"""
import requests
from config import Config

class DataManager:
    """Google Sheets manager class"""
    
    def __init__(self):
        """initialize data manager"""
        # obtain Sheety API endpoints from config
        prices_endpoint = Config.SHEETY_PRICES_ENDPOINT
        users_endpoint = Config.SHEETY_USERS_ENDPOINT
        
        # # check if endpoints are configured
        # if not prices_endpoint or not users_endpoint:
        #     raise ValueError(
        #         "Sheety API is not configured\n"
        #         "请在.env文件中设置以下变量：\n"
        #         "  - SHEETY_PRICES_ENDPOINT\n"
        #         "  - SHEETY_USERS_ENDPOINT"
        #     )
        
        # endpoints
        self._prices_endpoint: str = prices_endpoint  # pyright: ignore[reportAttributeAccessIssue]
        self._users_endpoint: str = users_endpoint # pyright: ignore[reportAttributeAccessIssue]

        self.destination_data = []
        self.user_data = []
    
    def get_destination_data(self):
        """
        obtain destination data from Google Sheet
        return: list of destination data dicts
        """
        try:
            response = requests.get(url=self._prices_endpoint, timeout=10)
            response.raise_for_status()
            data = response.json()
            self.destination_data = data.get("prices", [])
            return self.destination_data
        except requests.exceptions.RequestException as e:
            raise Exception(f"Fail to obtain the destination data: {e}")
    
    def update_destination_code(self, row_id: int, iata_code: str) -> None:
        """
        update the IATA code for a destination in Google Sheet
        
        parameters:
            row_id: ID of the row to update
            iata_code: code to update
        """
        new_data = {
            "price": {
                "iataCode": iata_code
            }
        }
        try:
            response = requests.put(
                url=f"{self._prices_endpoint}/{row_id}",
                json=new_data,
                timeout=10
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Fail to update IATA code: {e}")
    
    def get_user_emails(self):
        """
        obtain user emails from Google Sheet
        return: list of user email strings
        """
        try:
            response = requests.get(url=self._users_endpoint, timeout=10)
            response.raise_for_status()
            data = response.json()
            self.user_data = data.get("users", [])
            emails = [user["email"] for user in self.user_data if "email" in user]
            return emails
        except requests.exceptions.RequestException as e:
            raise Exception(f"Fail to obatin requests: {e}")
