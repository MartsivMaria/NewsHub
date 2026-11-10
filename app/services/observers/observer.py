from abc import ABC, abstractmethod


class ArticleObserver(ABC):

    @abstractmethod
    def update(self, article, link):
        pass