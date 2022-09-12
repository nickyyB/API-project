from flask import Flask, request, Response, jsonify
#from shop.configuration import Configuration
#from shop.models import db, Product, Category, ProductCategory, Order, OrderStatus, Status, ProductOrder
from configuration import Configuration
from models import db, Product, Category, ProductCategory, Order, OrderStatus, Status, ProductOrder
from redis import Redis
from buyerDecorator import roleCheck
from flask_jwt_extended import JWTManager, get_jwt_identity, get_jwt, verify_jwt_in_request
from sqlalchemy import and_
import json, datetime
#from pprint import pprint

app = Flask ( __name__ )
app.config.from_object ( Configuration )
jwt = JWTManager ( app )


@app.route("/search", methods=["GET"])
@roleCheck ( role = "kupac" )
def search():
    name = request.args.get("name")
    category = request.args.get("category")

    products=[]
    categories = []
    if (name and category):
        products = Product.query.join(ProductCategory).join(Category).filter(and_(Category.name.like(f"%{category}%"), Product.name.like(f"%{name}%")))
    elif (name and category == None):
        products = Product.query.filter(Product.name.like(f"%{name}%"))
    elif (name==None and category):
        products = Product.query.join(ProductCategory).join(Category).filter(Category.name.like(f"%{category}%"))
    else:
        products = Product.query.all()

    search_products = []
    for product in products:
        product_categories = []
        for product_cat in product.categories:
            product_categories.append(product_cat.name)
            if product_cat.name not in categories:
                categories.append(product_cat.name)
        search_products.append({
            "categories": product_categories,
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "quantity": product.number
        })
    return Response(json.dumps({"categories": categories,"products": search_products}), status=200)

@app.route("/order", methods=["POST"])
@roleCheck ( role = "kupac" )
def order():
    requests = request.json.get("requests", "")

    if len(requests)==0:
        return Response(json.dumps({"message": "Field requests is missing."}), status=400)

    cnt = 0
    for r in requests:
        id = r.get("id", "")
        if id=="":
            return Response(json.dumps({"message": f"Product id is missing for request number {cnt}."}), status=400)
        number = r.get("quantity", "")
        if number=="":
            return Response(json.dumps({"message": f"Product quantity is missing for request number {cnt}."}), status=400)
        try:
            id = int(id)
        except ValueError:
            return Response(json.dumps({"message": f"Invalid product id for request number {cnt}."}), status=400)
        if( int(id)<0 ):
            return Response(json.dumps({"message": f"Invalid product id for request number {cnt}."}), status=400)
        try:
            number = int(number)
        except ValueError:
            return Response(json.dumps({"message": f"Invalid product quantity for request number {cnt}."}), status=400)
        if(int(number)<=0):
            return Response(json.dumps({"message": f"Invalid product quantity for request number {cnt}."}), status=400)

        product = Product.query.filter(Product.id == id).first()
        if product is None:
            return Response(json.dumps({"message": f"Invalid product for request number {cnt}."}), status=400)
        cnt += 1

    order = Order(priceTOTAL=0, time=datetime.datetime.now().isoformat(), email=get_jwt_identity())
    db.session.add(order)
    db.session.commit()
    status = OrderStatus(orderID=order.id, statusID=2)
    db.session.add(status)
    db.session.commit()

    completed = True
    #pprint(locals())
    for r in requests:
        product = Product.query.filter(Product.id == r['id']).first()
        order.priceTOTAL += float(product.price) * float(r['quantity'])
        product_order = ProductOrder(productID=r["id"], orderID=order.id, priceATM=product.price, received=0, requested=r["quantity"])

        if product.number >= r['quantity']:
            product.number = product.number - r["quantity"]
            product_order.received = r["quantity"]
        else:
            product_order.received = product.number
            product.number = 0
            completed = False

        db.session.add(product_order)
        db.session.commit()

    if completed:
        status.statusID=1

    db.session.commit()

    return Response(json.dumps({"id": order.id}), status=200)

@app.route("/status", methods=["GET"])
@roleCheck ( role = "kupac" )
def status():
    user = get_jwt_identity()
    orders = Order.query.filter(Order.email == user).all()

    orders_result = []
    for order in orders:
        products_result = []
        for product in order.products:
            categories_result = []
            for category in product.categories:
                categories_result.append(category.name)
            product_order = ProductOrder.query.join(Order).filter(and_(Order.id == order.id,ProductOrder.productID == product.id)).first()
            products_result.append({
                "categories":categories_result,
                "name":product.name,
                "price":product_order.priceATM,
                "received" : product_order.received,
                "requested" : product_order.requested
            })
        o = OrderStatus.query.filter(OrderStatus.orderID==order.id).first()
        status = "PENDING"
        if(o.statusID==1):
            status = "COMPLETE"
        orders_result.append({
            "products": products_result,
            "price": order.priceTOTAL,
            "status": status,
            "timestamp": str(order.time)
        })
    return jsonify(orders=orders_result)

if (__name__ == "__main__"):
    db.init_app(app)
    app.run(debug=True, host="0.0.0.0", port=5004)