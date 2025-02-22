#!/bin/bash

# celery
echo "Starting Celery worker..."
celery -A make_celery worker --loglevel=info &

# 启动 Flask 后端应用
echo "Starting Flask backend..."

# 初始化数据库
flask init-db

flask run --host=0.0.0.0 --port=5000

# TODO: gunicorn