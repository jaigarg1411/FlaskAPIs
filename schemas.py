from marshmallow import Schema, fields, validates_schema, ValidationError


class ItemPostSchema(Schema):
    name = fields.Str(required=True)
    price = fields.Int(required=True)


class ItemPutSchema(Schema):
    name = fields.Str()
    price = fields.Int()

    @validates_schema
    def validate_name_or_price(self, data, **kwargs):
        if not (data.get("name") or data.get("price")):
            raise ValidationError("At least one of 'name' or 'price' is required.")


class ItemGetSchema(Schema):
    name = fields.Str()
    price = fields.Int()
    id = fields.Int()


class SuccessMessageSchema(Schema):
    message = fields.Str(dump_only=True)


class ItemQuerySchema(Schema):
    id = fields.Str(required=True)


class UserPostSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)


class UserPutSchema(Schema):
    username = fields.Str()
    password = fields.Str()

    @validates_schema
    def validate_username_or_password(self, data, **kwargs):
        if not (data.get("username") or data.get("passsword")):
            raise ValidationError(
                "At least one of 'username' or 'password' is required."
            )


class UserGetSchema(Schema):
    username = fields.Str()
    password = fields.Str()
    id = fields.Int()
    
class UserQuerySchema(Schema):
    id = fields.Str(required=True)
