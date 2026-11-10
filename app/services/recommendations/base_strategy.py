from abc import ABC, abstractmethod


class RecommendationStrategy(ABC):

    @abstractmethod
    def get_recommendations(self, user, limit=5):
        pass