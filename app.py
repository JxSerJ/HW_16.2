from flask import Flask

application = Flask(__name__)
application.config.from_pyfile("config.py")


@application.route("/users/<int:uid>", methods=["GET"])
def get_users(uid: int):
    pass


@application.route("/users", methods=["POST"])
def add_user():
    pass


@application.route("/users/<int:uid>", methods=["PUT"])
def add_user_uid(uid: int):
    pass


@application.route("/users/<int:uid>", methods=["DELETE"])
def delete_user_uid(uid: int):
    pass


@application.route("/orders/<int:oid>", methods=["GET"])
def get_orders(oid: int):
    pass


@application.route("/orders", methods=["POST"])
def add_order():
    pass


@application.route("/orders/<int:oid>", methods=["PUT"])
def add_order_oid(oid: int):
    pass


@application.route("/orders/<int:oid>", methods=["DELETE"])
def delete_order_oid(oid: int):
    pass


@application.route("/offers/<int:offid>", methods=["GET"])
def get_orders(offid: int):
    pass


@application.route("/offers/<int:offid>", methods=["POST"])
def add_offer():
    pass


@application.route("/offers/<int:offid>", methods=["PUT"])
def add_offer_offid(offid: int):
    pass


@application.route("/offers/<int:offid>", methods=["DELETE"])
def delete_offer_offid(offid: int):
    pass


if __name__ == "__main__":
    application.run()
