import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # Flask基础配置
    SECRET_KEY = os.environ.get(
        "SECRET_KEY", "a_random_secret_key"
    )  # 需要更改为安全的随机密钥
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 禁用对象修改追踪
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "sqlite:///app.db"
    )  # SQLite数据库
    SUBMIT_FOLDER = os.environ.get("SUBMIT_FOLDER", "/var/submit")  # 上传文件的保存路径

    # Docker配置
    GRADING_IMAGE = os.environ.get(
        "GRADING_IMAGE", "grading-image:latest"
    )  # 评分用的Docker镜像
    DOCKER_TIMEOUT = 3600  # 容器执行评分脚本的最大时长（单位秒）

    # Celery配置
    CELERY = {
        "broker_url": os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379/0"),
        "result_backend": os.environ.get(
            "CELERY_RESULT_BACKEND", "redis://localhost:6379/0"
        ),
    }

    # 日志配置
    LOGGING_LEVEL = os.environ.get("LOGGING_LEVEL", "DEBUG")
    LOG_FILE_PATH = os.environ.get("LOG_FILE_PATH", "/var/log/app.log")
