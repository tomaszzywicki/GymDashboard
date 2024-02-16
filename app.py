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


fig = px.scatter(df, x='weight_kg', y='reps')
fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)


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
            html.H3('Tab content 1'),
            dcc.Graph(figure = fig),

        ])
                         
    elif tab == 'tab-2':
        return html.Div([
            html.H3('Tab content 2'),
            generate_table(df),
            html.H3('Select muscle group'),
            dcc.Dropdown(['Chest', 'Back', 'Arms', 'Legs'],
                         multi=False),
            html.H3('Select excercise'),
            dcc.Dropdown(['Dumbell bench press', 'Chest cable fly'],
                         multi=False)
        ])
    

def generate_table(dataframe, max_rows=5):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])




if __name__ == '__main__':
    app.run(debug=True)

