from flask.json import JSONEncoder
import datetime
import json
from datetime import date

from database.database import db
from models import User, Order, Offer


def instance_to_dict(instance) -> dict:
    """
    Serialize implementation. Because handwriting dicts is very annoying
    """
    result = {keys: values for keys, values in vars(instance).items()}
    del result['_sa_instance_state']
    return result


def add_users(users_data_path: str) -> None:
    """Populates Users table"""
    with open(users_data_path, 'r', encoding='UTF-8') as file:
        data = json.load(file)

    with db.session.begin():
        try:
            users_to_add = []
            for entry in data:
                user_to_add = User(**entry)
                users_to_add.append(user_to_add)
            db.session.add_all(users_to_add)
            # session.commit()
        except Exception as err:
            print(f"Error: {err}")
            db.session.rollback()


def add_orders(orders_data_path: str) -> None:
    """Populates Orders table"""
    with open(orders_data_path, "r", encoding='UTF-8') as file:
        data = json.load(file)

        with db.session() as session, session.begin():
            try:
                orders_to_add = []
                for entry in data:
                    # order_to_add = Order(
                    #     id=entry['id'],
                    #     name=entry['name'],
                    #     description=entry['description'],
                    #     start_date=date_to_python_type(entry['start_date']),  # datetime.strptime(entry['start_date'], '%m/%d/%Y')
                    #     end_date=date_to_python_type(entry['end_date']),  # datetime.strptime(entry['end_date'], '%m/%d/%Y')
                    #     address=entry['address'],
                    #     price=entry['price'],
                    #     customer_id=entry['customer_id'],
                    #     executor_id=entry['executor_id']
                    # ) # code archived for education purposes

                    # date conversion
                    for entry_key, entry_value in entry.items():
                        if 'date' in entry_key:
                            entry_value = date_to_python_type(entry_value)
                            entry[entry_key] = entry_value

                    order_to_add = Order(**entry)
                    orders_to_add.append(order_to_add)
                session.add_all(orders_to_add)
                # session.commit()
            except Exception as err:
                print(f"Error: {err}")
                session.rollback()


def add_offer(offers_data_path: str) -> None:
    """Populates Offers table"""
    with open(offers_data_path, "r", encoding='UTF-8') as file:
        data = json.load(file)

        with db.session() as session, session.begin():
            try:
                offers_to_add = []
                for entry in data:
                    offer_to_add = Offer(**entry)
                    offers_to_add.append(offer_to_add)
                session.add_all(offers_to_add)
                # session.commit()
            except Exception as err:
                print(f"Error: {err}")
                session.rollback()


def date_to_python_type(date_input: str) -> date:
    """Converts DB-specific date into python type date"""
    date_entries_list = date_input.split("/")
    date_result = datetime.date(int(date_entries_list[2]), int(date_entries_list[0]), int(date_entries_list[1]))
    return date_result


class ProjectJSONEncoder(JSONEncoder):
    """Custom JSONEncoder to ensure browser level response outputs date in ISO format"""

    def default(self, data_object):
        if isinstance(data_object, date):
            return data_object.isoformat()
        return JSONEncoder.default(self, data_object)
