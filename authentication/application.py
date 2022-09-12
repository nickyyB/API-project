import json, re

from flask import Flask, request, Response, jsonify
from configuration import Configuration
from models import db, User, UserRole
from roleDecorator import roleCheck
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, create_refresh_token, get_jwt, get_jwt_identity
from sqlalchemy import and_

app = Flask(__name__)
app.config.from_object(Configuration)

@app.route("/register", methods=["POST"])
def register():
    forename = request.json.get("forename", "")
    surname = request.json.get("surname", "")
    email = request.json.get("email", "")
    password = request.json.get("password", "")
    buyer = request.json.get("isCustomer", "")

    #PROVERA DA LI JE PRAZNO NEKO POLJE
    if (len(forename) == 0): return Response(json.dumps({"message": "Field forename is missing."}), status=400)
    if (len(surname) == 0): return Response(json.dumps({"message": "Field surname is missing."}), status=400)
    if (len(email)==0): return Response(json.dumps({"message":"Field email is missing."}), status=400)
    if (len(password) == 0): return Response(json.dumps({"message":"Field password is missing."}), status=400)
    if (not isinstance(buyer, bool)): return Response(json.dumps({"message":"Field isCustomer is missing."}), status=400)

    #PROVERA DA LI JE MAIL ISPRAVAN
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if(not re.fullmatch(regex, email)):
        return Response(json.dumps({"message":"Invalid email."}), status=400)

    #PROVERA DA LI JE SIFRA U DOBROM FORMATU
    if(len(password)<8 or not any(char.isdigit() for char in password) or password.islower() or password.isupper()):
        return Response(json.dumps({"message":"Invalid password."}), status=400)

    #PROVERA DA LI POSTOJI KORISNIK VEC U BAZI
    if(User.query.filter(User.email == email).first()):
        return Response(json.dumps({"message":"Email already exists."}), status=400)

    user = User (email=email, password=password, forename=forename, surname=surname)
    db.session.add(user)
    db.session.commit()
    if(buyer==True):
        userRole = UserRole(userID=user.id, roleID=2)
    else:
        userRole = UserRole(userID=user.id, roleID=3)
    db.session.add(userRole)
    db.session.commit()

    return Response(status=200)


jwt=JWTManager(app)

@app.route("/login", methods=["POST"])
def login():
    email = request.json.get("email", "")
    password = request.json.get("password", "")

    #PROVERA DA LI JE PRAZNO NEKO POLJE
    if (len(email)==0): return Response(json.dumps({"message":"Field email is missing."}), status=400)
    if (len(password) == 0): return Response(json.dumps({"message":"Field password is missing."}), status=400)

    #PROVERA DA LI JE MAIL ISPRAVAN
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if (not re.fullmatch(regex, email)):
        return Response(json.dumps({"message": "Invalid email."}), status=400)


    user = User.query.filter(and_(User.email==email,User.password==password)).first()
    if(not user):
        return Response(json.dumps({"message":"Invalid credentials."}), status=400)

    additionalClaims = {
        "forename": user.forename,
        "surname": user.surname,
        "roles": [str(role) for role in user.roles]
    }
    accessToken = create_access_token(identity=user.email, additional_claims=additionalClaims)
    refreshToken = create_refresh_token(identity=user.email, additional_claims=additionalClaims)
    #return Response(accessToken, status=200)
    return jsonify(accessToken=accessToken, refreshToken=refreshToken)

@app.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    refreshClaims = get_jwt()

    additionalClaims = {
        "forename": refreshClaims["forename"],
        "surname": refreshClaims["surname"],
        "roles": refreshClaims["roles"]
    }
    return jsonify(accessToken=create_access_token(identity=identity, additional_claims=additionalClaims)), 200

@app.route("/delete", methods=["POST"])
@roleCheck ( role = "admin" )
def delete():
    email = request.json.get("email", "")
    if(len(email)==0):
        return Response(json.dumps({"message":"Field email is missing."}), status=400)

    # PROVERA DA LI JE MAIL ISPRAVAN
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if (not re.fullmatch(regex, email)):
        return Response(json.dumps({"message": "Invalid email."}), status=400)

    user = User.query.filter(User.email == email).first()
    if user:
        User.query.filter(User.email == email).delete()
        db.session.commit()
        return Response(status=200)
    return jsonify({"message": "Unknown user."}), 400

@app.route("/", methods=["GET"])
def index():
    return "Hello World!"

if(__name__=="__main__"):
    db.init_app(app)
    app.run(debug=True, host="0.0.0.0", port=5002)