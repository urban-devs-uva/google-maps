import googlemaps
import pandas as pd
import itertools

gmaps = googlemaps.Client(key="AIzaSyAyZ5x-tm9dSJc2Xk4iS5A1Amh2jGQi8DM")

def batch_for_gmaps(list):
    gmaps_matrix_size_limit = 10
    if len(list) <= gmaps_matrix_size_limit:
        return list
    else:
        return itertools.batched(list, gmaps_matrix_size_limit)

hub_addresses = []
with open("data/mobility_hub_addresses.txt") as file:
    lines = file.readlines()
    hub_addresses = [f"{line.replace("\n", "")} Amsterdam" for line in lines]
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

df_hubs_data = pd.DataFrame({"Mobility hub": hub_addresses})



def get_origin_dest_matrix(origins_batches, destinations_batches, mode):
    origin_dest_matrix = pd.DataFrame()
    
    for origin_batch in itertools.tee(origins_batches):
        # matrix for the origin batch and all their destinations
        origin_batch_matrix = pd.DataFrame()
        print("foo")

        for destinations_batch in destinations_batches:
            # 10x10 matrix for the origin batch and the destination batch
            batch_batch_matrix = pd.DataFrame()
            print("bar")

            gmaps_batch = gmaps.distance_matrix(
                list(origin_batch), list(destinations_batch), mode=mode
            )

            for row in gmaps_batch["rows"]:
                values = pd.Series([
                    element["distance"]["value"] for element in row["elements"]
                ])
                batch_batch_matrix = pd.concat([batch_batch_matrix, values], axis=1)

            origin_batch_matrix = pd.concat([origin_batch_matrix, batch_batch_matrix])
        origin_dest_matrix = pd.concat([origin_dest_matrix, origin_batch_matrix], axis=1)

    return origin_dest_matrix

get_origin_dest_matrix(hubs_batches, train_stations_batches, "walking").info()
