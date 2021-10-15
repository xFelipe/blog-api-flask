from marshmallow import Schema, fields, validate, INCLUDE

class UserSchema(Schema):
    class Meta:
        unknowl = INCLUDE

    username = fields.String(
        required=True, validate=validate.Length(min=6, max=50)
    )
    password = fields.String(
        required=True,
        validate=validate.Length(min=6, max=50)
    )
