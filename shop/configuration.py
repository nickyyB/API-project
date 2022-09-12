from datetime import timedelta
import os

databaseUrl = os.environ["DATABASE_URL"]

class Configuration():
    #SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@localhost/authentication"
    #SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@localhost/shop"
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://root:root@{databaseUrl}/shop"
    JWT_SECRET_KEY = "JWT_SECRET_KEY"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=3600)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    #REDIS_HOST = "localhost";
    REDIS_HOST = os.environ["REDIS_URL"]
    REDIS_PRODUCT_LIST = "products";