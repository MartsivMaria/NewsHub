from app import create_app, db
from app.models import User

app = create_app()

with app.app_context():
    user = User.query.filter_by(username="maria").first()

    if user:
        user.role = "admin"
        db.session.commit()
        print("Користувача maria призначено адміністратором!")
    else:
        print("Користувача maria не знайдено.")