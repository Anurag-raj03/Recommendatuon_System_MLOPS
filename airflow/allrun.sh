set -e
trap 'echo "Error occurred! Exiting..."' ERR

echo "Downloading NLTK Data..."
python nltk_downloader.py
echo "NLTK Data Downloaded Successfully."

echo "🛠️ Initializing Airflow Database..."
airflow db init
echo "Airflow Database Initialized."

echo "Checking if Airflow Admin User exists..."
set +e
airflow users list | grep -q admin
USER_EXISTS=$?
set -e

if [ $USER_EXISTS -eq 0 ]; then
    echo "Admin user already exists."
else
    echo "Creating Airflow Admin User..."
    airflow users create \
        --username admin \
        --firstname Admin \
        --lastname Admin \
        --role Admin \
        --email admin@example.com \
        --password admin
fi
echo "Waiting 5 seconds before starting Airflow Services..."
sleep 5

echo "Starting Airflow Services..."
airflow scheduler &  
airflow webserver   
