from flask import Flask, request, Response
#from shop.configuration import Configuration
#from shop.models import db, Product, Category, ProductCategory
from configuration import Configuration
from models import db, Product, Category, ProductCategory
from redis import Redis
from supplierDecorator import roleCheck
from flask_jwt_extended import JWTManager, jwt_required
import io, csv, json

app = Flask ( __name__ )
app.config.from_object ( Configuration )
jwt = JWTManager ( app )


@app.route("/update", methods=["POST"])
@roleCheck ( role = "magacioner" )
def update():
    if not request.files.get("file", None):
        return Response(json.dumps({"message": "Field file is missing."}), status=400)
    content = request.files["file"].stream.read().decode("utf-8")
    stream = io.StringIO(content)
    reader = csv.reader(stream)

    products = []
    cnt = 0
    for row in reader:
        if (len(row)!=4):
            return Response(json.dumps({"message":f"Incorrect number of values on line {cnt}."}), status=400)
        try:
            quantity = int(row[2])
        except ValueError:
            return Response(json.dumps({"message": f"Incorrect quantity on line {cnt}."}), status=400)
        if (int(row[2]) < 1):
            return Response(json.dumps({"message": f"Incorrect quantity on line {cnt}."}), status=400)
        try:
            price = float(row[3])
        except ValueError:
            return Response(json.dumps({"message": f"Incorrect price on line {cnt}."}), status=400)
        if (float(row[3]) < 1):
            return Response(json.dumps({"message": f"Incorrect price on line {cnt}."}), status=400)

        product = "{},{},{},{}".format(row[0], row[1], row[2], row[3])
        products.append(product)
        cnt+=1

    for product in products:
        with Redis(host=Configuration.REDIS_HOST) as redis:
            redis.rpush(Configuration.REDIS_PRODUCT_LIST, product);

    return Response(status=200)

if(__name__=="__main__"):
    db.init_app(app)
    app.run(debug=True, host="0.0.0.0", port=5001)