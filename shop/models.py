from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class ProductCategory(db.Model):
    __tablename__ = "productcategory"

    id = db.Column(db.Integer, primary_key=True)
    productID = db.Column(db.Integer, db.ForeignKey("products.id", ondelete ="CASCADE"), nullable=False)
    categoryID = db.Column(db.Integer, db.ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)

    def __repr__(self):
        return "(PRODUCTCATEGORY {}, {}, {})".format(self.id, self.productID, self.categoryID)

class ProductOrder(db.Model):
    __tablename__ = "productorder"

    id = db.Column(db.Integer, primary_key=True)
    orderID =  db.Column(db.Integer, db.ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    productID = db.Column(db.Integer, db.ForeignKey("products.id", ondelete="CASCADE"), nullable=False)

    priceATM = db.Column(db.Float, nullable=False)
    received = db.Column(db.Integer, nullable=False)
    requested = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "(PRODUCTORDER {}, {}, {}, {}, {}, {})".format(self.id, self.orderID, self.productID, self.priceATM, self.received, self.requested)

class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False, unique=True)

    products = db.relationship("Product", secondary=ProductCategory.__tablename__, back_populates="categories")

    def __repr__(self):
        return "(CATEGORY {}, {})".format(self.id, self.name)

class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    price = db.Column(db.Float, nullable=False)
    number = db.Column(db.Integer, nullable=False)

    categories = db.relationship("Category", secondary=ProductCategory.__tablename__, back_populates="products")
    orders = db.relationship("Order", secondary=ProductOrder.__tablename__, back_populates="products")

    def __repr__(self):
        return "(PRODUCT {}, {}, {}, {})".format(self.id, self.name, self.price, self.number)

class OrderStatus(db.Model):
    __tablename__ = "orderstatus"

    id = db.Column(db.Integer, primary_key=True)
    orderID = db.Column(db.Integer, db.ForeignKey("orders.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    statusID = db.Column(db.Integer, db.ForeignKey("status.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)

    def __repr__(self):
        return "(ORDERSTATUS {}, {}, {})".format(self.id, self.orderID, self.statusID)

class Status(db.Model):
    __tablename__ = "status"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False, unique=True)

    orders = db.relationship("Order", secondary=OrderStatus.__tablename__, back_populates="status")

    def __repr__(self):
        return "(STATUS {}, {})".format(self.id, self.name)

class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    priceTOTAL = db.Column(db.Float, nullable=False)
    time = db.Column(db.TIMESTAMP, nullable=False)
    email = db.Column(db.String(256), nullable=False)

    status = db.relationship("Status", secondary=OrderStatus.__tablename__, back_populates="orders")
    products = db.relationship("Product", secondary=ProductOrder.__tablename__, back_populates="orders")

    def __repr__(self):
        return "(ORDER {}, {}, {}, {})".format(self.id, self.priceTOTAL, self.time, self.email)