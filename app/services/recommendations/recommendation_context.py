from app.services.recommendations.base_strategy import RecommendationStrategy


class RecommendationContext:

    def __init__(self, strategy: RecommendationStrategy):
        self.strategy = strategy

    def set_strategy(self, strategy: RecommendationStrategy):
        self.strategy = strategy

    def get_recommendations(self, user, limit=5):
        return self.strategy.get_recommendations(user, limit)