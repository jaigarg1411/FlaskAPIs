from flask import request
from db.itemDB import ItemDatabase
from exceptions import ObjectNotFound
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required

from schemas import (
    ItemPostSchema,
    ItemPutSchema,
    ItemGetSchema,
    SuccessMessageSchema,
    ItemQuerySchema,
)

blp = Blueprint("items", __name__, description="Operations on items")

operatorMap = {
    "lt": lambda a, b: a < b,
    "lte": lambda a, b: a <= b,
    "gt": lambda a, b: a > b,
    "gte": lambda a, b: a >= b,
    "eq": lambda a, b: a == b,
    "neq": lambda a, b: a != b,
}


@blp.route("/item")
class Item(MethodView):
    def __init__(self):
        self.db = ItemDatabase()

    @jwt_required()
    @blp.response(200, ItemGetSchema(many=True))
    def get(self):
        id = request.args.get("id")
        if id is not None:
            itemList = self.db.getItem(id)
            if len(itemList) == 0:
                abort(404, message="Item not found")
            return itemList
        try:
            items = self.db.getItems()
            filters = request.args.getlist("filter")
            if len(filters) > 0:
                filters = filters[0].split(",")
                filteredItems = []
                for filter in filters:
                    filter = filter.split(":")
                    filterOn = filter[0]
                    filterCond = filter[1]
                    filterVal = (
                        int(filter[2]) if type(items[0][filterOn]) == int else filter[2]
                    )
                    filteredItems.append(
                        [
                            item
                            for item in items
                            if operatorMap[filterCond](item[filterOn], filterVal)
                        ]
                    )
                filteredItems = [
                    [frozenset(item.items()) for item in filteredItemsEle]
                    for filteredItemsEle in filteredItems
                ]
                filteredItems = set(filteredItems[0]).intersection(*filteredItems[0:])
                return [dict(ele) for ele in filteredItems]
            else:
                return items
        except Exception as e:
            abort(500, message="Invalid request")

    @jwt_required()
    @blp.arguments(ItemPostSchema)
    @blp.response(201, SuccessMessageSchema)
    def post(self, req):
        try:
            self.db.addItem(req)
            return {"message": "Item added successfully"}, 201
        except Exception as e:
            abort(500, message="Error occured")

    @jwt_required()
    @blp.arguments(ItemPutSchema)
    @blp.arguments(ItemQuerySchema, location="query")
    def put(self, req, args):
        try:
            self.db.updateItem(args.get("id"), req)
            return {"message": "Item updated successfully"}, 200
        except ObjectNotFound as o:
            abort(404, message="Item not found")
        except Exception as e:
            abort(500, message="Invalid request")

    @jwt_required()
    @blp.arguments(ItemQuerySchema, location="query")
    def delete(self, args):
        try:
            self.db.deleteItem(args.get("id"))
            return {"message": "Item deleted successfully"}, 200
        except ObjectNotFound as o:
            abort(404, message="Item not found")
        except Exception as e:
            abort(500, message="Invalid request")
