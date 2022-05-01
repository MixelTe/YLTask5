from flask import jsonify
from flask_restful import abort, Resource
from flask_jwt_simple import jwt_required, get_jwt_identity
from data import db_session
from data.users import User
from api.parser import parser_user as parser, parser_user_noreq as parser_noreq


def get_user_or_abort(user_id):
    session = db_session.create_session()
    user: User = session.query(User).get(user_id)
    if not user:
        abort(404, message=f"User {user_id} not found")
    return user, session


class UsersResource(Resource):
    def get(self, user_id):
        user, _ = get_user_or_abort(user_id)
        fields = ("id", "surname", "name", "age", "position", "speciality", "address", "email")
        return jsonify(
            {
                'user': user.to_dict(only=fields)
            }
        )

    @jwt_required
    def delete(self, user_id):
        user, session = get_user_or_abort(user_id)
        userId = get_jwt_identity()
        if (user.id != userId and userId != 1):
            abort(403, message=f"Forbidden")
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})

    @jwt_required
    def put(self, user_id):
        args = parser_noreq.parse_args()
        user, session = get_user_or_abort(user_id)
        userId = get_jwt_identity()
        if (user.id != userId and userId != 1):
            abort(403, message=f"Forbidden")

        if (args["surname"] is not None):
            user.surname = str(args["surname"])
        if (args["name"] is not None):
            user.name = str(args["name"])
        if (args["age"] is not None):
            user.age = int(args["age"])
        if (args["position"] is not None):
            user.position = str(args["position"])
        if (args["speciality"] is not None):
            user.speciality = str(args["speciality"])
        if (args["address"] is not None):
            user.address = str(args["address"])
        if (args["email"] is not None):
            if (session.query(User).filter_by(email=str(args["email"]).first())):
                abort(400, message=f"Email address already taken")
            user.email = str(args["email"])
        if (args["password"] is not None):
            user.set_password(str(args["password"]))
        session.commit()
        return jsonify({'success': 'OK'})


class UsersListResource(Resource):
    def get(self):
        db_sess = db_session.create_session()
        users = db_sess.query(User).all()
        return jsonify(
            {
                'users': [item.to_dict(only=("id", "name", "surname", "position", "email")) for item in users]
            }
        )

    def post(self):
        args = parser.parse_args()
        db_sess = db_session.create_session()
        if (db_sess.query(User).filter_by(email=str(args["email"])).first()):
            abort(400, message=f"Email address already taken")
        user = User(
            surname=str(args["surname"]),
            name=str(args["name"]),
            age=int(args["age"]),
            position=str(args["position"]),
            speciality=str(args["speciality"]),
            address=str(args["address"]),
            email=str(args["email"])
        )
        user.set_password(str(args["password"]))
        db_sess.add(user)
        db_sess.commit()
        return jsonify({'success': 'OK', "user_id": user.id})
