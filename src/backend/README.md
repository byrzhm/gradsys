```bash
pip install -e .

# 运行测试
# 安装依赖
pip install pytest pytest-mock

# 运行全部测试
pytest tests/unit/ tests/integration/ -v

# 运行指定模块
pytest tests/unit/test_models.py -v

# 测试报告
pytest --html=report.html
```