import pandas as pd 
cols=["Title","Synopsis","Type","Premiered","Producers","Studios","Source","Genres","Themes","Demographics","Rating","Score"]
def merg(df:pd.DataFrame,col=cols) ->pd.DataFrame:
    df['About']=""
    for i in col:
        df['About']+=df[i]+" "
    return df
