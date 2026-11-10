from abc import ABC, abstractmethod


class ArticleContent(ABC):
    """Спільний інтерфейс для реального об'єкта і Proxy."""

    @abstractmethod
    def get_content(self):
        pass


class RealArticleContent(ArticleContent):
    """Реальний об'єкт: повертає повний текст новини."""

    def __init__(self, article):
        self.article = article

    def get_content(self):
        return self.article.content


class ArticleProxy(ArticleContent):
    """Захисний Proxy для контролю доступу до новин."""

    PREMIUM_PLANS = ["premium", "student", "corporate"]

    def __init__(self, article, user):
        self.article = article
        self.user = user
        self._real = RealArticleContent(article)

    def has_full_access(self):
        if not self.article.is_exclusive:
            return True

        return (
            self.user.is_authenticated
            and self.user.subscription_plan in self.PREMIUM_PLANS
        )

    def get_content(self):
        if self.has_full_access():
            return self._real.get_content()

        return self.article.content[:450].strip() + "..."

    def should_show_ads(self):
        return (
            not self.user.is_authenticated
            or self.user.subscription_plan == "free"
        )