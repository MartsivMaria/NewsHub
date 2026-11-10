from datetime import datetime, timezone
from app import db


class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)

    content = db.Column(db.Text, nullable=False)

    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

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

    user = db.relationship("User", backref="comments")
    article = db.relationship("Article", backref="comments")
