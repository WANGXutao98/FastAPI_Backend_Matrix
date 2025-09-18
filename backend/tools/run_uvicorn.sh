cd /data/app
source .env
PORT=${BACKEND_SERVER_PORT}
uvicorn src.main:backend_app --reload --host 0.0.0.0 --port ${PORT}
