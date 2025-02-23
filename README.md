# gradsys
一个完整的评分系统


## 创建评分容器
```bash
mkdir var
git clone git@github.com:bupthpc/cs101-sp25-labs.git var/labs --depth=1
docker build -t grading-image -f ./docker/grading/Dockerfile .
```

## 在开发过程中启动项目

```bash
# 前端
cd src/frontend
npm run dev

# 后端
cd src/backend
## redis for celery broker
docker run -d -p 6379:6379 redis
## celery
celery -A make_celery worker --loglevel INFO
## 初始化数据库, 可能需要 rm -rf instance/
flask init-db
## 启动 flask
flask run --debug --host=0.0.0.0
```

> [!WARNING]
> 部分配置放置在 `.env` 中, 使用 `python-dotenv` 进行读取, 见 `config.py`, 部署时需要按情况进行配置
