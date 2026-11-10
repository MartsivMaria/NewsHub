from app.models.user import User


class UserRepository:

    @staticmethod
    def get_all():
        return User.query.all()

    @staticmethod
    def get_by_id(user_id):
        return User.query.get(user_id)

    @staticmethod
    def get_by_email(email):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def get_subscribers():
        return User.query.filter_by(
            newsletter_enabled=True
        ).all()

    @staticmethod
    def get_by_role(role):
        return User.query.filter_by(role=role).all()

    @staticmethod
    def get_by_username_or_email(username, email):
        return User.query.filter(
            (User.username == username) |
            (User.email == email)
        ).first()

    @staticmethod
    def get_by_identifier(identifier):
        return User.query.filter(
            (User.username == identifier) |
            (User.email == identifier.lower())
        ).first()

    @staticmethod
    def create(user):
        from app import db

        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def update():
        from app import db

        db.session.commit()

    @staticmethod
    def get_push_subscribers():
        return User.query.filter_by(push_enabled=True).all()