# from flask import current_app
import datetime
import json
from datetime import date

from database.database import db
from models import User, Order, Offer


def instance_to_dict(instance) -> dict:
    """
    Serialize implementation
    """
    result = {keys: values for keys, values in vars(instance).items()}
    del result['_sa_instance_state']
    return result


def add_users(users_data_path: str):

    with open(users_data_path, 'r', encoding='UTF-8') as file:
        data = json.load(file)

    with db.session.begin():
        try:
            users_to_add = []
            for entry in data:
                user_to_add = User(
                    id=entry['id'],
                    first_name=entry['first_name'],
                    last_name=entry['last_name'],
                    age=entry['age'],
                    email=entry['email'],
                    role=entry['role'],
                    phone=entry['phone']
                )
                users_to_add.append(user_to_add)
            db.session.add_all(users_to_add)

        except Exception as err:

            print(f"Error: {err}")
            db.session.rollback()

        # session.commit()


def add_orders(orders_data_path: str):

    with open(orders_data_path, "r", encoding='UTF-8') as file:
        data = json.load(file)

        with db.session() as session, session.begin():
            orders_to_add = []
            for entry in data:
                order_to_add = Order(
                    id=entry['id'],
                    name=entry['name'],
                    description=entry['description'],
                    start_date=date_to_python_type(entry['start_date']), # datetime.strptime(entry['start_date'], '%m/%d/%Y')
                    end_date=date_to_python_type(entry['end_date']), # datetime.strptime(entry['end_date'], '%m/%d/%Y')
                    address=entry['address'],
                    price=entry['price'],
                    customer_id=entry['customer_id'],
                    executor_id=entry['executor_id']
                )
                orders_to_add.append(order_to_add)
            db.session().add_all(orders_to_add)
            # db.session.commit()


def add_offer(offers_data_path: str):

    with open(offers_data_path, "r", encoding='UTF-8') as file:
        data = json.load(file)

        with db.session() as session, session.begin():
            offers_to_add = []
            for entry in data:
                offer_to_add = Offer(
                    id=entry['id'],
                    order_id=entry['order_id'],
                    executor_id=entry['executor_id']
                )
                offers_to_add.append(offer_to_add)
            db.session().add_all(offers_to_add)
            # db.session.commit()


def date_to_python_type(date_input: str) -> date:

    date_entries_list = date_input.split("/")
    date_result = datetime.date(int(date_entries_list[2]), int(date_entries_list[0]), int(date_entries_list[1]))

    return date_result
