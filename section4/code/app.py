from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from security import authenticate, identity

app = Flask(__name__)
app.secret_key = "stuart"
api = Api(app)

jwt = JWT(
    app, authenticate, identity
)  # JWT will create /auth endpoint... that endpoint will return JWT token

items = []


class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument(
        "price", type=float, required=True, help="This field cannot be left blank!"
    )

    @jwt_required()
    def get(self, name):
        # for item in items:
        #     if item["name"] == name:
        #         return item
        # the "next" calls first item in this iterable. Notice that list comp is in parens not brackets... brackets would create a list
        item = next((item for item in items if item["name"] == name), None)
        return {"item": item}, 200 if item else 404

    def post(self, name):
        if next((item for item in items if item["name"] == name), None):
            return {"message": f"an item with name {name} already exists"}, 400

        data = Item.parser.parse_args()
        item = {"name": name, "price": data["price"]}
        items.append(item)
        return item, 201

    @jwt_required()
    def delete(self, name):
        global items
        items = [item for item in items if item["name"] != name]
        return {"message": "item deleted"}

    def put(self, name):

        data = Item.parser.parse_args()

        item = next((item for item in items if item["name"] == name), None)
        if item:
            item.update(data)
        else:
            item = {"name": name, "price": data["price"]}
            items.append(item)
        return item


class ItemList(Resource):
    def get(self):
        return {"items": items}


api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")

app.run(port=5000, debug=True)
