import pandas as pd
import data
import data_func

df_hub_data = pd.DataFrame({"mobility_hub": data.hub_addresses})

modes_of_interest = ["walking", "bicycling"]

for mode in modes_of_interest:
    df_hub_data = data_func.add_nearest_destination_to_hubs(
        df_hub_data,
        data.train_stations,
        data.train_stations_batches,
        "nearest_train_station_name",
        "nearest_train_station_distance",
        mode,
    )

    df_hub_data = data_func.add_nearest_destination_to_hubs()

df_hub_data.to_csv("data.csv")

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
