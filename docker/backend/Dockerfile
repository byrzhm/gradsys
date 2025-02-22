# 基础镜像：使用官方的 Python 3 镜像
FROM python:3.10-slim

WORKDIR /app
COPY ./src/backend /app

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 安装任何其他需要的系统依赖（如果有）
RUN apt-get update && apt-get install -y --no-install-recommends \
    # 添加您的其他依赖，如果有需要的话
    && apt-get clean

# 将 entrypoint.sh 脚本复制到容器中
COPY ./docker/backend/entrypoint.sh /app/entrypoint.sh

# 给予执行权限
RUN chmod +x /app/entrypoint.sh

# 设置容器启动时执行的命令
ENTRYPOINT ["/app/entrypoint.sh"]
