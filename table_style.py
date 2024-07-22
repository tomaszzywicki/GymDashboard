style_cell_conditional_workouts=[
    {
        'if': {'column_id': col},
        'textAlign': 'left',
    } for col in ['Workout']
]

style_cell = {
    'padding': '5px 10px',
    'textAlign': 'center',
    'whiteSpace': 'normal',
    'backgroundColor': '#1d232c',
    'color': 'white'

}

style_header= {
    'backgroundColor': '#0074D9',
    'fontWeight': 'bold',
}

style_cell_conditional_exercises=[
    {
        'if': {'column_id': col},
        'textAlign': 'left',
    } for col in ['Exercise', 'Body part']
]


