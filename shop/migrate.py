from flask import Flask
from configuration import Configuration
from flask_migrate import Migrate, init, migrate, upgrade
from models import db, Status
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
            migrate(message="Production migration shop.")
            upgrade()
            db.session.commit()
            status1 = Status(name="Uspesna")
            status2 = Status(name="Na cekanju")
            db.session.add(status1)
            db.session.add(status2)
            db.session.commit()
            done = True
    except Exception as error:
        print(error)
