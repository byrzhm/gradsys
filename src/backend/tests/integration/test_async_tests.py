from app.routes.submission import process_submission
from app.models.submission import Submission
from app import db


def test_async_task_success(mocker, tmpdir):
    """测试成功的异步任务"""
    # Mock Docker调用
    mock_docker = mocker.patch("app.utils.docker_util.run_grading")
    mock_docker.return_value = "Score: 90"

    # 创建测试提交记录
    sub = Submission(student_id="20230001", score=0)
    db.session.add(sub)
    db.session.commit()

    # 执行任务
    process_submission(sub.id, b"test data")

    # 验证结果
    updated = Submission.query.get(sub.id)
    assert updated.score == 90
    assert updated.status == "success"


def test_async_task_failure(mocker):
    """测试失败的任务处理"""
    mocker.patch("app.utils.docker_util.run_grading", side_effect=Exception("Error"))

    sub = Submission(student_id="20230001", score=0)
    db.session.add(sub)
    db.session.commit()

    process_submission(sub.id, b"test data")

    updated = Submission.query.get(sub.id)
    assert updated.status == "failed"
    assert "Error" in updated.error_msg
