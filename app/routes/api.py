from functools import wraps

from flask import Blueprint, jsonify, request, current_app, url_for
from flask_login import current_user

from app.models.article import Article

from app.repositories import (
    ArticleRepository,
    CategoryRepository
)
from app.services.article_proxy import ArticleProxy

api = Blueprint("api", __name__, url_prefix="/api")



def serialize_article(article):
    return {
        "id": article.id,
        "title": article.title,
        "description": article.description,
        "author": article.author,
        "image": article.image,
        "category_id": article.category_id,
        "published_at": (
            article.published_at.isoformat()
            if article.published_at else None
        ),
        "views": article.views,
        "is_featured": article.is_featured,
        "is_exclusive": article.is_exclusive,
        "is_breaking": article.is_breaking
    }


@api.route("/articles", methods=["GET"])
def get_articles():
    articles = ArticleRepository.get_all()

    return jsonify({
        "articles": [
            serialize_article(article)
            for article in articles
        ]
    }), 200


@api.route("/articles/<int:article_id>", methods=["GET"])
def get_article(article_id):
    article = ArticleRepository.get_by_id(article_id)

    if article is None:
        return jsonify({
            "error": "Новину не знайдено."
        }), 404

    article_proxy = ArticleProxy(article, current_user)

    data = serialize_article(article)
    data["content"] = article_proxy.get_content()
    data["has_full_access"] = article_proxy.has_full_access()
    data["show_ads"] = article_proxy.should_show_ads()

    return jsonify(data), 200

def admin_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated:
            return jsonify({
                "error": "Необхідно авторизуватися."
            }), 401

        if current_user.role != "admin":
            return jsonify({
                "error": "Недостатньо прав доступу."
            }), 403

        return view(*args, **kwargs)

    return wrapped

def validate_article_data(data, partial=False):
    if not isinstance(data, dict):
        return None, "Потрібно передати JSON."

    allowed_fields = {
        "title",
        "description",
        "content",
        "author",
        "image",
        "category_id",
        "is_featured",
        "is_exclusive",
        "is_breaking"
    }

    if set(data) - allowed_fields:
        return None, "Передано невідомі поля."

    required_fields = [
        "title",
        "description",
        "content",
        "author",
        "category_id"
    ]

    if not partial:
        missing = [
            field for field in required_fields
            if field not in data
        ]

        if missing:
            return None, f"Не заповнені поля: {missing}"

    updates = {}

    text_fields = ["title", "description", "content", "author"]

    for field in text_fields:
        if field in data:
            if not isinstance(data[field], str) or not data[field].strip():
                return None, f"Некоректне значення поля {field}."

            updates[field] = data[field].strip()

    if not partial:
        updates["image"] = data.get("image")
        updates["is_featured"] = data.get("is_featured", False)
        updates["is_exclusive"] = data.get("is_exclusive", False)
        updates["is_breaking"] = data.get("is_breaking", False)

    if "image" in data:
        if data["image"] is not None and not isinstance(data["image"], str):
            return None, "Некоректне значення image."
        updates["image"] = data["image"]

    if "category_id" in data:
        try:
            category_id = int(data["category_id"])
        except (ValueError, TypeError):
            return None, "Некоректний ID категорії."

        if not CategoryRepository.get_by_ids([category_id]):
            return None, "Такої категорії не існує."

        updates["category_id"] = category_id

    boolean_fields = [
        "is_featured",
        "is_exclusive",
        "is_breaking"
    ]

    for field in boolean_fields:
        if field in data:
            if not isinstance(data[field], bool):
                return None, f"Поле {field} повинно мати значення true або false."

            updates[field] = data[field]

    if partial and not updates:
        return None, "Не передано жодного поля для оновлення."

    return updates, None

