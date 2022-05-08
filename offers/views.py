from flask import Blueprint, jsonify, request

from database.session import Session
from models import Offer
from utils import instance_to_dict

offers_module = Blueprint("offers", __name__)


@offers_module.route("/offers", methods=["GET", "POST"])
def get_offers():

    if request.method == 'POST':
        with Session.begin() as session:
            data = request.json
            # validating input data structure now
            if not set(data).issubset(set(vars(Offer).keys())):
                return "Not valid data structure. Provided keys are not allowed.", 400
            elif 'id' in set(data):
                return "Not valid data structure. ID key found. ID is forbidden to declare in data-set for " \
                       "POST method.", 400
            # writing data
            result = Offer(**data)
            session.add(result)
            result_to_view = instance_to_dict(result)
            return jsonify(result_to_view)
    # query entries (GET)
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
            # validating input data structure now
            if not set(data).issubset(set(vars(Offer).keys())):
                return "Not valid data structure. Provided keys are not allowed.", 400
            elif 'id' in set(data):
                return "Not valid data structure. ID key found. ID is forbidden to declare in data-set for " \
                       "PUT method. Use endpoint route for ID designation", 400
            # writing data
            data_to_correct = session.query(Offer).get(off_id)
            for k, v in data.items():
                setattr(data_to_correct, k, v)
            session.add(data_to_correct)
            result_to_view = instance_to_dict(data_to_correct)
            return jsonify(result_to_view)

    elif request.method == 'DELETE':
        # delete entry
        with Session.begin() as session:
            try:
                data_to_delete = session.query(Offer).get(off_id)
                session.delete(data_to_delete)
                return instance_to_dict(data_to_delete)
            except Exception:
                return "Data not found", 404

    else:
        # query entry (GET)
        with Session.begin() as session:
            try:
                data = session.query(Offer).get(off_id)
                result = instance_to_dict(data)
                return jsonify(result)
            except TypeError:
                return "Data not found", 404
