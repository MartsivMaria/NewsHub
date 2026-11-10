from app.models.notification import Notification
from app.services.notifications.base_factory import NotificationFactory


class BreakingNotificationFactory(NotificationFactory):

    def create_notification(self, user_id, article, link):
        return Notification(
            title="Термінова новина!",
            message=f"Опубліковано термінову новину: {article.title}",
            link=link,
            is_read=False,
            user_id=user_id
        )