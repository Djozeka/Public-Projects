import requests
import os

TEQUILA_KIWI_API_KEY = os.environ.get("TEQUILA_KIWI_API_KEY")


# create headers for api call
headers = {
    "apikey": TEQUILA_KIWI_API_KEY
}

class FlightSearch:
    #This class is responsible for talking to the Flight Search API.
    def get_iata_code(city):
        tequila_kiwi_endpoint = "https://tequila-api.kiwi.com/locations/query"
        # create params for api call
        params = {
            "term": city,
            "location_types": "city"
        }
        # create api call to get iata code
        response = requests.get(url=tequila_kiwi_endpoint, params=params, headers=headers)
        return response.json()["locations"][0]["code"]
    
    def get_flight_data(origin_city_code, destination_city_code, from_time, to_time,max_price):
        """This function will get flight data from tequila kiwi api"""
        tequila_kiwi_endpoint = "https://tequila-api.kiwi.com/v2/search"
        #get flight data from tequila kiwi api
        # create params for api call
        params = {
            "fly_from": origin_city_code,
            "fly_to": destination_city_code,
            "date_from": from_time.strftime("%d/%m/%Y"),
            "date_to": to_time.strftime("%d/%m/%Y"),
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 15,
            "flight_type": "round",
            "curr": "EUR",
            "max_stopovers": 0,
            "price_to": max_price
        }
        # create api call to get flight data
        response = requests.get(url=tequila_kiwi_endpoint, params=params, headers=headers)
        if response.json()["data"] == []:
            params["max_stopovers"] = 2
            print("No direct flights found, searching for flights with 1 stopover")
            response = requests.get(url=tequila_kiwi_endpoint, params=params, headers=headers)

        return response.json()




        