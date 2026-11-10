from app.models.notification import Notification
from app.services.notifications.base_factory import NotificationFactory


class NewArticleNotificationFactory(NotificationFactory):

    def create_notification(self, user_id, article, link):
        return Notification(
            title="Нова публікація з ваших підписок",
            message=f"Автор {article.author} опублікував нову статтю: {article.title}",
            link=link,
            is_read=False,
            user_id=user_id
        )