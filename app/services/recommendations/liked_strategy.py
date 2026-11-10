from app.services.recommendations.base_strategy import RecommendationStrategy
from app.repositories import ArticleRepository


class LikedStrategy(RecommendationStrategy):

    def get_recommendations(self, user, limit=5):
        category_ids = ArticleRepository.get_liked_category_ids(
            user.id
        )

        if not category_ids:
            return []

        viewed_article_ids = ArticleRepository.get_viewed_article_ids(
            user.id
        )

        return ArticleRepository.get_recommended(
            category_ids,
            viewed_article_ids=viewed_article_ids,
            limit=limit
        )