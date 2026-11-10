import json

from app.models import Digest

from app.repositories import (
    UserRepository,
    ArticleRepository,
    DigestRepository,
    NotificationRepository
)

from app.services.notifications import DigestNotificationFactory


class DigestFacade:
    """Facade: один метод generate() об'єднує всі кроки формування дайджесту."""

    def __init__(self):
        self.factory = DigestNotificationFactory()

    def generate(self, notification_link, limit=5):
        sent_count = 0

        for user in UserRepository.get_subscribers():
            articles = self._pick_articles(user, limit)

            if not articles:
                continue

            digest = self._save_digest(user, articles)

            notification = self.factory.create_notification(
                user_id=user.id,
                digest=digest,
                article_count=len(articles),
                link=notification_link
            )

            NotificationRepository.create(notification)

            sent_count += 1

        return sent_count

    def _pick_articles(self, user, limit):
        category_ids = [
            category.id
            for category in user.favorite_categories
        ]

        if not category_ids:
            return []

        return ArticleRepository.get_by_categories(
            category_ids,
            limit=limit
        )

    def _save_digest(self, user, articles):
        digest = Digest(
            title="Ваш персональний новинний дайджест",
            article_ids=json.dumps([article.id for article in articles]),
            user_id=user.id
        )

        DigestRepository.create(digest)

        return digest