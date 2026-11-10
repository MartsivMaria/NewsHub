from app.models.notification import Notification
from app.services.notifications.base_factory import NotificationFactory


class DigestNotificationFactory(NotificationFactory):

    def create_notification(self, user_id, digest, article_count, link):
        return Notification(
            title="Ваш новинний дайджест",
            message=(
                f"Для вас підготовлено добірку "
                f"з {article_count} новин."
            ),
            link=link,
            is_read=False,
            user_id=user_id,
            digest_id=digest.id
        )