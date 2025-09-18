#!/usr/bin/env bash
set +x
cd /app

ulimit -HSn 65535

CUR_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_FILE=config/.env

source /etc/profile

#BACKEND_SERVER_PORT默认为8888
# 检查环境变量是否设置
if [[ -n "$BACKEND_SERVER_PORT" ]]; then
  PORT="$BACKEND_SERVER_PORT"
else
  # 检查是否存在 .env 文件
  if [[ -f $ENV_FILE ]]; then
    # 读取 .env 文件中的变量值
    PORT=$(grep 'BACKEND_SERVER_PORT' $ENV_FILE | sed 's/BACKEND_SERVER_PORT=//g')
  else
    # 设置默认变量值
    PORT=8888
  fi
fi
echo "PORT:${PORT}"

#BACKEND_SERVER_WORKERS默认为2
# 检查环境变量是否设置
if [[ -n "$BACKEND_SERVER_WORKERS" ]]; then
  WORKERS="$BACKEND_SERVER_WORKERS"
else
  # 检查是否存在 .env 文件
  if [[ -f $ENV_FILE ]]; then
    # 读取 .env 文件中的变量值
    WORKERS=$(grep 'BACKEND_SERVER_WORKERS' $ENV_FILE | sed 's/BACKEND_SERVER_WORKERS=//g')
  else
    # 设置默认变量值
    WORKERS=2
  fi
fi
echo "WORKERS:${WORKERS}"

WORKER_THREADS=100

monitor() {
  COUNT=$(lsof -i:$PORT | grep -c LIS)
  echo ${COUNT}
  if [ $COUNT -eq 0 ]; then
    echo "start"
    start_gunicorn
  fi
}

stop_gunicorn() {
  PIDS=$(lsof -i:$PORT | grep LISTEN | grep gunicorn | awk '{split($0,a," "); print a[2]}')
  for PID in ${PIDS[*]}; do
    echo $PID
    kill -9 $PID
  done
}

start_gunicorn() {
    mkdir -p logs
    
    gunicorn src.main:backend_app \
    --worker-class uvicorn.workers.UvicornWorker  \
    --bind 0.0.0.0:$PORT \
    --workers=$WORKERS \
    --worker-connections=$WORKER_THREADS \
    --timeout 300 \
    --log-level info \
    --access-logfile=logs/gunicorn_access.log \
    --error-logfile=logs/gunicorn_error.log &
}

case "$1" in
"start")
  start_gunicorn
  ;;
"stop")
  stop_gunicorn
  ;;
"restart")
  stop_gunicorn
  sleep 1
  start_gunicorn
  ;;
"monitor")
  monitor
  ;;
*)
  echo "error,usage: run.sh start/stop/restart/monitor"
  exit 1
  ;;
esac
