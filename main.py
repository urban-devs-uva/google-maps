from typing import NamedTuple

import googlemaps
import pandas as pd

class Coordinate(NamedTuple):
    name: str
    longitude: float
    latitude: float

gmaps = googlemaps.Client(key='AIzaSyAyZ5x-tm9dSJc2Xk4iS5A1Amh2jGQi8DM')

metro_tram_df = pd.read_csv("data/TRAMMETRO_PUNTEN_2022.csv", sep=";")
metro_df = metro_tram_df.loc[metro_tram_df["Modaliteit"] == "Metro"]
tram_df = metro_tram_df.loc[metro_tram_df["Modaliteit"] == "Tram"]


metro_coordinates = [
    Coordinate(name="", longitude=row["LNG"], latitude=row["LAT"])
    for _, row in metro_df.iterrows()
]

for index, row in metro_df.iterrows():
    metro_coordinate = [row["LNG"], row["LAT"]]
    metro_coordinates.append(metro_coordinate)


origins = ["Amsterdam", "Utrecht"]
destinations = ["Rotterdam", "The Hague"]

distance_matrix_driving = gmaps.distance_matrix(origins, destinations)
# print(metro_coordinates)
# print(distance_matrix_driving)

for row in distance_matrix_driving["rows"]:
    for element in row["elements"]:
        print(element["distance"])
