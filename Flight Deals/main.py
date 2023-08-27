#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
import flight_search
import flight_data
from datetime import datetime, timedelta

# Maximum number of days to search for flights
MAX_SEARCH_DAYS = 180
# City IATA code for origin city
ORIGIN_CITY_IATA = "BER"
# Dictionary of destinations with maximum price, you can leave iata_code empty
destinations = {
    "Lisbon": {
        "iata_code": "",
        "maximum_price": 80
    },
    "Dublin": {
        "iata_code": "",
        "maximum_price": 52
    }
}

# DON'T CHANGE ANYTHING BELOW HERE

flight_details_list = []

for destination in destinations:
    if destinations[destination]["iata_code"] == "":
        destinations[destination]["iata_code"] = flight_search.FlightSearch.get_iata_code(destination)
    flight_details = flight_search.FlightSearch.get_flight_data(
        ORIGIN_CITY_IATA,
        destinations[destination]["iata_code"],
        (datetime.now() + timedelta(days=1)),
        (datetime.now() + timedelta(days=MAX_SEARCH_DAYS)),
        destinations[destination]["maximum_price"]
    )
    flight_details_list.append(flight_details)
    print(f"{destination}: {destinations[destination]['maximum_price']} ({len(flight_details['data'])})")


flight_data_list = []

for flight in flight_details_list:
    for flight_details in flight["data"]:
        
        flight_object = flight_data.FlightData(
            flight_details["price"],
            flight_details["cityFrom"],
            flight_details["flyFrom"],
            flight_details["cityTo"],
            flight_details["flyTo"],
            flight_details["route"][0]["local_departure"].split("T")[0],
            flight_details["route"][-1]["local_departure"].split("T")[0],
        )

        if len(flight_details["route"])> 2:
            flight_object.stop_overs = 1
            flight_object.via_city = flight_details["route"][0]["cityTo"]

        flight_data_list.append(flight_object)

# create file to store flight_data_list
with open("cheap_flights.txt", "w") as file:
    for flight in flight_data_list:
        #write all flight data
        file.write(f"Low price alert! Only €{flight.price} to fly from {flight.origin_city}-{flight.origin_airport} to {flight.destination_city}-{flight.destination_airport}, from {flight.out_date} to {flight.return_date}.\n")
        if flight.stop_overs > 0:
            file.write(f"Flight has {flight.stop_overs} stop over, via {flight.via_city}.\n")