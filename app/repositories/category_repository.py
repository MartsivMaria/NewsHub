from app.models.category import Category
from app import db


class CategoryRepository:

    @staticmethod
    def get_all():
        return Category.query.order_by(Category.name).all()

    @staticmethod
    def get_by_ids(category_ids):
        if not category_ids:
            return []
        return Category.query.filter(Category.id.in_(category_ids)).all()

    @staticmethod
    def count():
        return Category.query.count()

    @staticmethod
    def create_many(categories):
        db.session.add_all(categories)
        db.session.commit()
    