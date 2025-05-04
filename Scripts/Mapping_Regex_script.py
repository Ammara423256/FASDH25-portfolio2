import pandas as pd
import plotly.express as px


#loading gazeeteer data into dataframe
coordinates_path="../gazetteers/geonames_gaza_selection.tsv"
coordinates_df=pd.read_csv(coordinates_path, sep="\t")

#loading frequency tsv
counts_df=pd.read_csv("regex_count.tsv", sep="\t")

#merging the two tsv
merge_df=pd.merge(coordinates_df, counts_df, on="asciiname")
print(merge_df)

## Display the merged dataframe (using color to represent frequency)
fig = px.scatter_map(merge_df, lat="latitude", lon="longitude", hover_name="asciiname", color="count", color_continuous_scale=px.colors.sequential.YlOrRd)
fig.update_layout(map_style="carto-darkmatter-nolabels")
fig.show()

# configures the map background:
fig.update_geos(
    projection_type="natural earth",
    fitbounds="locations",
    showcoastlines=True, coastlinecolor="RebeccaPurple",
    showland=True, landcolor="Green",
    showocean=True, oceancolor="LightBlue",
    showlakes=False, lakecolor="Blue",
    showrivers=True, rivercolor="Blue",
    showcountries=False, countrycolor="Brown"
)
fig.show()

# Saves the map as a static image (PNG)
fig.write_image("regex_map.png", scale=2)

# Display the frequencies on a frame map per month:
fig = px.scatter_geo(merge_df, lat="latitude", lon="longitude", size="count", hover_name="asciiname", animation_frame="month", color="count", color_continuous_scale=px.colors.sequential.YlOrRd,  projection="natural earth")


fig.update_layout(
    title="Regex Mentions Over Time",
    title_font_size=22,
    geo=dict(
        showland=True, landcolor="lightgreen",
        showocean=True, oceancolor="lightblue",
        showrivers=True, rivercolor="blue"
        )
    )

fig.show()


# saves the interactive map as html
fig.write_html("regex_map.html")




 





