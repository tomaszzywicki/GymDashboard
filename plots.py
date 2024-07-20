import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import dash_table
from table_style import *


# Tables

def generate_table_excercises(dataframe):
    # będzie w zależności od setów, repów

    aggregated_data = dataframe.groupby('exercise_title').apply(lambda group: pd.Series({
        'Body part': group['muscle_group'].iloc[0],
        'Sets': group['title'].count(),
        'Reps': group['reps'].sum(),
        'Volume': f"{(group['weight_kg'] * group['reps']).sum()} kg"
    })).reset_index()

    aggregated_data.sort_values(by='Sets', ascending=False, inplace=True)
    aggregated_data.rename(columns={'exercise_title': 'Excercise'}, inplace=True)
    aggregated_data.reset_index(drop=True, inplace=True)
    aggregated_data.index += 1  # Zaczynamy numerację od 1
    aggregated_data.reset_index(inplace=True)
    aggregated_data.rename(columns={'index': 'No'}, inplace=True)
    aggregated_data = aggregated_data.head(5)

    return dash_table.DataTable(
        id='excercise_table',
        columns=[{"name": col, 'id': col} for col in aggregated_data.columns],
        data=aggregated_data.to_dict('records'),
        style_as_list_view=True,
        style_cell_conditional=style_cell_conditional_excercises,
        style_cell=style_cell,
        style_header=style_header
    )


def generate_table_workouts(dataframe):
    def minutes_to_h_min(minutes):
        return f"{(minutes // 60):.0f}h {(minutes % 60):.0f}min"
    

    aggregated_data = dataframe.groupby('title').apply(lambda group: pd.Series({
        'Duration': minutes_to_h_min(group['duration'].iloc[0]),
        'Sets': group['title'].count(),
        'Excercises': group['exercise_title'].nunique(),
        'Volume': f"{(group['weight_kg'] * group['reps']).sum()} kg",
        'Start time': group['start_time'].iloc[0]
    })).reset_index()

    aggregated_data.rename(columns={'title': 'Workout'}, inplace=True)
    aggregated_data.sort_values(by='Start time', ascending=False, inplace=True)
    aggregated_data = aggregated_data.head(5)

    return dash_table.DataTable(
        id='workout_table',
        columns=[{"name": col, 'id': col} for col in aggregated_data.columns if col != 'Start time'],
        data=aggregated_data.to_dict('records'),
        style_as_list_view=True,
        style_cell_conditional=style_cell_conditional_workouts,
        style_cell=style_cell,
        style_header=style_header
    )

# Hour plot

def generate_hour_plot(df):
    minutes = [0] * 24

    def calculate_minutes(row):
        start_time = row['start_time']
        end_time = row['end_time']
        for i in range(start_time.hour, end_time.hour + 1):
            if i == start_time.hour:
                minutes[i] += 60 - start_time.minute if start_time.minute != 0 else 0
            elif i == end_time.hour:
                minutes[i] += end_time.minute
            else:
                minutes[i] += 60

    df.apply(calculate_minutes, axis=1)

    total_minutes = sum(minutes)
    percentage = [(x/total_minutes) for x in minutes]

    fig = go.Figure(data=[go.Bar(
        x = [str(i) for i in range(24)],
        y = percentage
    )])

    fig.update_layout(title_text='Workout Time Distribution throughout the day',
                    xaxis_title='Hour',
                    yaxis_title='Percentage of time spent',
                    plot_bgcolor='#1d232c',
                    paper_bgcolor='#1d232c',
                    font=dict(color='white'))
    
    fig.update_yaxes(tickformat=".0%")
    
    return fig


def generate_day_plot(df):
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    days_count = [0] * 7

    def calculate_days(row):
        days_count[row['start_time'].weekday()] += 1

    df.apply(calculate_days, axis=1)

    total_days = sum(days_count)
    percentage = [(x/total_days) for x in days_count]

    fig = go.Figure(data=[go.Bar(
        x = days,
        y = percentage
    )])

    fig.update_layout(title_text='Workout Days Distribution throughout the week',
                    xaxis_title='Day',
                    yaxis_title='Percentage of days',
                    plot_bgcolor='#1d232c',
                    paper_bgcolor='#1d232c',
                    font=dict(color='white'))

    fig.update_yaxes(tickformat=".0%")

    return fig

# Weight lifted progress plot

def generate_weight_lifted_plot(df, excercise):
    df_excercise = df[df['exercise_title'] == excercise]
    df_grouped = df_excercise.groupby('title')[['weight_kg', 'start_time']].max().reset_index()

    fig = go.Figure(data=go.Scatter(x=df_grouped['start_time'].dt.date, y=df_grouped['weight_kg'], mode='lines+markers'))
    fig.update_layout(title_text=f'Progress of {excercise} over time',
                      xaxis_title='Date',
                      yaxis_title='Max weight lifted (kg)')
    return fig




# Weight plot

def generate_weight_plot(df):
    fig = px.line(df, x='Date', y='Value', labels={'Value' : 'Weight'})
    return fig