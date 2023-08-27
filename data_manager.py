import requests
import os

BEARER_TOKEN = os.environ.get("SHEETY_BEARER_TOKEN")
sheet_endpoint = os.environ.get("SHEETY_ENDPOINT")
headers = {
    "Authorization" : f"Bearer {BEARER_TOKEN}"
}

class DataManager:
    #This class is responsible for talking to the Google Sheet.
    def __init__(self):
        pass

    def get_data_from_sheet():
        response = requests.get(url=f"{sheet_endpoint}/flightDeals/prices", headers=headers)
        return response.json()["prices"]
    
    def update_iata_code(row_id, iata_code):
        new_row_params = {
            "price": {
                "iataCode": iata_code
            }
        }
        requests.put(url=f"{sheet_endpoint}/flightDeals/prices/{row_id}", json=new_row_params,headers=headers)