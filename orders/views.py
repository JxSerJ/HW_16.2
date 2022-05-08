from flask import Blueprint, jsonify, request

from database.session import Session
from database.database import db
from models import Order, User
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
            try:
                result_to_write = Order(**data)
                session.add(result_to_write)
            except Exception as err:
                print(f"Error: {err}")
                session.rollback()
                return f"Error: {err}", 500

            # query new entry from database
            Customer_ali = db.aliased(User)
            Executor_ali = db.aliased(User)
            result = session.query(Order.id,
                                   Order.name,
                                   Order.description,
                                   Order.start_date,
                                   Order.end_date,
                                   Order.address,
                                   Order.price,
                                   Order.customer_id,
                                   (Customer_ali.first_name + ' ' + Customer_ali.last_name).label('customer_name'),
                                   Order.executor_id,
                                   (Executor_ali.first_name + ' ' + Executor_ali.last_name).label('executor_name'))\
                .join(Customer_ali, Order.customer_id == Customer_ali.id)\
                .join(Executor_ali, Order.executor_id == Executor_ali.id)\
                .filter(Order.name == data['name'],
                        Order.executor_id == data['executor_id'],
                        Order.customer_id == data['customer_id'])
            result_to_view = []
            for entry in result:
                result_to_view.append(entry._asdict())
            return jsonify(result_to_view), 201

    # query entries (GET)
    with Session.begin() as session:
        Customer_ali = db.aliased(User)
        Executor_ali = db.aliased(User)
        data = session.query(Order.id,
                             Order.name,
                             Order.description,
                             Order.start_date,
                             Order.end_date,
                             Order.address,
                             Order.price,
                             Order.customer_id,
                             (Customer_ali.first_name + ' ' + Customer_ali.last_name).label('customer_name'),
                             Order.executor_id,
                             (Executor_ali.first_name + ' ' + Executor_ali.last_name).label('executor_name'))\
            .join(Customer_ali, Order.customer_id == Customer_ali.id)\
            .join(Executor_ali, Order.executor_id == Executor_ali.id).all()
        result = []
        for entry in data:
            result.append(entry._asdict())
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
            try:
                data_to_correct = session.query(Order).get(oid)
                for k, v in data.items():
                    setattr(data_to_correct, k, v)
                session.add(data_to_correct)
            except Exception as err:
                print(f"Error: {err}")
                session.rollback()
                return f"Data not found. Error: {err}", 404

            # query new data from database
            result_to_view = instance_to_dict(session.query(Order).get(oid))
            return jsonify(result_to_view)

    elif request.method == 'DELETE':
        # delete entry
        with Session.begin() as session:
            try:
                data_to_delete = session.query(Order).get(oid)
                session.delete(data_to_delete)
                return instance_to_dict(data_to_delete)
            except Exception:
                return "Data not found", 404

    else:
        # query entry (GET)
        with Session.begin() as session:
            try:
                Customer_ali = db.aliased(User)
                Executor_ali = db.aliased(User)
                data = session.query(Order.id,
                                     Order.name,
                                     Order.description,
                                     Order.start_date,
                                     Order.end_date,
                                     Order.address,
                                     Order.price,
                                     Order.customer_id,
                                     (Customer_ali.first_name + ' ' + Customer_ali.last_name).label('customer_name'),
                                     Order.executor_id,
                                     (Executor_ali.first_name + ' ' + Executor_ali.last_name).label('executor_name')) \
                    .join(Customer_ali, Order.customer_id == Customer_ali.id) \
                    .join(Executor_ali, Order.executor_id == Executor_ali.id) \
                    .filter(Order.id == oid).one()
                result = data._asdict()
                return jsonify(result)
            except Exception:
                return "Data not found", 404
