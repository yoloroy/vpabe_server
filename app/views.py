from flask import request, jsonify

from app import app
from app.models import *
from database.database import db_session

from time import sleep
from functools import reduce

from utils import sum_dicts

waiters = 0
actions = []

# region index
@app.route('/')
def none():
    return "He110!"

@app.route("/index")
def index():
    with open("app/index.html") as f:
        text = f.read()
    return text
# endregion

# region messages
@app.route("/putmessage")
def put_message():
    if "message" not in actions:
        actions.append("message")

    Message(
        text=request.args.get("text"),
        sender=int(request.args.get("sender")),
        chatid=int(request.args.get("chatid"))
    ).put()

    return "200"

@app.route("/getmessages")
def get_messages():
    def add_attachments(message: dict):
        message["attachments"] = [
            attachment.dict
            for attachment in Attachment.query
                .filter(Attachment.messageid == message["_rowid_"])
        ]
        return message

    chatid = int(request.args.get("chatid", default="0"))
    after = int(request.args.get("after", default="0"))

    temp = Message.query \
        .filter(Message.chatid == chatid) \
        .filter(Message._rowid_ > after)

    while temp.count() == 0:
        sleep(0.1)
        temp = Message.query \
            .filter(Message.chatid == chatid) \
            .filter(Message._rowid_ > after)

    return jsonify(
        [
            add_attachments(message.dict)
            for message in temp
        ]
    )
# endregion

# region chats
@app.route("/getchats")
def get_chats_by_user():
    def last_message(chatid: int):
        return Message.query.filter(Message.chatid == chatid)[-1].dict

    userid = int(request.args.get("userid"))

    return jsonify([
        chat_view
        for chat_view in map(
            lambda chat: sum_dicts(
                chat.dict,
                {"lastMessage": last_message(chat.chatid)}
            ),
            Chat.query.filter(Chat.userid == userid)
        )
    ])

def add_chat():
    pass

def delete_chat():
    pass
# endregion

# region action
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

@app.route("/addaction")
def add_action():
    actions.append(request.args.get("action"))
    return "200"
# endregion

# region user
@app.route("/getuser")
def get_user():
    userid = int(request.args.get("userid", default=0))
    telephone = request.args.get("telephone", default="")

    if userid != 0:
        return get_user_by_id(userid)
    if telephone != "":
        return get_user_by_number(telephone)
    return "400"

def get_user_by_id(userid):
    return jsonify(
        User.query
            .filter(User.userid == userid)
            .first()
            .dict
    )

def get_user_by_number(telephone):
    return jsonify(
        User.query
            .filter(User.telephone == telephone)
            .first()
            .dict
    )

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
# endregion

# region event
def put_event():
    pass

@app.route("/getevents")
def get_events():  # TODO: add filtering
    userid = int(request.args.get("userid", default="0"))

    if userid:
        return get_events_for_user(userid)

    return jsonify(
        [
            event.dict
            for event in Event.query.all()
        ]
    )

def get_events_for_user(userid):
    subscribes = [
        subItem.eventid
        for subItem in SubscribeItem.query
            .filter(SubscribeItem.userid == userid)
    ]

    return jsonify([
        event.dict
        for event in reduce(
            lambda a, b: a + b,
            [
                Event.query.filter(Event.eventid == eventid)
                for eventid in subscribes
            ])
    ])
# endregion

# region db
# noinspection PyUnusedLocal
# because from tutorial
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
 #endregion
