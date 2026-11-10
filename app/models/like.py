from datetime import datetime, timezone

from app import db


class Like(db.Model):
    __tablename__ = "likes"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    article_id = db.Column(
        db.Integer,
        db.ForeignKey("article.id"),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    __table_args__ = (
        db.UniqueConstraint(
            "user_id",
            "article_id",
            name="unique_user_article_like"
        ),
    )