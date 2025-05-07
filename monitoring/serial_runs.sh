set -e
python model_register.py
python nltk_downloader.py
python pipeline.py
python main_pipeline.py

echo "Running the monitoring service Completed"

# dvc add Data_Versioning
# git add Data_Versioning.dvc .gitignore
# # git commit -m "Updated DVC Folder"
# echo "New Updated Version of Data has been Pushed"


