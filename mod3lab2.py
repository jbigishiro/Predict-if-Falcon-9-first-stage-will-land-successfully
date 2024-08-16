# Build a Dashboard Application with Plotly Dash

# Import required libraries
import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                               html.Div(dcc.Dropdown(id='site-dropdown', options=[{'label': 'All Sites', 'value': 'ALL'},
                               {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'}, {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}, 
                               {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'}, {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}],
                               value='ALL', placeholder='place holder here', searchable=True)),

                                html.Br(), 
                           
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                
                                # TASK 3: Add a slider to select payload range
                                html.Div(dcc.RangeSlider(id='payload-slider', min=0, max=10000, step=1000,
                                                         value=[min_payload, max_payload])),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart'))
                                ]
                    )

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        df1 = filtered_df[filtered_df['class'] == 1 ]
        df1 = df1.groupby('Launch Site')['class'].count().reset_index()
        fig = px.pie(df1, values='class', names='Launch Site', title='Total Success Launch By Site')
        return fig
    else:
        df2 = filtered_df[filtered_df["Launch Site"] == entered_site]
        df2 = df2[['Launch Site', 'class']].value_counts().reset_index()
        fig = px.pie(df2, values='count', names='class', title=f'Total Success for the site {entered_site}')
        return fig



# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output

@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'),
              Input(component_id='payload-slider', component_property='value'))
def get_pie_scatter(entered_site, entered_slide_range):
    filtered_df = spacex_df
    min, max = entered_slide_range
    if entered_site == 'ALL':
        df3 = filtered_df[(filtered_df['Payload Mass (kg)'] >= min) & (filtered_df['Payload Mass (kg)'] <= max ) ]
        fig = px.scatter(df3, x='Payload Mass (kg)', y='class', color='Launch Site', title='Correlation between Payload and Success for all Sites')
        return fig
    else:
        df4 = filtered_df[filtered_df["Launch Site"] == entered_site]
        df4 = df4[(df4['Payload Mass (kg)'] >= min) & (df4['Payload Mass (kg)'] <= max ) ]
        fig = px.scatter(df4, x='Payload Mass (kg)', y='class', color='Launch Site', title=f'Correlation between Payload and Success for the site {entered_site}')
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()