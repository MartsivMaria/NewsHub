from datetime import datetime, timezone

from app import db


class Notification(db.Model):
    __tablename__ = "notifications"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(150), nullable=False)
    message = db.Column(db.Text, nullable=False)

    link = db.Column(db.String(255), nullable=True)

    is_read = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

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

    digest_id = db.Column(
        db.Integer,
        db.ForeignKey("digests.id"),
        nullable=True
    )