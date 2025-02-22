from flask import current_app
from flask import Blueprint, request, jsonify
from app.utils import safe_extract, run_grading, parse_result
from app.models import Submission
from app import db
from celery import shared_task
import tempfile
import os
from datetime import datetime

submission_bp = Blueprint("submission", __name__, url_prefix="/api/v1")


@submission_bp.route("/submit", methods=["POST"])
def handle_submission():
    # 文件验证逻辑
    if "file" not in request.files:
        return jsonify(error="未上传文件"), 400

    file = request.files["file"]
    student_id = request.form.get("student_id")

    # 创建数据库记录
    submission = Submission(
        student_id=student_id,
        submit_time=datetime.now(),
        status="pending",
    )
    db.session.add(submission)
    db.session.commit()

    # 启动异步任务
    process_submission.delay(submission.id, student_id, file.read())
    return jsonify(message="提交已接收", submission_id=submission.id)


@shared_task
def process_submission(submission_id: int, student_id: str, file_data):
    # 异步处理逻辑
    submission = Submission.query.get(submission_id)
    try:
        submit_folder = current_app.config["SUBMIT_FOLDER"]
        # 保存文件
        os.makedirs(submit_folder, exist_ok=True)
        zip_path = os.path.join(submit_folder, f"{submission_id}-{student_id}.zip")
        with tempfile.TemporaryDirectory() as tmpdir:
            # 保存并解压文件
            with open(zip_path, "wb") as f:
                f.write(file_data)

            safe_extract(zip_path, tmpdir)

            # 运行评分容器
            result = run_grading(
                submission_code_path=tmpdir,
                grading_script_path=current_app.config["GRADING_SCRIPT_PATH"],
                grading_image=current_app.config["GRADING_IMAGE"],
            )
            score = parse_result(result)

            # 更新数据库
            submission.score = score
            submission.status = "success"
    except Exception as e:
        submission.status = "failed"
        submission.error_msg = str(e)
    finally:
        db.session.commit()
