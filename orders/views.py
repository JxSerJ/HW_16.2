from flask import Blueprint, jsonify, request

from database.session import Session
from models import Order
from utils import instance_to_dict, date_to_python_type

orders_module = Blueprint("orders", __name__)


@orders_module.route("/orders", methods=["GET", "POST"])
def get_orders():

    if request.method == 'POST':
        with Session.begin() as session:
            data = request.json
            # validating input data structure now
            if not set(data).issubset(set(vars(Order).keys())):
                return "Not valid data structure. Provided keys are not allowed.", 400
            elif 'id' in set(data):
                return "Not valid data structure. ID key found. ID is forbidden to declare in data-set for " \
                       "POST method.", 400
            # date conversion
            for entry_key, entry_value in data.items():
                if 'date' in entry_key:
                    entry_value = date_to_python_type(entry_value)
                    data[entry_key] = entry_value
            # writing data
            result = Order(**data)
            session.add(result)
            result_to_view = instance_to_dict(result)
            return jsonify(result_to_view), 201
    # query entries (GET)
    with Session.begin() as session:
        data = session.query(Order).all()
        result = []
        for entry in data:
            result.append(instance_to_dict(entry))
        return jsonify(result)


@orders_module.route("/orders/<int:oid>", methods=["GET", "PUT", "DELETE"])
def add_order_oid(oid: int):

    if request.method == 'PUT':
        # update entry
        with Session.begin() as session:
            data = request.json
            # validating input data structure now
            if not set(data).issubset(set(vars(Order).keys())):
                return "Not valid data structure. Provided keys are not allowed.", 400
            elif 'id' in set(data):
                return "Not valid data structure. ID key found. ID is forbidden to declare in data-set for " \
                       "PUT method. Use endpoint route for ID designation", 400
            # date conversion
            for entry_key, entry_value in data.items():
                if 'date' in entry_key:
                    entry_value = date_to_python_type(entry_value)
                    data[entry_key] = entry_value
            # writing data
            data_to_correct = session.query(Order).get(oid)
            for k, v in data.items():
                setattr(data_to_correct, k, v)
            session.add(data_to_correct)
            result_to_view = instance_to_dict(data_to_correct)
            return jsonify(result_to_view)

    elif request.method == 'DELETE':
        # delete entry
        with Session.begin() as session:
            data_to_delete = session.query(Order).get(oid)
            session.delete(data_to_delete)
            return instance_to_dict(data_to_delete)

    else:
        # query entry (GET)
        with Session.begin() as session:
            data = session.query(Order).get(oid)
            result = instance_to_dict(data)
            return jsonify(result)
