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
    hub_addresses = [line.replace("\n", "") + " Amsterdam" for line in lines]

hubs_batches = batch_for_gmaps(hub_addresses)


train_stations = []
with open("data/train_stations.txt") as file:
    lines = file.readlines()
    train_stations = [line.replace("\n", "") for line in lines]
train_stations_batches = batch_for_gmaps(train_stations)


metro_tram_df = pd.read_csv("data/TRAMMETRO_PUNTEN_2022.csv", sep=";")
metro_df = metro_tram_df.loc[metro_tram_df["Modaliteit"] == "Metro"]
tram_df = metro_tram_df.loc[metro_tram_df["Modaliteit"] == "Tram"]

metro_labels = [row["Naam"] for _, row in metro_df.iterrows()]
metro_gmaps_ids = [label + " amsterdam metro station" for label in metro_labels]
metro_gmaps_ids_batches = batch_for_gmaps(metro_gmaps_ids)

shared_mobility_ams_df = pd.read_csv(
    "data/rapportage_2020-09-01-2023-09-30_GM0363 - donkey.csv"
)

# get all the neighbourhood rows from this data
neighbourhoods_df = shared_mobility_ams_df.iloc[5:104]
neighbourhoods_df.set_index("neighbourhood", inplace=True, drop=True)
neighbourhood_labels = list(neighbourhoods_df.index.values)
neighbourhood_batches = batch_for_gmaps(neighbourhood_labels)
