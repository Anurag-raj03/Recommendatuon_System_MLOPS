import pandas as pd
def remove_na(df:pd.DataFrame) -> pd.DataFrame:
    df=df[df['English']!='Unknown']
    return df.dropna(axis=1,inplace=True)
