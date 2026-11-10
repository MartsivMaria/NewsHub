from app import db
from app.models.followed_author import FollowedAuthor
from app.models.user import User


class FollowedAuthorRepository:

    @staticmethod
    def is_following(user_id, author_name):
        return FollowedAuthor.query.filter_by(
            user_id=user_id,
            author_name=author_name
        ).first() is not None

    @staticmethod
    def follow(user_id, author_name):
        if FollowedAuthorRepository.is_following(
            user_id, author_name
        ):
            return None

        followed_author = FollowedAuthor(
            user_id=user_id,
            author_name=author_name
        )

        db.session.add(followed_author)
        db.session.commit()

        return followed_author

    @staticmethod
    def unfollow(user_id, author_name):
        followed_author = FollowedAuthor.query.filter_by(
            user_id=user_id,
            author_name=author_name
        ).first()

        if followed_author:
            db.session.delete(followed_author)
            db.session.commit()

        return followed_author

    @staticmethod
    def get_push_enabled_followers(author_name):
        return (
            User.query
            .join(
                FollowedAuthor,
                FollowedAuthor.user_id == User.id
            )
            .filter(
                FollowedAuthor.author_name == author_name,
                User.push_enabled.is_(True)
            )
            .all()
        )

    @staticmethod
    def get_followed_by_user(user_id):
        return (
            FollowedAuthor.query
            .filter_by(user_id=user_id)
            .order_by(FollowedAuthor.author_name.asc())
            .all()
        )