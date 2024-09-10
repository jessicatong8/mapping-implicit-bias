import pandas as pd
import plotly.express as px
from jinja2 import Template
import json
 
#import data
data = pd.read_csv('data/2020_RaceAverageScore_metro.csv', dtype={"metroNo": str})


with open('geojson/metro-area-github-2021.json') as response:
     metros = json.load(response)
#print(geojson["features"][2]["properties"])

# print(data['metroNo'])  # Inspect the metroNo values
# print([feature['properties']['GEOID'] for feature in geojson['features']])  # Check the ids in GeoJSON
# ids = [feature['properties']['GEOID'] for feature in geojson['features']]



# # Inspect the metroNo values
# print(data['metroNo'])

# # Inspect the GEOID values
# print([feature['properties']['GEOID'] for feature in geojson['features']])

# # Modify the metroNo values to match the GEOID values
# # Assuming the GEOID values are in the format 'XXXXX' and the metroNo values are in the format 'XXXXX'
# data['metroNo'] = data['metroNo'].str.zfill(5)

# # Verify the modification
# print(data['metroNo'])



fig = px.choropleth(data, geojson=metros, locations='metroNo', color='avgScore',
                    range_color=(0.2,0.3),
                    color_continuous_scale="Darkmint",
                    scope="usa",
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