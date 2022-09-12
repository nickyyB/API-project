from flask import Flask
#from shop.configuration import Configuration
#from shop.models import db, Product, Category, ProductCategory, Order, OrderStatus, ProductOrder, Status
from configuration import Configuration
from models import db, Product, Category, ProductCategory, Order, OrderStatus, ProductOrder, Status
from redis import Redis
from sqlalchemy import and_, update
from pprint import pprint

app = Flask ( __name__ )
app.config.from_object ( Configuration )
db.init_app(app)

if __name__ == "__main__":
    with Redis(host=Configuration.REDIS_HOST) as redis:
        while True:
            with app.app_context() as context:
                r = redis.blpop(Configuration.REDIS_PRODUCT_LIST)[1].decode("utf-8")
                if not type(r) == str:
                    continue
                row = r.split(',')
                categories = row[0].split('|')
                product = Product.query.filter(Product.name == row[1]).first()
                if not product:
                    product = Product(name=row[1], price=float(row[3]), number=int(row[2]))
                    db.session.add(product)
                    db.session.commit()
                    for category in categories:
                        c = Category.query.filter(Category.name==category).first()
                        if(not c):
                            c = Category(name = category)
                            db.session.add(c)
                            db.session.commit()
                        pc = ProductCategory(productID=product.id, categoryID=c.id)
                        db.session.add(pc)
                        db.session.commit()
                else:
                    allOK=True
                    for category in categories:
                        if not any(cat.name == category for cat in product.categories):
                            allOK=False
                    if allOK:
                        new_price = (product.number * product.price + int(row[2]) * float(row[3])) / (product.number + int(row[2]))
                        product.price = new_price
                        product.number = product.number + int(row[2])
                        db.session.commit()

                        pendingOrders = Status.query.join(OrderStatus).join(Order).join(ProductOrder).join(Product).filter(Status.id==2,Product.id==product.id,ProductOrder.requested - ProductOrder.received > 0).group_by(Order.id)

                        for order in pendingOrders:
                            product_order = ProductOrder.query.join(Order).filter(ProductOrder.productID == product.id,Order.id == order.id).first()
                            #print(product_order)
                            if product_order is not None:
                                if product_order.received + product.number > product_order.requested:
                                    product.number = product.number - (product_order.requested-product_order.received)
                                    product_order.received = product_order.requested
                                    query = OrderStatus.query.join(Order).filter(OrderStatus.orderID==order.id).first()
                                    query.statusID=1
                                    #print(query)
                                else:
                                    product_order.received += product.number
                                    product.number = 0

                                db.session.commit()
                                db.session.add(product)
                                db.session.add(order)
                                db.session.add(product_order)
                                db.session.commit()

                                db.session.commit()
                                stmt = ProductOrder.query.filter(ProductOrder.requested-ProductOrder.received > 0).all()
                                for statement in stmt:
                                    #print(statement)
                                    q = OrderStatus.query.filter(OrderStatus.orderID==statement.orderID).first()
                                    #print(q)
                                    if q.statusID != 2:
                                        q.statusID=2
                                        db.session.commit()

                db.session.commit()
                stmt = ProductOrder.query.filter(ProductOrder.requested - ProductOrder.received > 0).all()
                for statement in stmt:
                    quantity = statement.requested-statement.received - 1
                    q = Product.query.filter(statement.productID==Product.id, quantity<Product.number).first()
                    if q is not None:
                        statement.recieved = statement.requested
                        q.number = q.number - (statement.requested-statement.received)
                        query = OrderStatus.query.join(Order).filter(OrderStatus.orderID == order.id).first()
                        query.statusID = 1
                db.session.commit()
                db.session.commit()
                stmt = ProductOrder.query.filter(ProductOrder.requested - ProductOrder.received > 0).all()
                for statement in stmt:
                    #print(statement)
                    q = OrderStatus.query.filter(OrderStatus.orderID == statement.orderID).first()
                    #print(q)
                    if q.statusID != 2:
                        q.statusID = 2
                        db.session.commit()