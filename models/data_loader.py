import pandas as pd
from datetime import datetime

def load_poll_data(file_path):
    df = pd.read_csv(file_path)
    df['Sample'] = df['Sample'].str.split('@@').str[1].astype(float)
    df['EndDate'] = pd.to_datetime(df['Dates'].str.split('-').str[-1].str.split('@@').str[0].str.strip(), format='%m/%d')
    current_year = datetime.now().year
    df['EndDate'] = df['EndDate'].apply(lambda x: x.replace(year=current_year))
    return df

def load_pollster_ratings(file_path):
    df = pd.read_csv(file_path)
    df['Grade'] = df['Grade'].str.split('@@').str[0]
    df['Predictive +/-'] = df['Predictive +/-'].astype(float)
    df['Mean-reverted bias'] = df['Mean-reverted bias'].str.split('@@').str[1].astype(float)
    return df
