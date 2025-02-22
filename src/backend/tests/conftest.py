import os
import tempfile

import pytest
from app import create_app
from app import db as _db
from sqlalchemy import text
from flask import current_app

with open(os.path.join(os.path.dirname(__file__), "data.sql"), "rb") as f:
    _data_sql = f.read().decode("utf8")


@pytest.fixture
def test_app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///" + db_path,
            "CELERY_ALWAYS_EAGER": True,
            "DB_USE_TEST_DATA": False,
        }
    )

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(test_app):
    return test_app.test_client()


@pytest.fixture
def test_db(test_app):
    with test_app.app_context():
        _db.create_all()
        if current_app.config["DB_USE_TEST_DATA"]:
            _db.session.execute(text(_data_sql))
            _db.session.commit()
        yield _db
        _db.drop_all()
