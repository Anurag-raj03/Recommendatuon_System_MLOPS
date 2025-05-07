from airflow.decorators import task
print("Extract file is Running")
@task
def extract_data():
    conn=None
    import os
    import sys
    import pandas as pd

    # Append the parent directory to sys.path
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

    # Import after sys.path modification
    from Database_connection.db_init import get_connection

    try:
        # 🎯 Hardcoded database paths
        db_path_raw = "/opt/airflow/Database_connection/anime_dat.db"
        db_path_preprocessed = "/opt/airflow/Database_connection/anime_preprocessed_dat.db"

        # Paths for CSV files
        DVC_FOLDER = "Data_Versioning/ETL_Data"
        csv_path = os.path.join(DVC_FOLDER, "extracted_data.csv")
        main_sample_path = os.path.join("Data_Versioning", "raw_data", "Sample_df.csv")
        
        print("Extract task is running...")

        # Connect to raw database
        conn = get_connection(db_path_raw)
        if conn is None:
            print("Database Connection Failed.")
            return

        print("Database connection succeeded ----Extract.py")

        # Extract data
        query = "SELECT * FROM anime"
        df = pd.read_sql(query, conn)

        if df.empty:
            print("DAG Task returned None.")
            return 

        # Save extracted data
        df.to_csv(csv_path, index=False)

        # Clean up: delete extracted data from DB
        cursor = conn.cursor()
        cursor.execute("DELETE FROM anime")
        conn.commit()
        cursor.close()
        conn.close()

        print("After Extraction, the entries have been deleted.")
        print(f"Data extracted from the Database and saved successfully at {csv_path}")

        # Merge extracted data with main sample
        df1 = pd.read_csv(csv_path)
        df2 = pd.read_csv(main_sample_path)
        df_combined = pd.concat([df2, df1], ignore_index=True)
        df_combined.to_csv(main_sample_path, index=False)

    except Exception as e:
        print(f"Error: {e}")
