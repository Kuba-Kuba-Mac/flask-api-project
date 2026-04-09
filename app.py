from flask import Flask, jsonify,request

app = Flask(__name__)

products = [
    {"id":1, "name":"Keyboard","price":49.60},
    {"id":2, "name":"Pillow","price":20.40},
    {"id":3, "name":"book","price":5.33}
]

@app.route("/")
def home():
    return jsonify({
        "message": "Hello from our first Flask server!"
    })



@app.route("/products", methods = ["GET"])
def get_products():
    return jsonify(products)
    

@app.route("/products", methods=["POST"])
def add_product():
    data = request.get_json()
    new_product = {
        "id" : len(products)+1,
        "name" :data.get("name"),
        "price": data.get("price")
    }
    products.append(new_product)
    return jsonify({"message":"Product added", "product": new_product}), 201


if __name__ == "__main__":
    app.run(debug=True)
            


