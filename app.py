from flask import Flask, jsonify
from database.database import db

from utils import add_users, add_offer, add_orders, ProjectJSONEncoder
# from models import User, Order, Offer

from users.views import users_module
from orders.views import orders_module
from offers.views import offers_module

# initializing app and models
application = Flask(__name__)
application.config.from_pyfile("config.py")
# application.config.from_pyfile("models.py")

application.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{application.config.get("DATABASE_PATH")}'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
application.json_encoder = ProjectJSONEncoder

db.app = application
db.init_app(application)


# tables cleanup
with db.session() as session, session.begin():
    db.drop_all()
    session.execute("VACUUM")
    db.create_all()
    # db.session.commit()

# loading initial data set
add_users(application.config.get("USERS_INITIAL_DATA"))
add_offer(application.config.get("OFFERS_INITIAL_DATA"))
add_orders(application.config.get("ORDERS_INITIAL_DATA"))

# views
application.register_blueprint(users_module)
application.register_blueprint(orders_module)
application.register_blueprint(offers_module)


@application.route("/", methods=["GET"])
def index():
    User = application.config.get('USER_OBJ')
    data = session.query(User).all()
    print(data)
    return jsonify(data)
    return "INDEX PAGE JUST FOR FUN"


if __name__ == "__main__":
    application.run()
