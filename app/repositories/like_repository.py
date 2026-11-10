from app.models.like import Like
from app import db


class LikeRepository:

    @staticmethod
    def get_by_user_and_article(user_id, article_id):
        return Like.query.filter_by(
            user_id=user_id,
            article_id=article_id
        ).first()

    @staticmethod
    def create(like):
        db.session.add(like)
        db.session.commit()

    @staticmethod
    def delete(like):
        db.session.delete(like)
        db.session.commit()

    @staticmethod
    def is_liked_by_user(user_id, article_id):
        return Like.query.filter_by(
            user_id=user_id,
            article_id=article_id
        ).first() is not None