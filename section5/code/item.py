import sqlite3

from flask_restful import Resource, reqparse
from flask_jwt import jwt_required


class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument(
        "price", type=float, required=True, help="This field cannot be left blank!"
    )

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name = ?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {"item": {"name": row[1], "price": row[2]}}

    @jwt_required()
    def get(self, name):
        item = self.find_by_name(name)
        if item:
            return item
        return {"message": "item not found"}, 404

    def post(self, name):
        if self.find_by_name(name):
            return {"message": f"an item with name {name} already exists"}, 400

        data = Item.parser.parse_args()
        item = {"name": name, "price": data["price"]}

        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "INSERT INTO items (name, price) VALUES (?,?)"
        cursor.execute(query, (item["name"], item["price"]))
        connection.commit()
        connection.close()

        # note: we always have to return json
        return item, 201

    @jwt_required()
    def delete(self, name):
        # global items
        # items = [item for item in items if item["name"] != name]
        item = self.find_by_name(name)
        if item:
            connection = sqlite3.connect("data.db")
            cursor = connection.cursor()
            query = "DELETE FROM items WHERE name = ?"
            cursor.execute(query, (name,))
            connection.commit()
            connection.close()
            return {"message": "item deleted"}
        return {"message": "item not found"}, 404

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
