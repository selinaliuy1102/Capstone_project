# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
# replacing blank spaces with '_' 
spacex_df.columns =[column.replace(" ", "_") for column in spacex_df.columns]

#max_payload = spacex_df['Payload_Mass_(kg)'].max()
#min_payload = spacex_df['Payload_Mass_(kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                  dcc.Dropdown(id='site-dropdown',
                                                options=[
                                                    {'label': 'All Sites', 'value': 'ALL'},
                                                    {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                    {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                                    {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                    {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                                ],
                                                value='ALL',
                                                placeholder="place holder here",
                                                searchable=True
                                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={0: '0',
                                                    100: '100'},
                                                #value=[min_payload, max_payload]),
                                                value=[0, 10000]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(spacex_df, values='class', 
        names='Launch_Site', 
        title='Total success launches by site ')
        return fig
    else:
        # return the outcomes piechart for a selected site
        #filtered_df = spacex_df.query('Launch_Site == ' +'"'+ entered_site +'"')
        #filtered_df = spacex_df.query('Launch_Site == "CCAFS LC-40"')
        # fig = px.pie(filtered_df, values='class', 
        #names='class', 
        #title='Total sucess launches fro site :'+entered_site)
        #title=filtered_df.shape[0])

     # return the outcomes piechart for a selected site
        filtered_df = spacex_df[spacex_df['Launch_Site'] == entered_site].groupby(['Launch_Site', 'class']).size().reset_index(name='class_count')
        fig = px.pie(filtered_df, 
                    values='class_count', 
                    names='class_count', 
                    title='Launch site:'+ entered_site)
        return fig




# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'),
              Input(component_id='payload-slider', component_property='value'))
def get_scatter_chart(entered_site,entered_payload):
    #filtered_df = spacex_df
    if entered_site == 'ALL':
        fig1 = px.scatter(spacex_df,x="Payload_Mass_(kg)", y="class", color="Booster_Version_Category",
        title='Corralation between Payload and success for all sites')
        return fig1
    else:
        # return the outcomes piechart for a selected site
        return


# Run the app
if __name__ == '__main__':
    app.run_server()


