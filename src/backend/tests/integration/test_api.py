from app.models.submission import Submission
import io
from datetime import datetime
from app.routes.submission import process_submission

def test_submission_api(client, test_db, mocker):
    """测试作业提交接口"""
    # Mock异步任务
    mocker.patch("app.routes.submission.process_submission.delay")

    # 准备测试文件
    test_file = (io.BytesIO(b"test content"), "test.zip")

    response = client.post(
        "/api/v1/submit", data={"student_id": "20230001", "file": test_file}
    )

    process_submission.delay.assert_called_once()

    assert response.status_code == 200
    assert "submission_id" in response.json


def test_ranking_api(client, test_db):
    """测试排行榜接口"""
    # 插入测试数据
    for i in range(1, 6):
        sub = Submission(student_id=f"2023000{i}", score=100 - i * 5, status="success")
        test_db.session.add(sub)
    test_db.session.commit()

    response = client.get("/api/v1/ranking")
    data = response.json

    assert len(data["items"]) == 5
    assert data["items"][0]["score"] == 95  # 100 - 1*5


def test_ranking_api_hard(client, test_db):
    """
    测试排行榜接口
    每个学号有多次提交，只取最高分
    """
    # 插入测试数据
    for i in range(1, 6):
        for j in range(3):
            sub = Submission(
                student_id=f"2023000{i}",
                score=100 - i * 5 - j,
                status="success",
                submit_time=datetime(2021, 1, 1, j + 1, 0, 0),
            )
            test_db.session.add(sub)
    test_db.session.commit()

    response = client.get("/api/v1/ranking")
    data = response.json

    assert len(data["items"]) == 5
    assert data["items"][0]["score"] == 95  # 100 - 1*5
    assert data["items"][1]["score"] == 90  # 100 - 1*5 - 1
    assert data["items"][2]["score"] == 85  # 100 - 1*5 - 2
    assert data["items"][3]["score"] == 80  # 100 - 1*5 - 3
    assert data["items"][4]["score"] == 75  # 100 - 1*5 - 4
