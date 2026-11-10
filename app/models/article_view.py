from datetime import datetime, timezone

from app import db


class ArticleView(db.Model):
    __tablename__ = "article_views"

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

    viewed_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )