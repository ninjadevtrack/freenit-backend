import os
import re
from flask import current_app
from flask_restplus import abort
from .resources import ProtectedResource
from .namespaces import ns_user
from ..models.auth import User
from ..schemas import UserSchema


@ns_user.route('', endpoint='users')
class UserListAPI(ProtectedResource):
    def get(self):
        """List users"""
        response, errors = UserSchema(many=True).dump(User.select())
        if errors:
            abort(409, errors)
        return response

    @ns_user.expect(UserSchema.fields())
    def post(self):
        user, errors = UserSchema().load(current_app.api.payload)
        if errors:
            abort(409, errors)
        user.save()
        return UserSchema().dump(user)


@ns_user.route('/<id>', endpoint='user')
@ns_user.response(404, 'User not found')
class UserAPI(ProtectedResource):
    def get(self, id):
        """Get user details"""
        try:
            user = User.get(id=id)
        except User.DoesNotExist:
            abort(404, 'User not found')
        response, errors = UserSchema().dump(user)
        if errors:
            abort(409, errors)
        return response
