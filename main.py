import googlemaps
import pandas as pd
import itertools

gmaps = googlemaps.Client(key="AIzaSyAyZ5x-tm9dSJc2Xk4iS5A1Amh2jGQi8DM")

hub_addresses = []
with open("data/mobility_hub_addresses.txt") as file:
    lines = file.readlines()
    hub_addresses = [line.replace("\n", "") + " Amsterdam" for line in lines]

hubs_batches = itertools.batched(hub_addresses, 10)

train_stations = []
with open("data/train_stations.txt") as file:
    lines = file.readlines()
    train_stations = [line.replace("\n", "") for line in lines]

train_stations_batches = itertools.batched(train_stations, 10)

metro_tram_df = pd.read_csv("data/TRAMMETRO_PUNTEN_2022.csv", sep=";")
metro_df = metro_tram_df.loc[metro_tram_df["Modaliteit"] == "Metro"]
tram_df = metro_tram_df.loc[metro_tram_df["Modaliteit"] == "Tram"]

metro_coordinates = [[row["LNG"], row["LAT"]] for _, row in metro_df.iterrows()]

df_hubs_data = pd.DataFrame({"Mobility hub": hub_addresses})


def find_nearest_from_destination_list(hub, destinations, mode):
    nearest_destination = ""
    distance_to_nearest = 999999999
    for destination in destinations:
        directions = gmaps.directions(hub, destination, mode=mode)
        distance = directions[0]["legs"][0]["distance"]["value"]
        if distance < distance_to_nearest:
            distance_to_nearest = distance
            nearest_destination = destination
    return {"name": nearest_destination, "distance": distance_to_nearest}


nearest_stations = {
    "walking": [
        find_nearest_from_destination_list(hub, train_stations, "walking")
        for hub in hub_addresses
    ],
    "biking": [
        find_nearest_from_destination_list(hub, train_stations, "bicycling")
        for hub in hub_addresses
    ],
}

df_hubs_data["Nearest station (walking)"] = [
    station["name"] for station in nearest_stations["walking"]
]
df_hubs_data["Distance to nearest train station (walking)"] = [
    station["distance"] for station in nearest_stations["walking"]
]
df_hubs_data["Nearest station (biking)"] = [
    station["name"] for station in nearest_stations["biking"]
]
df_hubs_data["Distance to nearest train station (biking)"] = [
    station["distance"] for station in nearest_stations["biking"]
]

df_hubs_data.to_csv("results/mobility_hub_google_maps_data.csv")

"""
The result should be dataset with each mobility hub per row and some new observations
derived from this per column.

Likely relevant, achievable data:
- distance to the nearest train station
- distance to nearest tram/metro/bus point (separately)
- distance to nearest other mobility hub
- 

Other ideas (harder to get):
- distance to nearest "shopping centre"
- aggregation of residences in area
- aggregation of restaurants and shops in area 
- traffic in the area
- distance to nearest park
- distance to A10
- distance to parking lot
- distance to landmarks
- distance to university
- 

"""
