import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import dash_table


# Tables

def generate_table_excercises(dataframe):
    # będzie w zależności od setów, repów

    aggregated_data = dataframe.groupby('exercise_title').apply(lambda group: pd.Series({
        'Body part': group['muscle_group'].iloc[0],
        'Sets': group['title'].count(),
        'Reps': group['reps'].sum(),
        'Volume': (group['weight_kg'] * group['reps']).sum()
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
        data=aggregated_data.to_dict('records')
    )


def generate_table_workouts(dataframe):
    def minutes_to_h_min(minutes):
        return f"{(minutes // 60):.0f}h {(minutes % 60):.0f}min"
    
    aggregated_data = dataframe.groupby('title').apply(lambda group: pd.Series({
        'Duration': minutes_to_h_min(group['duration'].iloc[0]),
        'Volume': f"{(group['weight_kg'] * group['reps']).sum()} kg",
        'Excercises': group['exercise_title'].nunique(),
        'Sets': group['title'].count()
    })).reset_index()

    aggregated_data.sort_values(by='title', ascending=False, inplace=True)
    aggregated_data.rename(columns={'title': 'Workout'}, inplace=True)

    return dash_table.DataTable(
        id='workout_table',
        columns=[{"name": col, 'id': col} for col in aggregated_data.columns],
        data=aggregated_data.to_dict('records')
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
    fig = px.line(df, x='Date', y='Value', labels={'Value' : 'Weight'})
    return fig