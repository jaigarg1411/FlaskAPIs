from flask import Flask
from resources.item import blp as ItemBluePrint
from resources.users import blp as UsersBluePrint
from resources.login import blp as LoginBluePrint, dbObj
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from db.usersDB import UsersDatabase

app = Flask(__name__)

app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["API_TITLE"] = "My REST API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

app.config[
    "JWT_SECRET_KEY"
] = "1241691190210501596851087062392788145360316770048204292537070907917922206281"

api = Api(app)
jwt = JWTManager(app)


@jwt.token_in_blocklist_loader
def checkIfTokenBlocked(jwt_headers, jwt_payload):
    return jwt_payload["jti"] in UsersDatabase().getBlockedTokenList()


@jwt.revoked_token_loader
def revokedTokenCallback(jwt_headers, jwt_payload):
    return ({"description": "User is logged out", "error": "Token revoked"}, 401)


api.register_blueprint(ItemBluePrint)
api.register_blueprint(UsersBluePrint)
api.register_blueprint(LoginBluePrint)
