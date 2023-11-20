import pandas as pd
import data
import distance_matrix

df_hub_data = pd.DataFrame({"mobility_hub": data.hub_addresses})
df_neighbourhood_data = pd.DataFrame({"neighbourhood": data.neighbourhood_labels})

modes_of_interest = ["walking", "bicycling"]
for mode in modes_of_interest:
    df_hub_data = distance_matrix.add_nearest_destination_to_origins_df(
        df_hub_data,
        data.train_stations,
        data.train_stations_batches,
        "nearest_train_station_name",
        "nearest_train_station_distance",
        mode,
    )

    df_hub_data = distance_matrix.add_nearest_destination_to_origins_df(
        df_hub_data,
        data.metro_labels,
        data.metro_gmaps_ids_batches,
        "nearest_metro_station_name",
        "nearest_metro_station_distance",
        mode,
    )


df_hub_data.to_csv("hub_data.csv")
df_neighbourhood_data.to_csv("neighbourhood_data.csv")

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
