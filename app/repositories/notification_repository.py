from app.models.notification import Notification
from app import db


class NotificationRepository:

    @staticmethod
    def get_all_by_user(user_id):
        return Notification.query.filter_by(
            user_id=user_id
        ).order_by(
            Notification.created_at.desc()
        ).all()

    @staticmethod
    def get_unread_count(user_id):
        return Notification.query.filter_by(
            user_id=user_id,
            is_read=False
        ).count()

    @staticmethod
    def get_by_id(notification_id, user_id):
        return Notification.query.filter_by(
            id=notification_id,
            user_id=user_id
        ).first()

    @staticmethod
    def create(notification):
        db.session.add(notification)
        db.session.commit()
        return notification

    @staticmethod
    def mark_as_read(notification):
        notification.is_read = True
        db.session.commit()
        return notification

    @staticmethod
    def get_all_by_user(user_id):
        return Notification.query.filter_by(
            user_id=user_id
        ).order_by(
            Notification.created_at.desc()
        ).all()