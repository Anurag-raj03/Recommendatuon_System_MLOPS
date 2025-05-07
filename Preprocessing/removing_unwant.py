import pandas as pd
cols=["Title","Synopsis","Type","Premiered","Producers","Studios","Source","Genres","Themes","Demographics","Rating","Score"]
def rem(df:pd.DataFrame,col=cols) -> pd.DataFrame:
    for i in cols: 
        df.drop(i,axis=1,inplace=True)
    return df 