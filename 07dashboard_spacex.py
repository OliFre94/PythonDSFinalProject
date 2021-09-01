# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

#print(spacex_df["Booster Version"].head())


x = list(range(0,10000,1000))
rslider_marks = {}
for i in x:
    rslider_marks[i] = str(i)

#figu = px.scatter(spacex_df, x = "Payload Mass (kg)", y = "class", color = "Booster Version")

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(id='dropdown1',
                                    value = 'All',
                                    options = [
                                        {'label':'CCAFS LC-40','value':'CCAFS LC-40'},
                                        {'label':'VAFB SLC-4E','value':'VAFB SLC-4E'},
                                        {'label':'CCAFS SLC-40','value':'CCAFS SLC-40'},
                                        {'label':'KSC LC-39A','value':'KSC LC-39A'},
                                        {'label':'All', 'value':'All'}
                                        ],
                                        placeholder = 'Select a Launch Site',
                                        searchable = True
                                    ),
                                html.Br(),


                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart', figure = {})),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='slider1',
                                    min = 0,
                                    max = 10000,
                                    step = 1000,
                                    marks = rslider_marks,
                                    #marks = {0: '0', 5000: '5000', 10000: '10000'},
                                    value = [0, 10000]),
                                html.Br(),

                                html.H1(id = 'output_container', children =[]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart', figure = {})),
                                ])




# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

@app.callback(
    [Output(component_id = 'success-pie-chart', component_property = 'figure')],
    [Input(component_id = 'dropdown1', component_property = 'value')]
    )


def update_graph(opt_slc):



    if opt_slc == 'All':
        df = spacex_df
        df = df[df["class"] == 1]
        fig = px.pie(df, values = 'class', names = 'Launch Site')
    else:
        df = spacex_df
        df = df[df["Launch Site"] == opt_slc]
        fig = px.pie(df, values = 'class', names = 'Mission Outcome')

    return [fig]

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output

@app.callback(
    [Output(component_id = 'success-payload-scatter-chart', component_property = 'figure')],
    [Input(component_id = 'slider1', component_property = 'value')],
    [Input(component_id = 'dropdown1', component_property = 'value')]
    )

def update_graph2(opt_slc_slide, opt_slc_drop):
    
    dff = spacex_df
    dff = dff[dff["Payload Mass (kg)"] >= opt_slc_slide[0]]
    dff = dff[dff["Payload Mass (kg)"] <= opt_slc_slide[1]]

    if opt_slc_drop == "All":
        fig2 = px.scatter(dff, x = "Payload Mass (kg)", y = "class", color = 'Booster Version')
    else:
        dff = dff[dff["Launch Site"] == opt_slc_drop]
        fig2 = px.scatter(dff, x = "Payload Mass (kg)", y = "class", color = 'Booster Version')

    return [fig2]




# Run the app
if __name__ == '__main__':
    app.run_server(debug = True)
