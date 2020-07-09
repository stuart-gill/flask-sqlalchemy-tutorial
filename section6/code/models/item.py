from db import db


class ItemModel(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"))
    store = db.relationship("StoreModel")  # hooks items and stores tables together

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {"name": self.name, "price": self.price, "store_id": self.store_id}

    @classmethod
    def find_by_name(cls, name):
        # this line replaces everything below
        return cls.query.filter_by(
            name=name
        ).first()  # gets first row, converts row to ItemModel object and returns that. Query is part of sqlalchemy

        # connection = sqlite3.connect("data.db")
        # cursor = connection.cursor()

        # query = "SELECT * FROM items WHERE name = ?"
        # result = cursor.execute(query, (name,))
        # row = result.fetchone()
        # connection.close()

        # if row:
        #     return cls(name=row[1], price=row[2])

    def upsert(self):  # works for both insert and update functions
        db.session.add(self)
        db.session.commit()

        # connection = sqlite3.connect("data.db")
        # cursor = connection.cursor()

        # query = "INSERT INTO items (name, price) VALUES (?,?)"
        # cursor.execute(query, (self.name, self.price))
        # connection.commit()
        # connection.close()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

        # connection = sqlite3.connect("data.db")
        # cursor = connection.cursor()

        # query = "UPDATE items SET price = ? WHERE name = ?"
        # cursor.execute(query, (self.price, self.name))
        # connection.commit()
        # connection.close()
