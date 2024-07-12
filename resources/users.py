from flask import request
from db.usersDB import UsersDatabase
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint, abort
from exceptions import ObjectAlreadyExist, ObjectNotFound
from schemas import SuccessMessageSchema, UserGetSchema, UserPostSchema, UserPutSchema, UserQuerySchema
from flask.views import MethodView

blp = Blueprint("users", __name__, description="Operations on users")

dbObj = UsersDatabase()

blp = Blueprint("users", __name__, description="Operations on users")

@blp.route("/user")
class User(MethodView):
    def __init__(self):
        self.db = UsersDatabase()

    @jwt_required()
    @blp.response(200, UserGetSchema(many=True))
    def get(self):
        try:
            id = request.args.get("id")
            if id is not None:
                user = self.db.getUser(id)
                if not user:
                    abort(404, message="User not found")
                return user
            else:
                return self.db.getUsers()
        except Exception as e:
            abort(500, message="Invalid request")

    @jwt_required()
    @blp.arguments(UserPostSchema)
    @blp.response(201, SuccessMessageSchema)
    def post(self, req):
        try:
            self.db.addUser(req)
            return {"message": "User added successfully"}, 201
        except ObjectAlreadyExist as e:
            abort(409, message="User already exists")
        except Exception as e:
            abort(500, message="An error occurred")

    @jwt_required()
    @blp.arguments(UserPutSchema)
    @blp.arguments(UserQuerySchema, location="query")
    @blp.response(200, SuccessMessageSchema)
    def put(self, req, args):
        try:
            self.db.updateUser(args.get("id"), req)
            return {"message": "User updated successfully"}, 200
        except ObjectNotFound as e:
            abort(404, message="User not found")
        except Exception as e:
            abort(500, message="An error occurred")

    @jwt_required()
    @blp.arguments(UserQuerySchema, location="query")
    @blp.response(200, SuccessMessageSchema)
    def delete(self, args):
        try:
            self.db.deleteUser(args.get("id"))
            return {"message": "User deleted successfully"}, 200
        except ObjectNotFound as e:
            abort(404, message="User not found")
        except Exception as e:
            abort(500, message="An error occurred")

