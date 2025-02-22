from flask import Blueprint, jsonify
from app.models import Submission
from app import db
from sqlalchemy import select, func, and_

ranking_bp = Blueprint("ranking", __name__, url_prefix="/api/v1")


@ranking_bp.route("/ranking", methods=["GET"])
def get_ranking():
    """
    每个学号有多次提交，只取最高分
    """
    max_score_subquery = (
        select(Submission.student_id, func.max(Submission.score).label("max_score"))
        .where(Submission.status == "success")
        .group_by(Submission.student_id)
        .subquery()
    )

    stmt = (
        select(Submission.student_id, Submission.score, Submission.submit_time)
        .join(
            max_score_subquery,
            and_(
                Submission.student_id == max_score_subquery.c.student_id,
                Submission.score == max_score_subquery.c.max_score,
            ),
        )
        .where(Submission.status == "success")
        .order_by(Submission.score.desc(), Submission.submit_time.asc())
    )

    items = []
    for i, row in enumerate(db.session.execute(stmt).all()):
        items.append(
            {
                "rank": i + 1,
                "student_id": row.student_id,
                "score": row.score,
                "submit_time": row.submit_time.strftime("%Y-%m-%d %H:%M:%S"),
            }
        )

    return jsonify({"items": items})
