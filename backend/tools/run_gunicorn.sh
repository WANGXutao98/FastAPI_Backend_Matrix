cd /data/app

export PORT=${BACKEND_SERVER_PORT:-8888}
gunicorn src.main:backend_app \
    --worker-class uvicorn.workers.UvicornWorker 
