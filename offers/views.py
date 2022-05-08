from flask import Blueprint, jsonify, request

from database.session import Session
from models import Offer, Order, User
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
            try:
                result_to_write = Offer(**data)
                session.add(result_to_write)
            except Exception as err:
                print(f"Error: {err}")
                session.rollback()
                return f"Error: {err}", 500

            # query new entry from database
            result = session.query(Offer.id,
                                   Offer.order_id,
                                   Order.name,
                                   Order.description,
                                   Order.address,
                                   Order.start_date,
                                   Order.end_date,
                                   Order.price,
                                   Offer.executor_id,
                                   (User.first_name + ' ' + User.last_name).label('executor_name')) \
                .join(Order, Offer.order_id == Order.id) \
                .join(User, Offer.executor_id == User.id) \
                .filter(Offer.executor_id == data['executor_id'],
                        Offer.order_id == data['order_id'])
            result_to_view = []
            for entry in result:
                result_to_view.append(entry._asdict())
            return jsonify(result_to_view), 201

    # query entries (GET)
    with Session.begin() as session:

        data = session.query(Offer.id,
                             Offer.order_id,
                             Order.name,
                             Order.description,
                             Order.address,
                             Order.start_date,
                             Order.end_date,
                             Order.price,
                             Offer.executor_id,
                             (User.first_name + ' ' + User.last_name).label('executor_name')) \
            .join(Order, Offer.order_id == Order.id) \
            .join(User, Offer.executor_id == User.id).all()
        result = []
        for entry in data:
            result.append(entry._asdict())
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
            try:
                data_to_correct = session.query(Offer).get(off_id)
                for k, v in data.items():
                    setattr(data_to_correct, k, v)
                session.add(data_to_correct)
            except Exception as err:
                print(f"Error: {err}")
                session.rollback()
                return f"Data not found. Error: {err}", 404

            # query new data from database
            result_to_view = instance_to_dict(session.query(Offer).get(off_id))
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
                data = session.query(Offer.id,
                                     Offer.order_id,
                                     Order.name,
                                     Order.description,
                                     Order.address,
                                     Order.start_date,
                                     Order.end_date,
                                     Order.price,
                                     Offer.executor_id,
                                     (User.first_name + ' ' + User.last_name).label('executor_name')) \
                    .join(Order, Offer.order_id == Order.id) \
                    .join(User, Offer.executor_id == User.id) \
                    .filter(Offer.id == off_id).one()
                result = data._asdict()
                return jsonify(result)
            except Exception:
                return "Data not found", 404
