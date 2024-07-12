from exceptions import ObjectNotFound
from db.dbConn import Database


class ItemDatabase(Database):
    def __init__(self):
        super().__init__()

    def getItems(self):
        query = "SELECT * FROM item"
        self.cursor.execute(query)
        item_list = []
        for row in self.cursor.fetchall():
            item_dict = {}
            item_dict["id"], item_dict["name"], item_dict["price"] = row
            item_list.append(item_dict)
        return item_list

    def getItem(self, id):
        query = "SELECT * FROM item WHERE id = ?"
        self.cursor.execute(query, id)
        row = self.cursor.fetchone()
        if row is None:
            return []
        return [{"id": row[0], "name": row[1], "price": row[2]}]

    def addItem(self, bodyObj):
        query = "INSERT INTO item (name, price) values (?, ?)"
        try:
            self.cursor.execute(query, (bodyObj["name"], bodyObj["price"]))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise Exception(e)

    def updateItem(self, id, bodyObj):
        updatedName = bodyObj.get("name", None)
        updatedPrice = bodyObj.get("price", None)
        query = "UPDATE item SET name = ? and price = ? where id = ?"
        if updatedName is None:
            query = "UPDATE item SET price = ? where id = ?"
            self.cursor.execute(query, updatedPrice, id)
        elif updatedPrice is None:
            query = "UPDATE item SET name = ? where id = ?"
            self.cursor.execute(query, updatedName, id)
        else:
            self.cursor.execute(query, updatedName, updatedPrice, id)
        self.conn.commit()
        rowCount = self.cursor.rowcount
        if rowCount == 0:
            raise ObjectNotFound("Item not found")

    def deleteItem(self, id):
        query = "DELETE FROM item where id = ?"
        self.cursor.execute(query, id)
        self.conn.commit()
        rowCount = self.cursor.rowcount
        if rowCount == 0:
            raise ObjectNotFound("Item not found")
