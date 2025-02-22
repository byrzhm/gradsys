from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_migrate import Migrate
from celery import Celery, Task
from app.config import Config
import click


class BaseModel(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=BaseModel)
migrate = Migrate()


def create_app(test_config=None) -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)
    if test_config is not None:
        app.config.update(test_config)

    db.init_app(app)
    migrate.init_app(app, db)
    celery_init_app(app)

    app.cli.add_command(init_db_command)

    from .routes import submission_bp
    from .routes import ranking_bp

    app.register_blueprint(submission_bp)
    app.register_blueprint(ranking_bp)

    return app


def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app


@click.command("init-db")
def init_db_command():
    db.create_all()
    click.echo("Initialized the database.")
