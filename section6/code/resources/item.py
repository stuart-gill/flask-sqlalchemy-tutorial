import sqlite3

from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


# resources used to map endpoints (like get, post) to /item/name or whatever
# anything not called by an API directly shouldn't be a resource but a model


class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument(
        "price", type=float, required=True, help="This field cannot be left blank!"
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {"message": "item not found"}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {"message": f"an item with name {name} already exists"}, 400

        data = Item.parser.parse_args()
        item = ItemModel(name, data["price"])

        try:
            item.upsert()
        except:
            return {"message": "an error occured while trying to post the item"}, 500

        # note: we always have to return json
        return item.json(), 201

    @jwt_required()
    def delete(self, name):
        # global items
        # items = [item for item in items if item["name"] != name]
        item = ItemModel.find_by_name(name)
        if item:
            item.delete()
            return {"message": "item deleted"}
        return {"message": "item not found"}, 404

    def put(self, name):

        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item:
            try:
                item.price = data["price"]
            except:
                return {"message": "an error occurred updating the item"}, 500
        else:
            try:
                item = ItemModel(name, data["price"])
                item.upsert()
            except:
                return {"message": "an error occured inserting the item"}, 500
        item.upsert()
        return item.json()


class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        result = cursor.execute(query)

        items = []

        for row in result:
            items.append({"name": row[1], "price": row[2]})
        connection.close()

        return {"items": items}
