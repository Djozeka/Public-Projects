#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
import data_manager
import flight_search
import flight_data
from datetime import datetime, timedelta

sheet_data = data_manager.DataManager.get_data_from_sheet()

ORIGIN_CITY_IATA = "BER"

for row in sheet_data:
    if row["iataCode"] == "":
        row["iataCode"] = flight_search.FlightSearch.get_iata_code(row["city"])
        data_manager.DataManager.update_iata_code(row["id"], row["iataCode"])
    else:
        print(f"{row['city']}: {row['lowestPrice']}")
        flight_details = flight_search.FlightSearch.get_flight_data(
            ORIGIN_CITY_IATA,
            row["iataCode"],
            (datetime.now() + timedelta(days=1)),
            (datetime.now() + timedelta(days=180)),
            row["lowestPrice"]
        )

flight_data_list = []

for flight in flight_details["data"]:
    flight_object = flight_data.FlightData(
        flight["price"],
        flight["cityFrom"],
        flight["flyFrom"],
        flight["cityTo"],
        flight["flyTo"],
        flight["route"][0]["local_departure"].split("T")[0],
        flight["route"][1]["local_departure"].split("T")[0]
    )
        
    flight_data_list.append(flight_object)

# create file to store flight_data_list
with open("flight_data.txt", "w") as file:
    for flight in flight_data_list:
        #write all flight data
        file.write(f"Low price alert! Only €{flight.price} to fly from {flight.origin_city}-{flight.origin_airport} to {flight.destination_city}-{flight.destination_airport}, from {flight.out_date} to {flight.return_date}.\n")
