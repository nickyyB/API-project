from flask import Flask, Response
from configuration import Configuration
from models import db, Product, ProductOrder, Category, ProductCategory
#from shop.configuration import Configuration
#from shop.models import db, Product, ProductOrder, Category, ProductCategory
from adminDecorator import roleCheck
from flask_jwt_extended import JWTManager
import json, pprint
from sqlalchemy import func

app = Flask ( __name__ )
app.config.from_object ( Configuration )
jwt = JWTManager ( app )

@app.route("/productStatistics", methods=["GET"])
@roleCheck(role="admin")
def productStatistics():
    statistics=[]
    product_orders = ProductOrder.query.group_by(ProductOrder.productID).with_entities(ProductOrder.productID, func.sum(ProductOrder.requested), func.sum(ProductOrder.requested) - func.sum(ProductOrder.received)).all()
    for product in product_orders:
        statistics.append({
            "name": Product.query.filter_by(id=product[0]).first().name,
            "sold": int(product[1]),
            "waiting": int(product[2])
        })

    return Response(json.dumps({"statistics" : statistics}), status=200)

@app.route("/categoryStatistics", methods=["GET"])
@roleCheck(role="admin")
def categoryStatistics():
    statistics = []

    total_requested = func.coalesce(func.sum(ProductOrder.requested), 0)
    categories = Category.query.outerjoin(ProductCategory, Category.id==ProductCategory.categoryID).outerjoin(ProductOrder, ProductCategory.productID==ProductOrder.productID).group_by(Category.id).order_by(total_requested.desc()).order_by(Category.name).with_entities(Category.name).all()

    for category in categories:
        statistics.append(category[0])
    return Response(json.dumps({"statistics" : statistics}), status=200)


@app.route("/modifikacija", methods=["GET"])
def modifikacija():
    statistics=[]

    product_orders = Category.query.outerjoin(ProductCategory, Category.id==ProductCategory.categoryID).outerjoin(ProductOrder, ProductCategory.productID==ProductOrder.productID).group_by(Category.id).with_entities(Category.name, func.coalesce(func.sum(ProductOrder.requested)-func.sum(ProductOrder.received),0)).all()

    for product in product_orders:
        statistics.append({
            "name": product[0],
            "waiting": int(product[1])
        })

    return Response(json.dumps({"statistics": statistics}), status=200)


if(__name__=="__main__"):
    db.init_app(app)
    app.run(debug=True, host="0.0.0.0", port=5005)
