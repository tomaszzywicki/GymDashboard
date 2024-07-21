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

workouts_count = df_excercise['title'].nunique()
total_time = df_excercise.drop_duplicates(subset=['title', 'duration'])['duration'].sum()
total_time = f"{(total_time // 60):.0f}h {(total_time % 60):.0f}min"
total_volume = (df_excercise['weight_kg'] * df_excercise['reps']).sum()
total_sets = df_excercise['title'].count()
total_reps = int(df_excercise['reps'].sum())


app.layout = html.Div([
    html.Div(className='app-header',
        children=[
            html.H1('Gym dashboard'),
                dcc.Tabs(id="tabs", value='tab-1', children=[
                    dcc.Tab(label='Statistics', value='tab-1'),
                    dcc.Tab(label='Strength progress', value='tab-2'),
    
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
            html.Div(className='tables-container', children=[
                html.Div(className='table', id="table1", children=[
                    html.H2('Last 5 workouts'),
                    generate_table_workouts(df_excercise)
                ]),
                html.Div(className='table', id="table2", children=[
                    html.H2('Top 5 popular excercises'),
                    generate_table_excercises(df_excercise)
                ])
            ]),
            html.Div(className='time-plots-container', children=[
                html.Div(className='time-plot', id="time-plot1", children=[
                    html.H2(className='time-plot-title', children=['Workouts per hour']),
                    dcc.Graph(figure=generate_hour_plot(df_excercise))
                ]),
                html.Div(className='time-plot', id="time-plot2", children=[
                    html.H2(className='time-plot-title', children=['Workouts per day']),
                    dcc.Graph(figure=generate_day_plot(df_excercise))
                ])
            ]),
            html.Div(className='stats-container', children=[
                html.Div(className='stats-title', children=[
                    html.H1('Overall stats')
                ]),
                html.Div(className='stat-row', id="stat-row-1", children=[
                    html.Div(className='stat-item', id="stat-item-1", children=[
                        html.H2(className='stat-title', children=['Total workouts']),
                        html.H3(className='stat-text', children=[f'{workouts_count}'])
                    ]),
                    html.Div(className='stat-item', id="stat-item-2", children=[
                        html.H2(className='stat-title', children=['Total time']),
                        html.H3(className='stat-text', children=[f'{total_time}'])
                    ]),
                    html.Div(className='stat-item', id="stat-item-3", children=[
                        html.H2(className='stat-title', children=['Volume lifted']),
                        html.H3(className='stat-text', children=[f'{total_volume} kg'])
                    ])
                ]),
                html.Div(className='stat-row', id="stat-row-1", children=[
                    html.Div(className='stat-item', id="stat-item-1", children=[
                        html.H2(className='stat-title', children=['Total sets']),
                        html.H3(className='stat-text', children=[f'{total_sets}'])
                    ]),
                    html.Div(className='stat-item', id="stat-item-2", children=[
                        html.H2(className='stat-title', children=['Total reps']),
                        html.H3(className='stat-text', children=[f'{total_reps}'])
                    ]),
                    html.Div(className='stat-item', id="stat-item-3", children=[
                        html.H2(className='stat-title', children=['Todo']),
                        html.H3(className='stat-text', children=['todo'])
                    ])
                ])

            ])
       ])
                         
    elif tab == 'tab-2':
        return html.Div([
            html.Div(className='tab-2-container', children=[
                html.Div(className='tab-2-first-row', children=[
                    html.Div(className='button-container', children=[
                        html.Div(className='select-container', children=[
                            html.Div(className='select-muscle-1', children=[
                                html.H3('Select muscle group 1'),
                                dcc.Dropdown(['Chest', 'Back', 'Arms', 'Legs'],
                                            multi=False),
                                html.H3('Select excercise 2'),
                                dcc.Dropdown(['Dumbell bench press', 'Chest cable fly'],
                                            multi=False),
                                html.H3('Select y-axis 1'),
                                dcc.Dropdown(['Max weight', 'Max volume'])
                            ]),
                            html.Div(className='select-muscle-2', children=[
                                html.H3('Select muscle group 2'),
                                dcc.Dropdown(['Chest', 'Back', 'Arms', 'Legs'],
                                            multi=False),
                                html.H3('Select excercise 2'),
                                dcc.Dropdown(['Dumbell bench press', 'Chest cable fly'],
                                            multi=False),
                                html.H3('Select y-axis 2'),
                                dcc.Dropdown(['Max weight', 'Max volume'])
                            ]),
                    ]),
                    html.Div(className='date-picker-container', children=[
                        html.H3(className='h3-date', children=['Select date range']),
                        dcc.DatePickerRange(
                            id='date-picker',
                            min_date_allowed=date(2019, 12, 25),
                            max_date_allowed=date.today(),
                            initial_visible_month=date.today(),
                            start_date=date(2022, 10, 1),
                            end_date=date.today()
                        )
                        
                    ])

                    ]),
                    html.Div(className='bodyweight-plot', children=[
                        html.H2('Bodyweight progress'),
                        dcc.Graph(figure=generate_weight_plot(df_weight))
                    ])
                ]),
                html.Div(className='tab-2-second-row', children=[
                    html.Div(className='excercise-plot', children=[
                        html.H2(className='excersice-plot-title', children=[f'excercise 1 progress'])

                    ]),
                    html.Div(className='excercise-plot', children=[
                        html.H2(className='excersice-plot-title', children=[f'excercise 2 progress'])

                    ])
                ])
            ]),
        ])





if __name__ == '__main__':
    app.run(debug=True)

