import pytest
from datetime import datetime
from app.models import Submission


@pytest.mark.skip(reason="跳过测试初始数据")
def test_initial_seed_data(test_db):
    """测试初始数据"""
    query = test_db.session.query(Submission).all()
    assert len(query) == 2
    assert query[0].student_id == "2025211233"
    assert query[1].student_id == "2025211234"


def test_submission_creation(test_app, test_db):
    """测试提交记录创建"""
    with test_app.app_context():
        sub = Submission(student_id="20230001", score=85)
        test_db.session.add(sub)
        test_db.session.commit()

        assert sub.id is not None
        assert sub.status == "pending"
        assert isinstance(sub.submit_time, datetime)


def test_unique_constraint(test_app, test_db):
    """测试唯一性约束"""
    with test_app.app_context():
        sub1 = Submission(
            student_id="20230001", score=85, submit_time=datetime(2021, 1, 1, 12, 0, 0)
        )
        test_db.session.add(sub1)
        test_db.session.commit()

        sub2 = Submission(
            student_id="20230001", score=90, submit_time=datetime(2021, 1, 1, 13, 0, 0)
        )
        test_db.session.add(sub2)
        test_db.session.commit()

        # 尝试创建相同时间的提交
        sub3 = Submission(
            student_id="20230001", score=95, submit_time=datetime(2021, 1, 1, 12, 0, 0)
        )
        test_db.session.add(sub3)

        with pytest.raises(Exception):
            test_db.session.commit()
