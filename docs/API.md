# 作业评分系统 API 文档

## 认证方式
使用JWT Bearer Token认证：

Authorization: Bearer \<your_jwt_token\>

## 接口列表

### 1. 提交作业
**URL**  
`POST /api/v1/submit`

**请求格式**  
```http
Content-Type: multipart/form-data
```

参数：
- student_id: 学号
- file: ZIP压缩包文件（最大10MB）

**成功响应**

```json
{
  "message": "提交已接收",
  "submission_id": 123
}
```

**错误状态码**

- 400: 无效的请求格式
- 413: 文件超过大小限制
- 500: 服务器内部错误


### 2. 获取排行榜

**URL**

`GET /api/v1/ranking`

**成功响应**
```json
{
  "items": [
    {
      "rank": 1,
      "student_id": "20230001",
      "score": 95,
      "submit_time": "2023-08-20 14:30:00"
    }
  ],
}
```

### 3. 查询提交状态

**URL**
`GET /api/v1/submissions/{submission_id}`

**成功响应**
```json
{
  "submission_id": 123,
  "status": "success",
  "score": 95,
  "error_msg": null
}
```

**状态码说明**
- 200: 请求成功
- 400: 客户端请求错误
- 401: 未授权访问
- 500: 服务器内部错误


---

### 部署说明

1. **安装依赖**
```bash
# requirements.txt
celery==5.4.0
docker==7.1.0
Flask==3.1.0
Flask-Migrate==4.1.0
Flask-SQLAlchemy==3.1.1
gunicorn==23.0.0
python-dotenv==1.0.1
```

2. **数据库迁移**
```bash
flask db init
flask db migrate -m "initial migration"
flask db upgrade
```

3. **启动服务**
```bash
# 启动Flask应用
gunicorn -w 4 'app:create_app()'

# 启动Celery Worker
celery -A app.celery worker --loglevel=info
```
