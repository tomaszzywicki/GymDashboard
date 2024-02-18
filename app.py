from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
from datetime import date
from plots import *
from data_cleanup import *


df_excercise = pd.read_csv('workout_data.csv')
df_weight = pd.read_csv('weight_data.csv')

df_excercise = clean_workout_data(df_excercise)
df_weight = clean_weight_data(df_weight)

app = Dash(__name__)

colors = {
    'background' : '#111111',
    'text' : '#7FDBFF'
}


app.layout = html.Div([
    html.Div(style={'backgroundColor': "yellow",
                    'textAlign': 'center'},
        className='app-header',
        children=[
            html.H1('Gym dashboard'),
                dcc.Tabs(id="tabs", value='tab-1', children=[
                    dcc.Tab(label='Tab one', value='tab-1'),
                    dcc.Tab(label='Tab two', value='tab-2'),
    
                ])
        ],
    ),

    html.Div(id='tabs-content'),
])


@callback(Output('tabs-content', 'children'),
          Input('tabs', 'value'))
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            html.H2('Top 5 popular excercises'),
            html.Div([
                generate_table(df_excercise),
                dcc.Graph(figure=generate_hour_plot(df_excercise)),
                dcc.Graph(figure=generate_weight_plot(df_weight))
            ])
       ])
                         
    elif tab == 'tab-2':
        return html.Div([
            html.H3('Tab content 2'),
            html.H3('Select muscle group'),
            dcc.Dropdown(['Chest', 'Back', 'Arms', 'Legs'],
                         multi=False),
            html.H3('Select excercise'),
            dcc.Dropdown(['Dumbell bench press', 'Chest cable fly'],
                         multi=False),
            dcc.Graph(figure=generate_weight_lifted_plot(df_excercise, 'Incline Bench Press (Dumbbell)'))
        ])





if __name__ == '__main__':
    app.run(debug=True)

