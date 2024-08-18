import plotly.graph_objects as go
import pandas as pd
from jinja2 import Template

df = pd.read_csv('2020_RaceAverageScore.csv')
# x = list(df['State'])

fig = go.Figure(data=go.Choropleth(
    locations=df['State'], # Spatial coordinates
    z = df['Average'].astype(float), # Data to be color-coded
    locationmode = 'USA-states', # set of locations match entries in `locations`
    colorscale = 'Reds',
    marker_line_color='white', # line markers between states
    colorbar_title = "IAT Score",
    zmin=0.19,  # Sets the minimum value of the color scale
    zmax=0.3,  # Sets the maximum value of the color scale
    # hovertemplate =
    # 'State: %{x}', #+
    # # '<br><b>X</b>: %{x}<br>'+
    # # '<b>%{text}</b>',
))

fig.update_layout(
    title_text = '2020 Average Race IAT Scores by State',
    geo = dict(
        scope='usa',
        projection=go.layout.geo.Projection(type = 'albers usa'),
        showlakes=False,)
)

fig.show()

jjinja = {"fig":fig.to_html(full_html=False)}