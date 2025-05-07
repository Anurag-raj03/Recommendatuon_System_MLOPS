from airflow.decorators import task

print("Load file Running")
@task
def aft_to_csv():
    conn = None 
    try:
        import os
        import sys
        import pandas as pd
        import sqlite3
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
        from Database_connection.db_init import get_connection

        print("Load file Running")
        db_path = "/opt/airflow/Database_connection/anime_preprocessed_dat.db"
        etl_preprocessed = os.path.join("Data_Versioning", "preprocessed", "etl_transform.csv")
        conn = get_connection(db_path)
        if conn is None:
            print("Failed to establish database connection.")
            return
        query = "SELECT * FROM anime_preprocessed_table"
        df = pd.read_sql(query, conn)

        if df.empty:
            print("No data available to load.")
            return
        df.to_csv(etl_preprocessed, index=False)
        print(f"Data saved to {etl_preprocessed}")
        with conn:
            conn.execute("DELETE FROM anime_preprocessed_table")
        print("Table cleaned after extraction.")

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        if conn:
            conn.close() 