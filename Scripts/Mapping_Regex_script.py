
# importing necessary libraries
import pandas as pd
import plotly.express as px

# loading gazetteer data containing place names and coordinates
coordinates_path = "../gazetteers/NER_gazetteer.tsv"
coordinates_df = pd.read_csv(coordinates_path, sep="\t")

# loading the TSV file containing regex frequency counts per place and month
counts_df = pd.read_csv("../Count/ner_counts.tsv", sep="\t")

# filter the data for January 2024
counts_df = counts_df[counts_df["month"] == "2024-01"]

# merging the two dataframes on the common column "asciiname"
merge_df = pd.merge(coordinates_df, counts_df, on="asciiname")
print(merge_df)

# create a static map using frequency (count) as color
fig = px.scatter_mapbox(
    merge_df,
    lat="latitude",
    lon="longitude",
    hover_name="asciiname",
    color="count",
    color_continuous_scale=px.colors.sequential.YlOrRd,
    zoom=1
)
fig.update_layout(mapbox_style="carto-darkmatter")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

# show the static map
fig.show()

# Save the static version of the map as PNG image
fig.write_image("ner_map.png", scale=2)

# create an animated map is not required here since it's only January 2024
# instead, just save the interactive static map as HTML
fig.write_html("ner_map.html")





 





