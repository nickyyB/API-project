from flask import Flask
from models import db, Role, User, UserRole
from sqlalchemy_utils import database_exists
from configuration import Configuration

app = Flask(__name__)
app.config.from_object(Configuration)


while True:
    if (not database_exists(Configuration.SQLALCHEMY_DATABASE_URI)):
        print("Greska dodavanje rola, nema baze")
        break
    else:
        db.init_app(app)
        with app.app_context() as contex:
            rola1 = Role (name = "admin")
            rola2 = Role (name = "kupac")
            rola3 = Role (name = "magacioner")
            admin = User (email = "admin@admin.com", password = "1", forename = "admin", surname = "admin")
            veza = UserRole(userID = 1, roleID = 1)
            db.session.add(rola1)
            db.session.add(rola2)
            db.session.add(rola3)
            db.session.add(admin)
            db.session.commit()
            db.session.add(veza)
            db.session.commit()
            print("Dodate Role i Admin")
    break
