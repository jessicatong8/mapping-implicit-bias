import pandas as pd
import plotly.express as px
from jinja2 import Template
import json
 
#import data
data = pd.read_csv('data/2020_RaceAverageScore_metro.csv', dtype={"metroNo": str})


with open('geojson/us-metro-area.json') as response:
     metroAreas = json.load(response)
#print(metroAreas["features"][2]["properties"])

# print(data['metroNo'])  # Inspect the metroNo values
# print([feature['properties']['GEOID'] for feature in metroAreas['features']])  # Check the ids in GeoJSON
# ids = [feature['properties']['GEOID'] for feature in metroAreas['features']]

fig = px.choropleth(data, geojson=metroAreas, locations='metroNo', color='avgScore',
                    range_color=(0.2,0.3),
                    color_continuous_scale="Darkmint",
                    scope="usa",
                    labels={'unemp':'unemployment rate'}
                    )
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

# fig.update_traces(marker_line_color='gray',  # Border color
#                   marker_line_width=0.5)        # Border width

fig.show()


# outputFile = r"index-metro.html"
# templateFile = r"template.html"

# plotly_jinja_data = {"fig":fig.to_html(full_html=False)}

# with open(outputFile, "w", encoding="utf-8") as output_file:
#     with open(templateFile) as template_file:
#         template = Template(template_file.read())
#         output_file.write(template.render(plotly_jinja_data))