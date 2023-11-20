import googlemaps
import pandas as pd
import data

gmaps = googlemaps.Client(key="AIzaSyAyZ5x-tm9dSJc2Xk4iS5A1Amh2jGQi8DM")


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
            print(gmaps_batch["destination_addresses"])
            for row in gmaps_batch["rows"]:
                try:
                    values = pd.Series(
                        [element["distance"]["value"] for element in row["elements"]]
                    )
                    print(gmaps_batch["rows"].index(row))
                except:
                    print("index of row: ")
                    print(gmaps_batch["rows"].index(row))

                batch_batch_matrix = pd.concat([batch_batch_matrix, values], axis=1)

            origin_batch_matrix = pd.concat([origin_batch_matrix, batch_batch_matrix])
        origin_dest_matrix = pd.concat(
            [origin_dest_matrix, origin_batch_matrix], axis=1
        )

    origin_dest_matrix.columns = origins
    origin_dest_matrix.index = destinations

    return origin_dest_matrix


def get_nearest_destinations(distance_matrix: pd.DataFrame, name_col, distance_col):
    nearest_dest_name = []
    nearest_dest_distance = []
    for _, destination_series in distance_matrix.items():
        nearest_dest = destination_series.nsmallest(1)
        nearest_dest_name.append(nearest_dest.index[0])
        nearest_dest_distance.append(nearest_dest.iloc[0])
    return pd.DataFrame(
        {name_col: nearest_dest_name, distance_col: nearest_dest_distance}
    )


def add_nearest_destination_to_origins_df(
    df, destinations, destinations_batches, name_col: str, distance_col: str, mode: str
):
    origins = data.hub_addresses
    origins_batches = data.hubs_batches

    origin_dest_matrix = get_origin_dest_matrix(
        origins, origins_batches, destinations, destinations_batches, mode
    )
    nearest_destinations = get_nearest_destinations(
        origin_dest_matrix, f"{name_col}_{mode}", f"{distance_col}_{mode}"
    )
    return pd.concat([df, nearest_destinations], axis=1)
