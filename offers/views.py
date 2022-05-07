from flask import Blueprint, jsonify, request
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
from database.session import Session

from models import Offer
from utils import instance_to_dict

offers_module = Blueprint("offers", __name__)


@offers_module.route("/offers", methods=["GET", "POST"])
def get_offers():

    if request.method == 'POST':
        with Session.begin() as session:
            data = request.json
            result = Offer(**data)
            session.add(result)
            result_to_view = instance_to_dict(result)
            return jsonify(result_to_view)

    with Session.begin() as session:
        data = session.query(Offer).all()
        result = []
        for entry in data:
            result.append(instance_to_dict(entry))
        return jsonify(result)


@offers_module.route("/offers/<int:off_id>", methods=["GET", "PUT", "DELETE"])
def add_offer_off_id(off_id: int):

    if request.method == 'PUT':
        # update entry
        with Session.begin() as session:
            data = request.json
            data_to_correct = session.query(Offer).get(off_id)
            for k, v in data.items():
                setattr(data_to_correct, k, v)
            session.add(data_to_correct)
            result_to_view = instance_to_dict(data_to_correct)
            return jsonify(result_to_view)

    elif request.method == 'DELETE':
        # delete entry
        with Session.begin() as session:
            data_to_delete = session.query(Offer).get(off_id)
            session.delete(data_to_delete)
            return instance_to_dict(data_to_delete)

    else:
        # query entry
        with Session.begin() as session:
            data = session.query(Offer).get(off_id)
            result = instance_to_dict(data)
            return jsonify(result)
