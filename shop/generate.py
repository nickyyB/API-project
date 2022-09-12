from flask import Flask
from models import db, Status
from sqlalchemy_utils import database_exists
from configuration import Configuration

app = Flask(__name__)
app.config.from_object(Configuration)


while True:
    if (not database_exists(Configuration.SQLALCHEMY_DATABASE_URI)):
        print("Greska dodavanje statusa, nema baze")
        break
    else:
        db.init_app(app)
        with app.app_context() as contex:
            status1 = Status (name="Uspesna")
            status2 = Status (name="Na cekanju")
            db.session.add(status1)
            db.session.add(status2)
            db.session.commit()
            print("Dodati Statusi Porudzbine")
    break