def validate_article_data(data, partial=False):
    if not isinstance(data, dict):
        return None, "Потрібно передати JSON."

    allowed_fields = {
        "title",
        "description",
        "content",
        "author",
        "image",
        "category_id",
        "is_featured",
        "is_exclusive",
        "is_breaking"
    }

    if set(data) - allowed_fields:
        return None, "Передано невідомі поля."

    required_fields = [
        "title",
        "description",
        "content",
        "author",
        "category_id"
    ]

    if not partial:
        missing = [
            field for field in required_fields
            if field not in data
        ]

        if missing:
            return None, f"Не заповнені поля: {missing}"

    updates = {}

    text_fields = ["title", "description", "content", "author"]

    for field in text_fields:
        if field in data:
            if not isinstance(data[field], str) or not data[field].strip():
                return None, f"Некоректне значення поля {field}."

            updates[field] = data[field].strip()

    if not partial:
        updates["image"] = data.get("image")
        updates["is_featured"] = data.get("is_featured", False)
        updates["is_exclusive"] = data.get("is_exclusive", False)
        updates["is_breaking"] = data.get("is_breaking", False)

    if "image" in data:
        if data["image"] is not None and not isinstance(data["image"], str):
            return None, "Некоректне значення image."
        updates["image"] = data["image"]

    if "category_id" in data:
        try:
            category_id = int(data["category_id"])
        except (ValueError, TypeError):
            return None, "Некоректний ID категорії."

        if not CategoryRepository.get_by_ids([category_id]):
            return None, "Такої категорії не існує."

        updates["category_id"] = category_id

    boolean_fields = [
        "is_featured",
        "is_exclusive",
        "is_breaking"
    ]

    for field in boolean_fields:
        if field in data:
            if not isinstance(data[field], bool):
                return None, f"Поле {field} повинно мати значення true або false."

            updates[field] = data[field]

    if partial and not updates:
        return None, "Не передано жодного поля для оновлення."

    return updates, None

@api.route("/articles", methods=["POST"])
@admin_required
def create_article():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": "Потрібно передати JSON."
        }), 400

    required_fields = [
        "title",
        "description",
        "content",
        "author",
        "category_id"
    ]

    missing_fields = [
        field for field in required_fields
        if field not in data or data[field] is None
        or (isinstance(data[field], str) and not data[field].strip())
    ]

    if missing_fields:
        return jsonify({
            "error": "Не заповнені обов'язкові поля.",
            "fields": missing_fields
        }), 400

    try:
        category_id = int(data["category_id"])
    except (ValueError, TypeError):
        return jsonify({
            "error": "Некоректний ID категорії."
        }), 400

    categories = CategoryRepository.get_all()

    if not any(category.id == category_id for category in categories):
        return jsonify({
            "error": "Такої категорії не існує."
        }), 400

    for field in ("is_featured", "is_exclusive", "is_breaking"):
        if field in data and not isinstance(data[field], bool):
            return jsonify({
                "error": f"Поле {field} повинно мати значення true або false."
            }), 400

    article = Article(
        title=data["title"].strip(),
        description=data["description"].strip(),
        content=data["content"].strip(),
        author=data["author"].strip(),
        image=data.get("image"),
        category_id=category_id,
        is_featured=data.get("is_featured", False),
        is_exclusive=data.get("is_exclusive", False),
        is_breaking=data.get("is_breaking", False)
    )

    ArticleRepository.create(article)

    article_link = url_for(
        "article",
        article_id=article.id
    )

    current_app.extensions["article_publisher"].notify(
        article,
        article_link
    )

    return jsonify({
        "message": "Новину успішно створено.",
        "article": serialize_article(article)
    }), 201

@api.route("/articles/<int:article_id>", methods=["PUT"])
@admin_required
def update_article(article_id):
    article = ArticleRepository.get_by_id(article_id)

    if article is None:
        return jsonify({
            "error": "Новину не знайдено."
        }), 404

    data = request.get_json(silent=True)

    updates, error = validate_article_data(data)

    if error:
        return jsonify({
            "error": error
        }), 400

    for field, value in updates.items():
        setattr(article, field, value)

    ArticleRepository.update()

    result = serialize_article(article)
    result["content"] = article.content

    return jsonify({
        "message": "Новину повністю оновлено.",
        "article": result
    }), 200


@api.route("/articles/<int:article_id>", methods=["PATCH"])
@admin_required
def patch_article(article_id):
    article = ArticleRepository.get_by_id(article_id)

    if article is None:
        return jsonify({"error": "Новину не знайдено."}), 404

    data = request.get_json(silent=True)

    updates, error = validate_article_data(data, partial=True)

    if error:
        return jsonify({"error": error}), 400

    for field, value in updates.items():
        setattr(article, field, value)

    ArticleRepository.update()

    result = serialize_article(article)
    result["content"] = article.content

    return jsonify({
        "message": "Новину частково оновлено.",
        "article": result
    }), 200

@api.route("/articles/<int:article_id>", methods=["DELETE"])
@admin_required
def delete_article_api(article_id):
    article = ArticleRepository.get_by_id(article_id)

    if article is None:
        return jsonify({
            "error": "Новину не знайдено."
        }), 404

    ArticleRepository.delete(article)

    return jsonify({
        "message": "Новину успішно видалено.",
        "article_id": article_id
    }), 200