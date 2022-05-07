from flask import Blueprint, jsonify, request
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
from database.session import Session

from models import User
from utils import instance_to_dict

users_module = Blueprint("users_module", __name__)


@users_module.route("/users", methods=["GET", "POST"])
def get_users():

    if request.method == 'POST':
        with Session.begin() as session:
            data = request.json
            result = User(**data)
            session.add(result)
            result_to_view = instance_to_dict(result)
            return jsonify(result_to_view)

    with Session.begin() as session:
        data = session.query(User).all()
        result = []
        for entry in data:
            result.append(instance_to_dict(entry))
        return jsonify(result)


@users_module.route("/users/<int:uid>", methods=["GET", "PUT", "DELETE"])
def users_handler(uid: int):

    if request.method == 'PUT':
        # update entry
        with Session.begin() as session:
            data = request.json
            data_to_correct = session.query(User).get(uid)
            for k, v in data.items():
                setattr(data_to_correct, k, v)
            session.add(data_to_correct)
            result_to_view = instance_to_dict(data_to_correct)
            return jsonify(result_to_view)

    elif request.method == 'DELETE':
        # delete entry
        with Session.begin() as session:
            data_to_delete = session.query(User).get(uid)
            session.delete(data_to_delete)
            return instance_to_dict(data_to_delete)

    else:
        # query entry
        with Session.begin() as session:
            data = session.query(User).get(uid)
            result = instance_to_dict(data)
            return jsonify(result)
