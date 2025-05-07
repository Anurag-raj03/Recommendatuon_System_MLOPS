
def merging_csv_file(new_preprocessd_path: str, old_preprocessd_path: str) -> None:
    import pandas as pd
    import os
    import sys

    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

    if os.path.exists(old_preprocessd_path):
        old_df = pd.read_csv(old_preprocessd_path)
        print("Old CSV file loaded successfully!", old_df.shape)
    else:
        raise ValueError("No old csv file has been found")   
    
    if os.path.exists(new_preprocessd_path):
        new_df = pd.read_csv(new_preprocessd_path)
        print("New CSV file loaded successfully!", new_df.shape)
        if not new_df.empty:
            merge_df = pd.concat([old_df, new_df], ignore_index=True)
            merge_df.to_csv(old_preprocessd_path, index=False)
            print("Data has been merged successfully!")
        else:
            print("New CSV file is empty. No data merged.")    
    else:
        print("New CSV file not found.")