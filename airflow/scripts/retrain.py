from airflow.decorators import task

print("retrain file  running")


@task
def retrain_after_updated():
    try:
        import pandas as pd
        import os
        import sys

        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
        from updated_run_monitoring.mergeing_old_new import merging_csv_file
        from updated_run_monitoring.retrain_run import rerun_pipeline

        preprocess_data_path = os.path.join("Data_Versioning", "preprocessed", "Preprocessed_anime.csv")
        cosine_sim_path = os.path.join("artifacts", "anime_cosine.jbl")
        new_preprocessd_path = "Data_Versioning/preprocessed/etl_transform.csv"
        old_preprocessd_path = os.path.join("Data_Versioning", "preprocessed", "Preprocessed_anime.csv")

        print("🚀 Retrain process started...")

        merging_csv_file(new_preprocessd_path, old_preprocessd_path)
        rerun_pipeline(preprocess_data_path, cosine_sim_path)

        print("✅ Retrain process completed successfully.")

    except Exception as e:
        print(f"❌ Error in retrain_after_updated task: {e}")