import pandas as pd
import itertools

gmaps_matrix_size_limit = 10


def batch_for_gmaps(data):
    if len(data) <= gmaps_matrix_size_limit:
        return data
    batched_data = []
    it = iter(data)
    while batch := list(itertools.islice(it, gmaps_matrix_size_limit)):
        batched_data.append(batch)
    return batched_data


hub_addresses = []
with open("data/mobility_hub_addresses.txt") as file:
    lines = file.readlines()
    hub_addresses = [f'{line.replace("\n", "")} Amsterdam' for line in lines]
hubs_batches = batch_for_gmaps(hub_addresses)


train_stations = []
with open("data/train_stations.txt") as file:
    lines = file.readlines()
    train_stations = [line.replace("\n", "") for line in lines]
train_stations_batches = batch_for_gmaps(train_stations)


metro_tram_df = pd.read_csv("data/TRAMMETRO_PUNTEN_2022.csv", sep=";")
metro_df = metro_tram_df.loc[metro_tram_df["Modaliteit"] == "Metro"]
tram_df = metro_tram_df.loc[metro_tram_df["Modaliteit"] == "Tram"]

metro_coordinates = [[row["LNG"], row["LAT"]] for _, row in metro_df.iterrows()]
