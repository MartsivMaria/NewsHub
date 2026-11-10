from datetime import datetime, timezone

from app import db


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    content = db.Column(db.Text, nullable=False)

    image = db.Column(db.String(500))
    author = db.Column(db.String(120), nullable=False)

    published_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    views = db.Column(db.Integer, default=0, nullable=False)
    is_featured = db.Column(db.Boolean, default=False, nullable=False)

    is_exclusive = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )
    is_breaking = db.Column(
        db.Boolean,
        default=False, 
        nullable=False
    )

    category_id = db.Column(
        db.Integer,
        db.ForeignKey("category.id"),
        nullable=False
    )

    category = db.relationship(
        "Category",
        back_populates="articles"
    )
