from flask import Flask
from configuration import Configuration
from flask_migrate import Migrate, init, migrate, upgrade
from models import db, Role, User, UserRole
from sqlalchemy_utils import database_exists, create_database, drop_database

app = Flask(__name__)
app.config.from_object(Configuration)

migrateObject = Migrate(app, db)

done = False

while(not done):
    try:
        if(not database_exists(app.config["SQLALCHEMY_DATABASE_URI"])):
                create_database(app.config["SQLALCHEMY_DATABASE_URI"])

        db.init_app(app)

        with app.app_context() as context:
            init()
            migrate(message="Production migration.")
            upgrade()
            rola1 = Role(name="admin")
            rola2 = Role(name="kupac")
            rola3 = Role(name="magacioner")
            admin = User(email="admin@admin.com", password="1", forename="admin", surname="admin")
            veza = UserRole(userID=1, roleID=1)
            db.session.add(rola1)
            db.session.add(rola2)
            db.session.add(rola3)
            db.session.add(admin)
            db.session.commit()
            db.session.add(veza)
            db.session.commit()
            done=True
    except Exception as error:
        print(error)
