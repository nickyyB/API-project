from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class UserRole(db.Model):
    __tablename__ = "userrole"

    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey("users.id", ondelete ="CASCADE"), nullable = False)
    roleID = db.Column(db.Integer, db.ForeignKey("roles.id", ondelete ="CASCADE"), nullable = False)

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    forename = db.Column(db.String(256), nullable=False)
    surname = db.Column(db.String(256), nullable=False)

    roles = db.relationship("Role", secondary=UserRole.__table__, back_populates="users", cascade="all, delete")

class Role(db.Model):
    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False, unique=True)

    users = db.relationship("User", secondary=UserRole.__table__, back_populates="roles", cascade="all, delete")

    def __repr__(self):
        return self.name