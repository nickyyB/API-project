from datetime import timedelta

import os

databaseUrl = os.environ["DATABASE_URL"]

class Configuration():
    #SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@authenticationDatabase/authentication"
    #SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@localhost:3307/authentication"
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://root:root@{databaseUrl}/authentication"
    JWT_SECRET_KEY = "JWT_SECRET_KEY"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=3600)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)