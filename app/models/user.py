from datetime import datetime, timezone

from app import db
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    role = db.Column(db.String(20), default="user", nullable=False)

    subscription_plan = db.Column(
        db.String(20),
        default="free",
        nullable=False
    )
    # Налаштування сповіщень користувача
    newsletter_enabled = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    push_enabled = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )
    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    favorite_categories = db.relationship(
        "Category",
        secondary="favorite_categories",
        backref="users_who_favorited"
    )

    saved_articles = db.relationship(
        "Article",
        secondary="favorite_articles",
        backref="saved_by_users"
    )

    notifications = db.relationship(
        "Notification",
        backref="user",
        lazy=True,
        cascade="all, delete-orphan"
    )