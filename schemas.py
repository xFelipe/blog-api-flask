from marshmallow import Schema, fields, validate, EXCLUDE, ValidationError


class UserSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    id = fields.Integer(required=False)
    email = fields.Email(required=True)
    password = fields.String(
        required=True,
        validate=validate.Length(min=6, max=50)
    )


class PostSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    title = fields.String(required=True)
    body = fields.String(required=True)


class CommentSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    body = fields.String(required=True)
    post_id = fields.Integer(required=True)


class AlbumSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    name = fields.String(required=True)


class PhotoSchema(Schema):
    class Meta:
        unknown = EXCLUDE
    title = fields.String(required=True)
    album_id = fields.Integer(required=True)
