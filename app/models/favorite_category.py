from app import db

favorite_categories_table = db.Table(
    "favorite_categories",

    db.Column(
        "user_id",
        db.Integer,
        db.ForeignKey("users.id"),
        primary_key=True
    ),

    db.Column(
        "category_id",
        db.Integer,
        db.ForeignKey("category.id"),
        primary_key=True
    )
)