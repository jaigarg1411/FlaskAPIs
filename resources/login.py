from db.usersDB import UsersDatabase
from flask_smorest import Blueprint, abort
from exceptions import ObjectNotFound
from schemas import UserPostSchema
from flask_jwt_extended import get_jwt, jwt_required

blp = Blueprint("login", __name__, description="Login operation")

dbObj = UsersDatabase()


@blp.route("/login", methods=["POST"])
@blp.arguments(UserPostSchema)
def loginUser(req):
    try:
        token = dbObj.loginUser(req)
        return {"token": token}, 200
    except ObjectNotFound as o:
        abort(401, message="Invalid credentials")
    except Exception as e:
        abort(500, message="Error occured")


@blp.route("/logout", methods=["POST"])
@jwt_required()
def loginUser():
    try:
        dbObj.invalidateToken(get_jwt()["jti"])
        return {"message": "Logged out sucessfully"}, 200
    except Exception as e:
        abort(500, message=f"Error occured: {e}")
