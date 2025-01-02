import pandas as pd
import plotly.express as px
from jinja2 import Template
import json
 
#import data
data = pd.read_csv('data/2020_RaceAverageScore_County.csv', dtype={"fips": str})
data = data.loc[data['count '] >= 20] 


with open('geojson/us-counties.json') as response:
     counties = json.load(response)
#print(counties["features"][2]["properties"])

fig = px.choropleth(data, geojson=counties, locations='fips  ', color='avgScore',
                    #range_color=(0.2,0.3),
                    color_continuous_scale="Darkmint",
                    scope="usa",
                    )
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

fig.update_traces(marker_line_color='gray',  # Border color
                  marker_line_width=0.5)        # Border width

fig.show()


outputFile = r"map_counties.html"
templateFile = r"template.html"

plotly_jinja_data = {"fig":fig.to_html(full_html=False)}

with open(outputFile, "w", encoding="utf-8") as output_file:
    with open(templateFile) as template_file:
        template = Template(template_file.read())
        output_file.write(template.render(plotly_jinja_data))