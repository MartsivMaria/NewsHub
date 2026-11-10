import os
import json

from flask import (
    Flask, render_template, request,
    redirect, url_for, flash
)
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager, login_user,
    logout_user, login_required, current_user
)
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)



db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    project_folder = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
    instance_folder = os.path.join(project_folder, "instance")

    os.makedirs(instance_folder, exist_ok=True)

    app = Flask(
        __name__,
        instance_path=instance_folder
    )
    from app.routes.api import api

    app.register_blueprint(api)

    app.config.from_object("config.Config")
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "login"
    login_manager.login_message = "Спочатку увійдіть у свій акаунт."
    login_manager.login_message_category = "warning"


    from app.models import User, Category, Article, Comment, Like, ArticleView, Notification, Digest, FollowedAuthor
    from app.services.recommendations.recommendation_context import RecommendationContext
    from app.services.recommendations.category_strategy import CategoryStrategy
    from app.services.recommendations.viewed_strategy import ViewedStrategy
    from app.services.recommendations.liked_strategy import LikedStrategy
    from app.services.article_proxy import ArticleProxy
    from app.services.digest_facade import DigestFacade
    from app.services.notifications import (
        BreakingNotificationFactory,
        DigestNotificationFactory,
        NewArticleNotificationFactory
    )
    from app.services.observers import (
        ArticlePublisher,
        NotificationObserver
    )
    from app.repositories import (
        ArticleRepository,
        CategoryRepository,
        NotificationRepository,
        DigestRepository,
        UserRepository,
        CommentRepository,
        LikeRepository,
        ArticleViewRepository,
        FollowedAuthorRepository
    )

    article_publisher = ArticlePublisher()
    article_publisher.attach(NotificationObserver())

    app.extensions["article_publisher"] = article_publisher

    @login_manager.user_loader
    def load_user(user_id):
        return UserRepository.get_by_id(int(user_id))

    with app.app_context():
        db.create_all()

        if CategoryRepository.count() == 0:
            categories = [
                Category(name="Технології", slug="technology"),
                Category(name="Освіта", slug="education"),
                Category(name="Наука", slug="science"),
                Category(name="Спорт", slug="sport"),
                Category(name="Культура", slug="culture"),
            ]

            CategoryRepository.create_many(categories)

        if ArticleRepository.count() == 0:
            category_map = {
                category.name: category
                for category in CategoryRepository.get_all()
            }

            articles_data = [
                {
                    "title": "Штучний інтелект змінює сучасні технології",
                    "description": (
                        "Нові цифрові рішення допомагають автоматизувати "
                        "завдання та відкривають нові можливості."
                    ),
                    "content": (
                        "Штучний інтелект стає важливою частиною "
                        "сучасного цифрового світу. Він допомагає "
                        "автоматизувати завдання та створює нові "
                        "можливості для людей і бізнесу."
                    ),
                    "category": "Технології",
                    "author": "Редакція NewsHub",
                    "image": (
                        "https://images.unsplash.com/"
                        "photo-1677442136019-21780ecad995"
                        "?auto=format&fit=crop&w=900&q=80"
                    ),
                    "featured": True,
                },
                {
                    "title": "Як цифрові сервіси змінюють наше повсякдення",
                    "description": (
                        "Онлайн-платформи стають важливою частиною "
                        "навчання, роботи та спілкування."
                    ),
                    "content": (
                        "Цифрові сервіси допомагають людям "
                        "отримувати інформацію, навчатися та "
                        "спілкуватися незалежно від місця перебування."
                    ),
                    "category": "Технології",
                    "author": "Марія Коваль",
                    "image": (
                        "https://images.unsplash.com/"
                        "photo-1516321318423-f06f85e504b3"
                        "?auto=format&fit=crop&w=900&q=80"
                    ),
                    "featured": False,
                },
                {
                    "title": "Освіта майбутнього: нові підходи до навчання",
                    "description": (
                        "Інтерактивні платформи допомагають "
                        "зробити навчання доступнішим."
                    ),
                    "content": (
                        "Цифрові інструменти змінюють способи "
                        "отримання знань і відкривають додаткові "
                        "можливості для учнів та викладачів."
                    ),
                    "category": "Освіта",
                    "author": "Олена Мельник",
                    "image": (
                        "https://images.unsplash.com/"
                        "photo-1503676260728-1c00da094a0b"
                        "?auto=format&fit=crop&w=900&q=80"
                    ),
                    "featured": False,
                },
                {
                    "title": "Наука відкриває нові горизонти",
                    "description": (
                        "Дослідники працюють над рішеннями, "
                        "які можуть змінити наше майбутнє."
                    ),
                    "content": (
                        "Наукові дослідження допомагають "
                        "краще зрозуміти світ і створювати "
                        "нові технології."
                    ),
                    "category": "Наука",
                    "author": "Андрій Бойко",
                    "image": (
                        "https://images.unsplash.com/"
                        "photo-1532094349884-543bc11b234d"
                        "?auto=format&fit=crop&w=900&q=80"
                    ),
                    "featured": False,
                },
                {
                    "title": "Світ спорту: головні події тижня",
                    "description": (
                        "Огляд цікавих спортивних подій "
                        "та досягнень спортсменів."
                    ),
                    "content": (
                        "Спортивні події об'єднують уболівальників "
                        "і демонструють результати наполегливої праці "
                        "спортсменів."
                    ),
                    "category": "Спорт",
                    "author": "Іван Петренко",
                    "image": (
                        "https://images.unsplash.com/"
                        "photo-1461896836934-ffe607ba8211"
                        "?auto=format&fit=crop&w=900&q=80"
                    ),
                    "featured": False,
                },
                {
                    "title": "Культурні події, на які варто звернути увагу",
                    "description": (
                        "Виставки, мистецькі проєкти та культурні "
                        "ініціативи, що об'єднують людей."
                    ),
                    "content": (
                        "Культурні заходи допомагають відкривати "
                        "нові ідеї, знайомитися з мистецтвом "
                        "і підтримувати творчі спільноти."
                    ),
                    "category": "Культура",
                    "author": "Софія Романюк",
                    "image": (
                        "https://images.unsplash.com/"
                        "photo-1513364776144-60967b0f800f"
                        "?auto=format&fit=crop&w=900&q=80"
                    ),
                    "featured": False,
                },
            ]

            for data in articles_data:
                category = category_map[data.pop("category")]
                featured = data.pop("featured")

                article = Article(
                    **data,
                    category=category,
                    is_featured=featured,
                )

            ArticleRepository.create(article)

    @app.context_processor
    def inject_notifications_count():
        if current_user.is_authenticated:
            unread_count = NotificationRepository.get_unread_count(
                current_user.id
            )
        else:
            unread_count = 0

        return {
            "unread_notifications_count": unread_count
        }

    @app.route("/")
    def index():
        show_ads = (
            not current_user.is_authenticated
            or current_user.subscription_plan == "free"
        )

        articles = ArticleRepository.get_for_homepage()
        breaking_articles = ArticleRepository.get_breaking()
        exclusive_articles = ArticleRepository.get_exclusive()

        categories = [
            "Усі новини",
            *[
                category.name
                for category in CategoryRepository.get_all()
            ],
        ]

        recommended_articles = []

        recommendation_strategies = {
            "category": CategoryStrategy(),
            "viewed": ViewedStrategy(),
            "liked": LikedStrategy()
        }

        selected_recommendation = request.args.get(
            "recommendation", "category"
        )

        if selected_recommendation not in recommendation_strategies:
            selected_recommendation = "category"

        if current_user.is_authenticated:
            recommendation_context = RecommendationContext(
                recommendation_strategies[selected_recommendation]
            )

            recommended_articles = recommendation_context.get_recommendations(
                current_user
            )

        return render_template(
            "index.html",
            articles=articles,
            categories=categories,
            recommended_articles=recommended_articles,
            exclusive_articles=exclusive_articles,
            show_ads=show_ads,
            breaking_articles=breaking_articles,
            selected_recommendation=selected_recommendation
        )

    @app.route("/article/<int:article_id>")
    def article(article_id):
        article = ArticleRepository.get_by_id(article_id)

        if article is None:
            flash("Новину не знайдено.", "error")
            return redirect(url_for("index"))

        article_proxy = ArticleProxy(article, current_user)

        show_ads = article_proxy.should_show_ads()
        has_full_access = article_proxy.has_full_access()
        display_content = article_proxy.get_content()

        ArticleRepository.increment_views(article)

        if current_user.is_authenticated:
            article_view = ArticleView(
                user_id=current_user.id,
                article_id=article.id
            )

            ArticleViewRepository.create(article_view)

        comments = CommentRepository.get_by_article(article.id)

        likes_count = ArticleRepository.get_likes_count(article.id)

        user_liked = False

        if current_user.is_authenticated:
            user_liked = LikeRepository.is_liked_by_user(
                current_user.id,
                article.id
            )

        is_following_author = False

        if current_user.is_authenticated:
            is_following_author = FollowedAuthorRepository.is_following(
                current_user.id,
                article.author.strip()
            )

        return render_template(
            "article.html",
            article=article,
            comments=comments,
            likes_count=likes_count,
            user_liked=user_liked,
            display_content=display_content,
            has_full_access=has_full_access,
            show_ads=show_ads,
            is_following_author=is_following_author
        )

    
    @app.route("/register", methods=["GET", "POST"])
    def register():
        if request.method == "POST":
            username = request.form.get("username", "").strip()
            email = request.form.get("email", "").strip().lower()
            password = request.form.get("password", "")

            if not username or not email or not password:
                flash("Заповніть усі поля.", "error")
                return render_template("register.html")

            if len(password) < 8:
                flash("Пароль повинен містити щонайменше 8 символів.", "error")
                return render_template("register.html")

            existing_user = UserRepository.get_by_username_or_email(
                username,
                email
            )

            if existing_user:
                flash("Це ім'я користувача або email вже зайняті.", "error")
                return render_template("register.html")

            user = User(
                username=username,
                email=email,
                password_hash=generate_password_hash(password)
            )

            UserRepository.create(user)

            flash("Реєстрація успішна! Тепер увійдіть.", "success")
            return redirect(url_for("login"))

        return render_template("register.html")

    @app.route("/logout", methods=["POST"])
    @login_required
    def logout():
        logout_user()
        flash("Ви вийшли з акаунта.", "info")
        return redirect(url_for("index"))

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            identifier = request.form.get("identifier", "").strip()
            password = request.form.get("password", "")

            user = UserRepository.get_by_identifier(identifier)

            if user and check_password_hash(
                user.password_hash, password
            ):
                login_user(user)
                flash("Раді бачити вас знову!", "success")
                return redirect(url_for("index"))

            flash("Неправильний email, логін або пароль.", "error")

        return render_template("login.html")


    @app.route("/profile", methods=["GET", "POST"])
    @login_required
    def profile():
        categories = CategoryRepository.get_all()

        if request.method == "POST":
            selected_ids = request.form.getlist("categories")

            current_user.favorite_categories = CategoryRepository.get_by_ids(
                selected_ids
            )

            UserRepository.update()

            flash("Улюблені теми успішно збережено!", "success")
            return redirect(url_for("profile"))

        followed_authors = FollowedAuthorRepository.get_followed_by_user(
            current_user.id
        )

        return render_template(
            "profile.html",
            categories=categories,
            followed_authors=followed_authors
    )

    @app.route("/profile/notifications", methods=["POST"])
    @login_required
    def update_notification_settings():
        current_user.newsletter_enabled = (
            request.form.get("newsletter_enabled") == "on"
        )

        current_user.push_enabled = (
            request.form.get("push_enabled") == "on"
        )

        UserRepository.update()

        flash("Налаштування сповіщень збережено!", "success")
        return redirect(url_for("profile"))

    @app.route("/plans")
    def plans():
        return render_template("plans.html")

    @app.route("/subscribe/<plan>", methods=["POST"])
    @login_required
    def subscribe(plan):
        available_plans = ["free", "premium", "student", "corporate"]

        if plan not in available_plans:
            flash("Такого тарифу не існує.", "error")
            return redirect(url_for("plans"))

        current_user.subscription_plan = plan
        UserRepository.update()

        flash("Ваш тариф успішно змінено!", "success")

        return redirect(url_for("plans"))

    @app.route("/article/<int:article_id>/save", methods=["POST"])
    @login_required
    def save_article(article_id):
        article = ArticleRepository.get_by_id(article_id)

        if article is None:
            flash("Новину не знайдено.", "error")
            return redirect(url_for("index"))

        if article not in current_user.saved_articles:
            current_user.saved_articles.append(article)
            UserRepository.update()
            flash("Новину додано до збережених!", "success")
        else:
            flash("Ця новина вже є у збережених.", "info")

        return redirect(url_for("article", article_id=article_id))

    @app.route("/article/<int:article_id>/remove", methods=["POST"])
    @login_required
    def remove_saved_article(article_id):
        article = ArticleRepository.get_by_id(article_id)

        if article is None:
            flash("Новину не знайдено.", "error")
            return redirect(url_for("index"))

        if article in current_user.saved_articles:
            current_user.saved_articles.remove(article)
            UserRepository.update()
            flash("Новину видалено зі збережених.", "success")

        return redirect(url_for("article", article_id=article_id))

    @app.route("/profile/saved/<int:article_id>/remove", methods=["POST"])
    @login_required
    def remove_saved_article_from_profile(article_id):
        article = ArticleRepository.get_by_id(article_id)

        if article and article in current_user.saved_articles:
            current_user.saved_articles.remove(article)
            UserRepository.update()

            flash("Новину видалено зі збережених.", "success")

        return redirect(url_for("profile"))


    @app.route("/article/<int:article_id>/like", methods=["POST"])
    @login_required
    def toggle_like(article_id):
        article = ArticleRepository.get_by_id(article_id)

        if article is None:
            flash("Новину не знайдено.", "error")
            return redirect(url_for("index"))

        existing_like = LikeRepository.get_by_user_and_article(
            current_user.id,
            article.id
        )

        if existing_like:
            LikeRepository.delete(existing_like)
            flash("Вподобання скасовано.", "info")
        else:
            like = Like(
                user_id=current_user.id,
                article_id=article.id
            )
            LikeRepository.create(like)
            flash("Вам сподобалася ця новина!", "success")

        return redirect(url_for("article", article_id=article.id))

    @app.route("/article/<int:article_id>/comment", methods=["POST"])
    @login_required
    def add_comment(article_id):
        article = ArticleRepository.get_by_id(article_id)

        if article is None:
            flash("Новину не знайдено.", "error")
            return redirect(url_for("index"))

        content = request.form.get("content", "").strip()

        if not content:
            flash("Коментар не може бути порожнім.", "error")
        elif len(content) > 1000:
            flash("Коментар не може містити більше 1000 символів.", "error")
        else:
            comment = Comment(
                content=content,
                user_id=current_user.id,
                article_id=article.id
            )

            CommentRepository.create(comment)
            flash("Коментар успішно додано!", "success")

        return redirect(url_for("article", article_id=article_id))

    @app.route("/comment/<int:comment_id>/delete", methods=["POST"])
    @login_required
    def delete_comment(comment_id):
        comment = CommentRepository.get_by_id(comment_id)

        if comment is None:
            flash("Коментар не знайдено.", "error")
            return redirect(url_for("index"))

        article_id = comment.article_id

        if comment.user_id != current_user.id:
            flash("Ти можеш видаляти лише власні коментарі.", "error")
        else:
            CommentRepository.delete(comment)
            flash("Коментар видалено.", "success")

        return redirect(url_for("article", article_id=article_id))

    @app.route("/notifications")
    @login_required
    def notifications():
        user_notifications = NotificationRepository.get_all_by_user(
            current_user.id
        )

        digest_articles = {}

        for notification in user_notifications:
            if notification.digest_id:
                digest = DigestRepository.get_by_id_and_user(
                    notification.digest_id,
                    current_user.id
                )

                if digest:
                    article_ids = json.loads(digest.article_ids)

                    articles = ArticleRepository.get_by_ids(article_ids)

                    digest_articles[notification.id] = articles

        return render_template(
            "notifications.html",
            notifications=user_notifications,
            digest_articles=digest_articles
        )

    @app.route("/notifications/<int:notification_id>/read", methods=["POST"])
    @login_required
    def mark_notification_read(notification_id):
        notification = NotificationRepository.get_by_id(
            notification_id,
            current_user.id
        )

        if notification:
            NotificationRepository.mark_as_read(notification)

            if notification.link:
                return redirect(notification.link)

        return redirect(url_for("notifications"))

    @app.route("/admin")
    @login_required
    def admin_panel():
        if current_user.role != "admin":
            flash("У вас немає доступу до цієї сторінки.", "error")
            return redirect(url_for("index"))

        return render_template("admin/dashboard.html")

    @app.route("/admin/articles")
    @login_required
    def admin_articles():
        if current_user.role != "admin":
            flash("У вас немає доступу до цієї сторінки.", "error")
            return redirect(url_for("index"))

        articles = ArticleRepository.get_all()

        return render_template(
            "admin/articles.html",
            articles=articles
        )


    @app.route("/admin/articles/add", methods=["GET", "POST"])
    @login_required
    def add_article():
        if current_user.role != "admin":
            flash("У вас немає доступу до цієї сторінки.", "error")
            return redirect(url_for("index"))

        categories = CategoryRepository.get_all()

        if request.method == "POST":
            title = request.form.get("title")
            description = request.form.get("description")
            content = request.form.get("content")
            author = request.form.get("author")
            image = request.form.get("image")
            category_id = request.form.get("category_id")

            is_breaking = request.form.get("is_breaking") == "on"
            is_exclusive = request.form.get("is_exclusive") == "on"

            article = Article(
                title=title,
                description=description,
                content=content,
                author=author,
                image=image,
                category_id=category_id,
                is_breaking=is_breaking,
                is_exclusive=is_exclusive
            )

            ArticleRepository.create(article)

            article_link = url_for(
                "article",
                article_id=article.id
            )

            article_publisher.notify(article, article_link)

            flash("Новину успішно додано!", "success")
            return redirect(url_for("admin_articles"))

        return render_template(
            "admin/add_article.html",
            categories=categories
        )

    @app.route("/admin/articles/<int:article_id>/edit", methods=["GET", "POST"])
    @login_required
    def edit_article(article_id):
        if current_user.role != "admin":
            flash("У вас немає доступу до цієї сторінки.", "error")
            return redirect(url_for("index"))

        article = ArticleRepository.get_by_id(article_id)

        if not article:
            flash("Новину не знайдено.", "error")
            return redirect(url_for("admin_articles"))

        categories = CategoryRepository.get_all()

        if request.method == "POST":
            article.title = request.form.get("title")
            article.description = request.form.get("description")
            article.content = request.form.get("content")
            article.author = request.form.get("author")
            article.image = request.form.get("image")
            article.category_id = request.form.get("category_id")
            article.is_breaking = request.form.get("is_breaking") == "on"
            article.is_exclusive = request.form.get("is_exclusive") == "on"

            ArticleRepository.update()

            flash("Новину успішно оновлено!", "success")
            return redirect(url_for("admin_articles"))

        return render_template(
            "admin/edit_article.html",
            article=article,
            categories=categories
        )

    @app.route("/admin/articles/<int:article_id>/delete", methods=["POST"])
    @login_required
    def delete_article(article_id):
        if current_user.role != "admin":
            flash("У вас немає доступу до цієї сторінки.", "error")
            return redirect(url_for("index"))

        article = ArticleRepository.get_by_id(article_id)

        if article is None:
            flash("Новину не знайдено.", "error")
            return redirect(url_for("admin_articles"))

        db.session.delete(article)
        db.session.commit()

        flash("Новину успішно видалено!", "success")
        return redirect(url_for("admin_articles"))

    @app.route("/admin/generate-digest", methods=["POST"])
    @login_required
    def generate_digest():
        if current_user.role != "admin":
            flash("У вас немає доступу до цієї сторінки.", "error")
            return redirect(url_for("index"))

        digest_facade = DigestFacade()

        sent_count = digest_facade.generate(
            notification_link=url_for("notifications")
        )

        flash(
            f"Дайджест сформовано для {sent_count} користувачів!",
            "success"
        )

        return redirect(url_for("admin_panel"))

    @app.route("/article/<int:article_id>/follow-author", methods=["POST"])
    @login_required
    def follow_author(article_id):
        article = ArticleRepository.get_by_id(article_id)

        if article is None:
            flash("Новину не знайдено.", "error")
            return redirect(url_for("index"))

        author_name = article.author.strip()

        if FollowedAuthorRepository.is_following(
            current_user.id, author_name
        ):
            flash("Ви вже стежите за цим автором.", "info")
        else:
            FollowedAuthorRepository.follow(
                current_user.id, author_name
            )
            flash(
                f"Ви почали стежити за автором {author_name}!",
                "success"
            )

        return redirect(url_for("article", article_id=article_id))


    @app.route("/article/<int:article_id>/unfollow-author", methods=["POST"])
    @login_required
    def unfollow_author(article_id):
        article = ArticleRepository.get_by_id(article_id)

        if article is None:
            flash("Новину не знайдено.", "error")
            return redirect(url_for("index"))

        author_name = article.author.strip()

        FollowedAuthorRepository.unfollow(
            current_user.id, author_name
        )

        flash(
            f"Ви перестали стежити за автором {author_name}.",
            "info"
        )

        return redirect(url_for("article", article_id=article_id))

    @app.route("/profile/unfollow-author", methods=["POST"])
    @login_required
    def unfollow_author_from_profile():
        author_name = request.form.get("author_name", "").strip()

        if author_name:
            FollowedAuthorRepository.unfollow(
                current_user.id,
                author_name
            )
            flash(
                f"Ви відписалися від автора {author_name}.",
                "success"
            )

        return redirect(url_for("profile"))

    return app

    