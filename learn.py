import pandas as pd

df = pd.DataFrame()

labels = ["a", "b", "c", "d"]
labels2 = ["e", "f", "g"]

series1 = pd.Series([1, 2, 3])
series2 = pd.Series([4, 5, 6])


df = pd.concat([df, series1], axis=1)
df = pd.concat([df, series2], axis=1)

df2 = df * 2
df = pd.concat([df, df2], axis=1)

df3 = pd.DataFrame()
df3 = pd.concat([df3, df])
df3 = pd.concat([df3, df])
df.columns = labels
df.index = labels2


df_neigh = pd.read_csv("neighbourhood_data.csv")
