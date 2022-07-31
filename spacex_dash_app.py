# Import required libraries
import pandas as pd
import dash
# import dash_html_components as html
from dash import html
# import dash_core_components as dcc
from dash import dcc

from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

options = [{'label': 'All Sites', 'value': 'ALL'}] + [{'label': row['Launch Site'], 'value': row['Launch Site']} for
                                                      i, row in spacex_df[['Launch Site']].groupby(['Launch Site'],
                                                                                                   as_index=False).first().iterrows()]
menu_sites = dcc.Dropdown(id='site-dropdown',
                          options=options,
                          value='ALL',
                          placeholder='Select a Launch Site',
                          searchable=True,
                          style={'width': '80%', 'padding': '3px', 'text-align-last': 'center', 'font-size': '20px'})

min0 = 0
max0 = 10000
import numpy as np

slider = dcc.RangeSlider(id='payload-slider',
                         min=min0, max=max0, step=1000,
                         marks={int(el): f'{el:g}' for el in np.linspace(min0, max0, 5)},
                         value=[min_payload, max_payload])
# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                menu_sites,
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                slider,
                                # TASK 3: Add a slider to select payload range
                                # dcc.RangeSlider(id='payload-slider',...)

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])


# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    #    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(spacex_df, values='class',
                     names='Launch Site',
                     title='Total success launches by site')
        return fig
    else:
        # return the outcomes piechart for a selected site
        fig = px.pie(spacex_df[spacex_df['Launch Site'] == entered_site],
                     names='class',
                     title=f'Total success launches for site {entered_site}')
        return fig


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id='payload-slider', component_property='value')],
              )
def get_graph(site, load):
    print(site, load)
    val1, val2 = load
    df = spacex_df[(val1 <= spacex_df['Payload Mass (kg)'])
                   & (spacex_df['Payload Mass (kg)'] <= val2)]
    if site != 'ALL':
        df = df[df['Launch Site'] == site]

    fig = px.scatter(df, x='Payload Mass (kg)', y='class',
                     color="Booster Version Category")

    #    x = line_data['Month'], y = line_data['ArrDelay'], mode = 'lines', marker = dict(color='green')))
    #    fig.update_layout(title='Month vs Average Flight Delay Time', xaxis_title='Month', yaxis_title='ArrDelay')
    #     fig = px.pie(spacex_df, values='class',
    #                  names='Launch Site',
    #                  title='Total success launches by site')
    return fig


# Run the app
if __name__ == '__main__':
    app.run_server()
