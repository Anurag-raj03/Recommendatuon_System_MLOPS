import pandas as pd
def read_file(file_path:str)->pd.DataFrame:
    if file_path.endswith("csv"):
        return pd.read_csv(file_path)
    elif file_path.endswith("xlsx"):
        return pd.read_excel(file_path) 
    else:
        raise ValueError("The Files in the given File path is not satisfying the extension .csv or .xlsx")  
          
          
        
    