from app import db

favorite_articles_table = db.Table(
    "favorite_articles",

    db.Column(
        "user_id",
        db.Integer,
        db.ForeignKey("users.id"),
        primary_key=True
    ),

    db.Column(
        "article_id",
        db.Integer,
        db.ForeignKey("article.id"),
        primary_key=True
    )
)