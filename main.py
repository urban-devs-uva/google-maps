import googlemaps
import pandas as pd
import itertools

gmaps = googlemaps.Client(key="AIzaSyAyZ5x-tm9dSJc2Xk4iS5A1Amh2jGQi8DM")
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


def get_origin_dest_matrix(
    origins,
    origins_batches,
    destinations,
    destinations_batches,
    mode,
):
    origin_dest_matrix = pd.DataFrame()

    for origin_batch in origins_batches:
        # matrix for the origin batch and all their destinations
        origin_batch_matrix = pd.DataFrame()

        for destinations_batch in destinations_batches:
            # 10x10 matrix for the origin batch and the destination batch
            batch_batch_matrix = pd.DataFrame()

            gmaps_batch = gmaps.distance_matrix(
                origin_batch, destinations_batch, mode=mode
            )

            for row in gmaps_batch["rows"]:
                values = pd.Series(
                    [element["distance"]["value"] for element in row["elements"]]
                )
                batch_batch_matrix = pd.concat([batch_batch_matrix, values], axis=1)

            origin_batch_matrix = pd.concat([origin_batch_matrix, batch_batch_matrix])
        origin_dest_matrix = pd.concat(
            [origin_dest_matrix, origin_batch_matrix], axis=1
        )

    origin_dest_matrix.columns = origins
    origin_dest_matrix.index = destinations
    return origin_dest_matrix


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
