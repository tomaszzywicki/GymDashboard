from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
from datetime import date

df = pd.read_csv('workout_data.csv')

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
                generate_table(df)
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
                         multi=False)
        ])
    

def generate_table(dataframe):
    # będzie w zależności od setów, repów
    df = dataframe.groupby('exercise_title').agg({'exercise_title':'count'}).rename(columns={'exercise_title':'count'}).sort_values(by='count', ascending=False).head(5).reset_index()
    return dash_table.DataTable(
            id = 'exercise_table',
            columns=[{"name": col, 'id': col} for col in df.columns],
            data=df.to_dict('records')
        )





if __name__ == '__main__':
    app.run(debug=True)

