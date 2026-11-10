from app import db


class FollowedAuthor(db.Model):
    __tablename__ = "followed_authors"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    author_name = db.Column(
        db.String(150),
        nullable=False
    )

    __table_args__ = (
        db.UniqueConstraint(
            "user_id",
            "author_name",
            name="unique_user_author"
        ),
    )