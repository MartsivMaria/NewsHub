from app.services.observers.observer import ArticleObserver

from app.repositories import (
    UserRepository,
    FollowedAuthorRepository,
    NotificationRepository
)

from app.services.notifications import (
    BreakingNotificationFactory,
    NewArticleNotificationFactory
)


class NotificationObserver(ArticleObserver):

    def update(self, article, link):

        if article.is_breaking:
            users = UserRepository.get_push_subscribers()
            notification_factory = BreakingNotificationFactory()

        else:
            users = FollowedAuthorRepository.get_push_enabled_followers(
                article.author.strip()
            )

            notification_factory = NewArticleNotificationFactory()

        for user in users:
            notification = notification_factory.create_notification(
                user_id=user.id,
                article=article,
                link=link
            )

            NotificationRepository.create(notification)