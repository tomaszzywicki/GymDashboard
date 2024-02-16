from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
from datetime import date

df = pd.read_csv('workout_data.csv')

app = Dash(__name__)


app.layout = html.Div([
    html.H1(children='Gym dashboard'),
    dcc.Tabs(id="tabs", value='tab-1', children=[
        dcc.Tab(label='Tab one', value='tab-1'),
        dcc.Tab(label='Tab two', value='tab-2'),
    ]),
    html.Div(id='tabs-content')
])


@callback(Output('tabs-content', 'children'),
          Input('tabs', 'value'))
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            html.H3('Tab content 1')
        ])
                         
    elif tab == 'tab-2':
        return html.Div([
            html.H3('Tab content 2')
        ])




if __name__ == '__main__':
    app.run(debug=True)

