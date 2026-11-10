from app.models.article_view import ArticleView
from app import db


class ArticleViewRepository:

    @staticmethod
    def create(article_view):
        db.session.add(article_view)
        db.session.commit()