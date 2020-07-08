from flask import request, jsonify

from app import app
from app.models import Message, User
from database.database import db_session

from time import sleep

waiters = 0
actions = []

@app.route('/')
def none():
    return "He110!"

@app.route("/index")
def index():
    with open("app/index.html") as f:
        text = f.read()
    return text

@app.route("/putmessage")
def put_message():
    if "message" not in actions:
        actions.append("message")

    Message(
        text=request.args.get("text")
    ).put()

    return "200"

@app.route("/getmessages")
def get_messages():
    return jsonify([message.dict for message in Message.query.all()])

@app.route("/getaction")
def get_action():
    global waiters
    waiters += 1

    while True:
        if len(actions) != 0:
            waiters -= 1
            break
        sleep(0.1)

    action = actions[0]
    if waiters == 0:
        actions.pop(0)

    return action

@app.route("/clearallmessages")
def clear_all_messages():
    actions.append("message")
    return str(Message.clear_all())

@app.route("/addaction")
def add_action():
    actions.append(request.args.get("action"))
    return "200"

@app.route("/getusers")
def get_users():
    return jsonify([user.dict for user in User.query.all()])

@app.route("/putuser")
def put_user():
    if "message" not in actions:
        actions.append("message")

    User(
        username=request.args.get("username"),
        telephone=request.args.get("telephone"),
        status=request.args.get("status", default=""),
        avatar=request.args.get("avatar", default="")
    ).put()
    return "200"

# noinspection PyUnusedLocal
# because from tutorial
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
