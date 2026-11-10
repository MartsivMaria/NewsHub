class ArticlePublisher:
    """Клас, який повідомляє спостерігачів про публікацію новини."""

    def __init__(self):
        self._observers = []

    def attach(self, observer):
        """Підключає спостерігача."""
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer):
        """Відключає спостерігача."""
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self, article, link):
        """Повідомляє всіх підключених спостерігачів."""
        for observer in self._observers:
            observer.update(article, link)