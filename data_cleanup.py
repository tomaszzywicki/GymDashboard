import pandas as pd


def clean_workout_data(df):
    muscle_group_dict = {
        'Seated Incline Curl (Dumbbell)': 'Arms',
        'Seated Palms Up Wrist Curl': 'Arms',
        'Triceps Extension (Dumbbell)': 'Arms',
        'Preacher Curl (Dumbbell)': 'Arms',
        'Triceps Pushdown': 'Arms',
        'Forearm Dumbell Curl': 'Arms',
        'Hammer Curl (Dumbbell)': 'Arms',
        'Knee Raise Parallel Bars': 'Abs',
        'Leg Press Horizontal (Machine)': 'Legs',
        'Pull Up': 'Back',
        'Seated Row (Machine)': 'Back',
        'Face Pull': 'Shoulders',
        'Leg Extension (Machine)': 'Legs',
        'Dumbell Skiers': 'Shoulders',
        'Shrug (Dumbbell)': 'Back',
        'Seated Cable Row - Bar Grip': 'Back',
        'Lat Pulldown (Machine)': 'Back',
        'Seated Calf Raise': 'Legs',
        'Incline Bench Press (Dumbbell)': 'Chest',
        'Shoulder Press (Dumbbell)': 'Shoulders',
        'Incline Bench Press (Barbell)': 'Chest',
        'Lateral Raise (Dumbbell)': 'Shoulders',
        'Cable Fly Crossovers': 'Chest',
        'Shoulder Press (Machine Plates)': 'Shoulders',
        'Torso Rotation': 'Abs'
    }

    df['muscle_group'] = df['exercise_title'].map(muscle_group_dict)


    df['start_time'] = pd.to_datetime(df['start_time'], format='%d %b %Y, %H:%M')
    df['end_time'] = pd.to_datetime(df['end_time'], format='%d %b %Y, %H:%M')
    df['duration'] = (df['end_time'] - df['start_time']).dt.total_seconds() / 60
    return df


def clean_weight_data(df):
    df = df.loc[df['Measurement'] == 'Bodyweight']
    return df
