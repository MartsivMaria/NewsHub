from app.models.digest import Digest
from app import db


class DigestRepository:

    @staticmethod
    def get_by_id(digest_id):
        return Digest.query.get(digest_id)

    @staticmethod
    def get_by_user(user_id):
        return Digest.query.filter_by(
            user_id=user_id
        ).order_by(
            Digest.created_at.desc()
        ).all()

    @staticmethod
    def create(digest):
        db.session.add(digest)
        db.session.commit()
        return digest

    @staticmethod
    def delete(digest):
        db.session.delete(digest)
        db.session.commit()

    @staticmethod
    def get_by_id_and_user(digest_id, user_id):
        return Digest.query.filter_by(
            id=digest_id,
            user_id=user_id
        ).first()