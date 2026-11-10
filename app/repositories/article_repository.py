from app.models.article import Article
from app import db


class ArticleRepository:

    @staticmethod
    def get_all():
        return Article.query.order_by(
            Article.published_at.desc()
        ).all()

    @staticmethod
    def get_for_homepage():
        return Article.query.order_by(
            Article.is_featured.desc(),
            Article.published_at.desc(),
            Article.id.desc()
        ).all()

    @staticmethod
    def get_by_id(article_id):
        return Article.query.get(article_id)

    @staticmethod
    def get_latest(limit=5):
        return Article.query.order_by(
            Article.published_at.desc()
        ).limit(limit).all()

    @staticmethod
    def get_by_categories(category_ids, limit=5):
        if not category_ids:
            return []

        return Article.query.filter(
            Article.category_id.in_(category_ids)
        ).order_by(
            Article.published_at.desc()
        ).limit(limit).all()

    @staticmethod
    def get_breaking():
        return Article.query.filter_by(
            is_breaking=True
        ).order_by(
            Article.published_at.desc()
        ).all()

    @staticmethod
    def get_exclusive():
        return Article.query.filter_by(
            is_exclusive=True
        ).order_by(
            Article.published_at.desc()
        ).all()

    @staticmethod
    def get_recommended(category_ids, viewed_article_ids=None, limit=5):
        if not category_ids:
            return []

        query = Article.query.filter(
            Article.category_id.in_(category_ids)
        )

        if viewed_article_ids:
            query = query.filter(
                ~Article.id.in_(viewed_article_ids)
            )

        return query.order_by(
            Article.views.desc(),
            Article.published_at.desc()
        ).limit(limit).all()

    @staticmethod
    def create(article):
        db.session.add(article)
        db.session.commit()
        return article

    @staticmethod
    def delete(article):
        db.session.delete(article)
        db.session.commit()

    @staticmethod
    def get_viewed_category_ids(user_id):
        from app.models.article_view import ArticleView

        results = (
            db.session.query(Article.category_id)
            .join(ArticleView, ArticleView.article_id == Article.id)
            .filter(ArticleView.user_id == user_id)
            .distinct()
            .all()
        )

        return [category_id for (category_id,) in results]


    @staticmethod
    def get_liked_category_ids(user_id):
        from app.models.like import Like

        results = (
            db.session.query(Article.category_id)
            .join(Like, Like.article_id == Article.id)
            .filter(Like.user_id == user_id)
            .distinct()
            .all()
        )

        return [category_id for (category_id,) in results]
    
    @staticmethod
    def get_by_ids(article_ids):
        if not article_ids:
            return []

        return Article.query.filter(
            Article.id.in_(article_ids)
        ).order_by(
            Article.published_at.desc()
        ).all()

    @staticmethod
    def update():
        db.session.commit()

    @staticmethod
    def increment_views(article):
        article.views += 1
        db.session.commit()


    @staticmethod
    def get_likes_count(article_id):
        from app.models.like import Like

        return Like.query.filter_by(article_id=article_id).count()
    
    @staticmethod
    def count():
        return Article.query.count()

    @staticmethod
    def get_viewed_article_ids(user_id):
        from app.models.article_view import ArticleView

        results = db.session.query(
            ArticleView.article_id
        ).filter_by(
            user_id=user_id
        ).distinct().all()

        return [article_id for (article_id,) in results]