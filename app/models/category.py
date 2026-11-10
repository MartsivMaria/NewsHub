from app import db


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(80), unique=True, nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False)

    articles = db.relationship(
        "Article",
        back_populates="category",
        lazy=True
    )
