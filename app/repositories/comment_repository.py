from app.models.comment import Comment
from app import db


class CommentRepository:

    @staticmethod
    def get_by_id(comment_id):
        return db.session.get(Comment, comment_id)

    @staticmethod
    def create(comment):
        db.session.add(comment)
        db.session.commit()
        return comment

    @staticmethod
    def delete(comment):
        db.session.delete(comment)
        db.session.commit()

    @staticmethod
    def get_by_article(article_id):
        return Comment.query.filter_by(
            article_id=article_id
        ).order_by(
            Comment.created_at.desc()
        ).all()