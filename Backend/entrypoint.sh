echo "⏳ Waiting for monitoring to complete..."

echo "✅ Monitoring completed."
echo "📂 Initializing the Databases..."
python Database_connection/db_init.py
echo "✅ Backend completed. Flag created for frontend."
echo "🚀 Starting FastAPI application..."
uvicorn main:app --host 0.0.0.0 --port 8000
