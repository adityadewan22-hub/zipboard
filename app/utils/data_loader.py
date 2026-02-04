import pandas as pd

def load_excel(path):
    df=pd.read_excel(path)
    df=df.fillna("")
    return df

