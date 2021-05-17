#!/usr/bin/env python
# coding: utf-8

# In[7]:


import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
import requests


# In[8]:


# Load Data
url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
r= requests.get(url)
json = r.json()
json.keys()


# In[9]:


gamedf = pd.DataFrame(json['events'])
elements_df = pd.DataFrame(json['elements'])
elements_types_df = pd.DataFrame(json['element_types'])
teams_df = pd.DataFrame(json['teams'])


# In[10]:


slim_elements_df = elements_df[['second_name','team','element_type','selected_by_percent','now_cost','minutes','transfers_in','value_season','total_points']]
slim_elements_df['position'] = slim_elements_df.element_type.map(elements_types_df.set_index('id').singular_name)
slim_elements_df['team'] = slim_elements_df.team.map(teams_df.set_index('id').name)
#slim_elements_df.head()
slim_elements_df.head()


# In[12]:


#df = px.data.tips()
# Build App
server = app.server
app = dash.Dash(__name__)
app.layout = html.Div([
    html.H1("Total Points per Player"),
    dcc.Graph(id='graph'),
    html.Label([
        "colorscale",
        dcc.Dropdown(
            id='colorscale-dropdown', clearable=False,
            value='plasma', options=[
                {'label': c, 'value': c}
                for c in px.colors.named_colorscales()
            ])
    ]),
])
# Define callback to update graph
@app.callback(
    Output('graph', 'figure'),
    [Input("colorscale-dropdown", "value")]
)
def update_figure(colorscale):
    return px.scatter(
        slim_elements_df, x="team", y="total_points", size="minutes", color="minutes", hover_data=['second_name'],
        color_continuous_scale=colorscale,
        render_mode="webgl", title="Tips"
    )
# Run app and display result inline in the notebook
if __name__ == '__main__'
    app.run_server(debug=True)

