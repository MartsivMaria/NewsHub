from datetime import datetime

from app import create_app, db
from app.models import User, Category, Article


app = create_app()
client = app.test_client()


def check_response(response, expected_status, test_name):
    print(f"\n{test_name}")

    print(f"Статус: {response.status_code}")

    if response.status_code != expected_status:
        print("ПОМИЛКА!")
        print(response.get_json(silent=True))
        raise AssertionError(
            f"Очікувався статус {expected_status}"
        )

    print("ТЕСТ ПРОЙДЕНО!")


def run_tests():
    created_article_id = None
    test_title = (
        "API TEST " + datetime.now().strftime("%Y%m%d%H%M%S")
    )

    push_user_ids = []

    try:
        with app.app_context():

            # Знаходимо адміністратора
            admin = User.query.filter_by(role="admin").first()
            category = Category.query.first()

            if admin is None:
                raise RuntimeError("У базі немає адміністратора.")

            if category is None:
                raise RuntimeError("У базі немає категорій.")

            # Тимчасово вимикаємо сповіщення,
            # щоб тестова публікація не створювала зайвих сповіщень
            push_users = User.query.filter_by(
                push_enabled=True
            ).all()

            push_user_ids = [user.id for user in push_users]

            for user in push_users:
                user.push_enabled = False

            db.session.commit()

            # Авторизація адміністратора для тестових запитів
            with client.session_transaction() as session:
                session["_user_id"] = str(admin.get_id())
                session["_fresh"] = True

            # 1. GET — отримання всіх новин
            response = client.get("/api/articles")

            check_response(
                response,
                200,
                "1. GET — отримання всіх новин"
            )

            # Дані для тестової новини
            article_data = {
                "title": test_title,
                "description": "Тестовий опис новини.",
                "content": "Тестовий текст новини.",
                "author": "API Tester",
                "image": "",
                "category_id": category.id,
                "is_featured": False,
                "is_exclusive": False,
                "is_breaking": False
            }

            # 2. POST — створення новини
            response = client.post(
                "/api/articles",
                json=article_data
            )

            check_response(
                response,
                201,
                "2. POST — створення новини"
            )

            created_article_id = response.get_json()["article"]["id"]

            print("Створено новину з ID:", created_article_id)

            # 3. GET — отримання конкретної новини
            response = client.get(
                f"/api/articles/{created_article_id}"
            )

            check_response(
                response,
                200,
                "3. GET — отримання однієї новини"
            )

            # 4. PUT — повне оновлення новини
            updated_data = {
                "title": "Оновлена тестова новина",
                "description": "Оновлений опис.",
                "content": "Оновлений текст новини.",
                "author": "API Tester",
                "image": "",
                "category_id": category.id,
                "is_featured": True,
                "is_exclusive": False,
                "is_breaking": False
            }

            response = client.put(
                f"/api/articles/{created_article_id}",
                json=updated_data
            )

            check_response(
                response,
                200,
                "4. PUT — повне оновлення новини"
            )

            # 5. PATCH — часткове оновлення новини
            response = client.patch(
                f"/api/articles/{created_article_id}",
                json={
                    "title": "Частково оновлена новина"
                }
            )

            check_response(
                response,
                200,
                "5. PATCH — часткове оновлення новини"
            )

            # 6. DELETE — видалення новини
            response = client.delete(
                f"/api/articles/{created_article_id}"
            )

            check_response(
                response,
                200,
                "6. DELETE — видалення новини"
            )

            # Додаткова перевірка: новина вже не існує
            response = client.get(
                f"/api/articles/{created_article_id}"
            )

            check_response(
                response,
                404,
                "7. GET — перевірка видалення новини"
            )

    finally:
        # Видаляємо тестову новину, якщо тест перервався
        with app.app_context():
            test_article = Article.query.filter_by(
                title=test_title
            ).first()

            if test_article:
                db.session.delete(test_article)

            # Повертаємо налаштування сповіщень користувачів
            for user_id in push_user_ids:
                user = db.session.get(User, user_id)

                if user:
                    user.push_enabled = True

            db.session.commit()

    print("УСІ REST API ТЕСТИ УСПІШНО ПРОЙДЕНІ!")


if __name__ == "__main__":
    run_tests()