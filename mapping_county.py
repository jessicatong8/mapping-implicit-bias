import pandas as pd
import plotly.express as px
from jinja2 import Template
import json
 
#import data
data = pd.read_csv('2020_RaceAverageScore_County.csv')


with open('geojson-counties-fips.json') as response:
     counties = json.load(response)

# print(counties['features'][0])

fig = px.choropleth(data, 
                    geojson=counties, 
                    #featureidkey="properties.COUNTY",
                    locations='fips', 
                    color='average',
                    color_continuous_scale="Viridis",
                    #range_color=(0, 12),
                    scope="usa",
                    #labels={'unemp':'unemployment rate'}
                    )
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()