import pandas as pd
import plotly.express as px
from jinja2 import Template
 
#import data
data = pd.read_csv('2020_RaceAverageScore_Cleaned.csv')

# create choropleth map for the data
# color will be the column to be color-coded
# locations is the column with sppatial coordinates
fig = px.choropleth(data, 
                    locations='State' ,
                    locationmode="USA-states", 
                    color='Average Score', 
                    scope="usa",
                    range_color=(data['Average Score'].min(), data['Average Score'].max()),
                    color_continuous_scale="Blues",

                    )

fig.update_layout(
    geo = dict(showlakes=False),
    autosize = False,
    margin=dict(l=0, r=0, t=0, b=0),
    #height = 300
    )
 
fig.show()

outputFile = r"index.html"
templateFile = r"template.html"

plotly_jinja_data = {"fig":fig.to_html(full_html=False)}

with open(outputFile, "w", encoding="utf-8") as output_file:
    with open(templateFile) as template_file:
        template = Template(template_file.read())
        output_file.write(template.render(plotly_jinja_data))