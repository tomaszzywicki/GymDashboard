from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
from datetime import date
from plots import *
from data_cleanup import *


df_exercise = pd.read_csv('workout_data.csv')
df_weight = pd.read_csv('weight_data.csv')

df_exercise = clean_workout_data(df_exercise)
df_weight = clean_weight_data(df_weight)

app = Dash(__name__)

app.config.suppress_callback_exceptions = True

workouts_count = df_exercise['title'].nunique()
total_time = df_exercise.drop_duplicates(subset=['title', 'duration'])['duration'].sum()
total_time = f"{(total_time // 60):.0f}h {(total_time % 60):.0f}min"
total_volume = (df_exercise['weight_kg'] * df_exercise['reps']).sum()
total_sets = df_exercise['title'].count()
total_reps = int(df_exercise['reps'].sum())

muscle_groups = df_exercise['muscle_group'].unique().tolist()


app.layout = html.Div([
    html.Div(className='app-header',
        children=[
            html.H1('Gym dashboard'),
                dcc.Tabs(id="tabs", value='tab-2', children=[
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
                    generate_table_workouts(df_exercise)
                ]),
                html.Div(className='table', id="table2", children=[
                    html.H2('Top 5 popular exercises'),
                    generate_table_exercises(df_exercise)
                ])
            ]),
            html.Div(className='time-plots-container', children=[
                html.Div(className='time-plot', id="time-plot1", children=[
                    html.H2(className='time-plot-title', children=['Workouts per hour']),
                    dcc.Graph(figure=generate_hour_plot(df_exercise))
                ]),
                html.Div(className='time-plot', id="time-plot2", children=[
                    html.H2(className='time-plot-title', children=['Workouts per day']),
                    dcc.Graph(figure=generate_day_plot(df_exercise))
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
        muscle_groups = df_exercise['muscle_group'].unique().tolist()
        muscle_groups = [{'label': i, 'value': i} for i in muscle_groups if pd.notna(i)]
        y_axis_options = ['Max weight', 'Max set volume', 'Session volume', 'Session reps']
        return html.Div([
            html.Div(className='tab-2-container', children=[
                html.Div(className='tab-2-first-row', children=[
                    html.Div(className='button-container', children=[
                        html.Div(className='select-container', children=[
                            html.Div(className='select-muscle', id='select-muscle-1', children=[
                                html.H3('Select muscle group 1'),
                                dcc.Dropdown(id='muscle-group-dropdown-1', 
                                             options=muscle_groups,
                                             multi=False,
                                             value=None),
                                html.H3('Select exercise 2'),
                                dcc.Dropdown(id='exercise-dropdown-1', 
                                             options=[], ### TODO
                                             multi=False,
                                             value=None),
                                html.H3('Select y-axis 1'),
                                dcc.Dropdown(id='y-axis-dropdown-1',
                                             options=y_axis_options)
                            ]),

                            html.Div(className='select-muscle', id='select-muscle-2', children=[
                                html.H3('Select muscle group 2'),
                                dcc.Dropdown(id='muscle-group-dropdown-2',
                                             options=muscle_groups,
                                             multi=False,
                                             value=None),
                                html.H3('Select exercise 2'),
                                dcc.Dropdown(id='exercise-dropdown-2',
                                             options=['todo'], ### TODO
                                             multi=False,
                                             value=None),
                                html.H3('Select y-axis 2'),
                                dcc.Dropdown(id='y-axis-dropdown-2',
                                             options=y_axis_options,
                                             multi=True,
                                            #  value=None) idk czy tak czy na odwrót
                                )
                            ])
                    ]),
                    html.Div(className='date-picker-container', children=[
                        html.H3(className='h3-date', children=['Select date range']),
                        dcc.DatePickerRange(
                            id='date-picker',
                            min_date_allowed=date(2019, 12, 25),
                            max_date_allowed=date(2100, 1, 1),
                            initial_visible_month=date.today(),
                            start_date=date(2022, 10, 1),
                            end_date=date.today()
                        )
                        
                    ])

                    ]),
                    html.Div(className='bodyweight-plot-container', children=[
                        html.H2(className='bodyweight-plot-title', children=['Bodyweight progress']),
                        dcc.Graph(id='bodyweight-plot', figure=generate_weight_plot(df_weight))
                    ])
                ]),
                html.Div(className='tab-2-second-row', children=[

                    html.Div(className='exercise-plot-container', children=[
                        html.Div(className='exercise-plot', children=[
                            html.H2(className='exercise-plot-title', children=[f'exercise 1 progress']),
                            dcc.Graph(id='exercise-plot-1', className='exercise-plot', figure=generate_weight_lifted_plot(df_exercise, 'Incline Bench Press (Dumbbell)'))
                        ])
                    ]),
                    html.Div(className='exercise-plot-container', children=[
                        html.Div(className='exercise-plot', children=[
                            html.H2(className='exercise-plot-title', children=[f'exercise 2 progress']),
                            dcc.Graph(className='exercise-plot', id='exercise-plot-2', figure=generate_weight_lifted_plot(df_exercise, 'Triceps Pushdown'))
                        ])
                    ])
                ])
            ]),
        ])

@app.callback(
    Output('exercise-dropdown-1', 'options'),
    Input('muscle-group-dropdown-1', 'value'),
)
def update_exercise_dropdown1(muscle_group):
    return [{'label': i, 'value': i} for i in df_exercise[df_exercise['muscle_group'] == muscle_group]['exercise_title'].unique()]

@app.callback(
    Output('exercise-dropdown-2', 'options'),
    Input('muscle-group-dropdown-2', 'value'),
)
def update_exercise_dropdown2(muscle_group):
    return [{'label': i, 'value': i} for i in df_exercise[df_exercise['muscle_group'] == muscle_group]['exercise_title'].unique()]

@app.callback(
    Output('bodyweight-plot', 'figure'),
    [Input('date-picker', 'start_date'), Input('date-picker', 'end_date')] 
)
def update_weight_plot(start_date, end_date):
    filtered_df = df_weight[(df_weight['Date'] >= start_date) & (df_weight['Date'] <= end_date)]
    fig = generate_weight_plot(filtered_df)
    return fig


if __name__ == '__main__':
    app.run(debug=True)

