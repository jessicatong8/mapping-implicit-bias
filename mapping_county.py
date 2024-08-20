import pandas as pd
import plotly.express as px
from jinja2 import Template
import json
 
#import data
data = pd.read_csv('2020_RaceAverageScore_fips.csv', dtype={"fips": str})


with open('geojson-counties-fips.json') as response:
     counties = json.load(response)


fig = px.choropleth(data, geojson=counties, locations='fips', color='avgScore',
                    range_color=(0.2,0.3),
                    color_continuous_scale="Blues",
                    scope="usa",
                    labels={'unemp':'unemployment rate'}
                    )
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()