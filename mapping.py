import plotly.graph_objects as go

import pandas as pd
df = pd.read_csv('2020_RaceAverageScore.csv')

fig = go.Figure(data=go.Choropleth(
    locations=df['State'], # Spatial coordinates
    z = df['Average'].astype(float), # Data to be color-coded
    locationmode = 'USA-states', # set of locations match entries in `locations`
    colorscale = 'Reds',
    colorbar_title = "IAT Score",
    zmin=0.19,  # Sets the minimum value of the color scale
    zmax=0.3,  # Sets the maximum value of the color scale
))

fig.update_layout(
    title_text = '2020 Average Race IAT Scores by State',
    geo_scope='usa', # limit map scope to USA
)

fig.show()