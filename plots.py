import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import dash_table


# Table

def generate_table(dataframe):
    # będzie w zależności od setów, repów
    df = dataframe.groupby('exercise_title').agg({'exercise_title':'count'}).rename(columns={'exercise_title':'count'}).sort_values(by='count', ascending=False).head(5).reset_index()
    return dash_table.DataTable(
            id = 'exercise_table',
            columns=[{"name": col, 'id': col} for col in df.columns],
            data=df.to_dict('records')
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
    percentage = [(x/total_minutes) * 100 for x in minutes]

    fig = go.Figure(data=[go.Bar(
        x = [str(i) for i in range(24)],
        y = percentage
    )])

    fig.update_layout(title_text='Workout Time Distribution throughout the day',
                    xaxis_title='Hour',
                    yaxis_title='Percentage of time spent')
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
    fig = px.line(df, x='Date', y='Value')
    return fig