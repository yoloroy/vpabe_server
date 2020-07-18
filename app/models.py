from abc import ABCMeta, abstractmethod

from sqlalchemy import Column, String, Integer
from database.database import Base, db_session


class Model:
    __metaclass__ = ABCMeta

    def put(self):
        """Put object to db"""
        db_session.add(self)
        db_session.commit()

        # noinspection PyUnresolvedReferences
        return self.query.count()

    @abstractmethod
    def dict(self):
        """Return data by dict"""


class Message(Base, Model):
    __tablename__ = "messages"
    _rowid_ = Column(Integer, primary_key=True)
    text = Column(String())
    sender = Column(Integer, nullable=False)
    chatid = Column(Integer, nullable=False)

    def __init__(self, text, sender, chatid):
        self.text = text
        self.sender = sender
        self.chatid = chatid

    def __repr__(self):
        return str(self.dict)

    @property
    def dict(self):
        sender: User = User.query.filter(User.userid==self.sender).first()

        return {
            "_rowid_": self._rowid_,
            "text": self.text,
            "chatid": self.chatid,
            "sender": sender.username,
            "avatar": sender.avatar
        }


class User(Base, Model):
    __tablename__ = "users"
    userid = Column(Integer, primary_key=True, nullable=False, autoincrement=True, unique=True)
    username = Column(String(), nullable=False)
    telephone = Column(String(), nullable=False)
    status = Column(String())
    avatar = Column(String())

    def __init__(self, username, telephone, status="", avatar=""):
        self.username = username
        self.telephone = telephone
        self.status = status
        self.avatar = avatar

    def __repr__(self):
        return str(self.dict)

    @property
    def dict(self):
        return {
            "userid":    self.userid,
            "username":  self.username,
            "status":    self.status,
            "avatar":    self.avatar,
            "telephone": self.telephone
        }


class Event(Base, Model):
    __tablename__ = "events"
    eventid = Column(Integer, primary_key=True, nullable=False, autoincrement=True, unique=True)
    name = Column(String(), nullable=False)
    description = Column(String(), nullable=False)
    avatar = Column(String())
    dateid = Column(Integer, nullable=False)
    likeid = Column(Integer, nullable=False)
    authorid = Column(Integer, nullable=False)

    def __init__(
            self,
            name: str,
            authorid: int,
            description: str,
            avatar: str,
            dateid: int,
            likeid: int
    ):
        self.name = name
        self.authorid = authorid
        self.description = description
        self.avatar = avatar
        self.dateid = dateid
        self.likeid = likeid

    def __repr__(self):
        return str(self.dict)

    @property
    def dict(self):
        return {
            "eventid":       self.eventid,
            "name":          self.name,
            "authorid":      self.authorid,
            "description":   self.description,
            "avatar":        self.avatar,
            "date":
                Date.query
                    .filter(Date.dateid == self.dateid)
                    .first().dict,
            "like":
                Like.query
                    .filter(Like.likeid == self.likeid)
                    .first().dict
        }


class Date(Base, Model):
    __tablename__ = "dates"
    dateid = Column(Integer, primary_key=True, nullable=False, autoincrement=True, unique=True)
    month = Column(Integer, nullable=False)
    day = Column(Integer, nullable=False)
    hour = Column(Integer, nullable=False)
    minute = Column(Integer, nullable=False)

    def __init__(
            self,
            month,
            day,
            hour,
            minute
    ):
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute

    def __repr__(self):
        return str(self.dict)

    @property
    def dict(self):
        return \
            {
                "dateid":    self.dateid,
                "month":  self.month,
                "day":    self.day,
                "hour":    self.hour,
                "minute": self.minute
            }


class Like(Base, Model):
    __tablename__ = "likes"
    likeid = Column(Integer, primary_key=True, nullable=False, autoincrement=True, unique=True)
    count = Column(Integer, nullable=False)

    def __init__(
            self
    ):
        self.count = 0

    def __repr__(self):
        return str(self.dict)

    @property
    def dict(self):
        return {
            "likeid":  self.likeid,
            "count": self.count
        }


class SubscribeItem(Base, Model):
    __tablename__ = "subscribers"
    subid = Column(Integer, primary_key=True, nullable=False, autoincrement=True, unique=True)
    eventid = Column(Integer, nullable=False)
    userid = Column(Integer, nullable=False)

    def __init__(self, eventid, subid):
        self.eventid = eventid
        self.subid = subid

    def __repr__(self):
        return str(self.dict)

    @property
    def dict(self):
        return {
            "eventid": self.eventid,
            "userid": self.userid
        }


class Attachment(Base, Model):
    __tablename__ = "message_attachments"
    _rowid_ = Column(Integer, primary_key=True, nullable=False, autoincrement=True, unique=True)
    messageid = Column(Integer, nullable=False)
    attachment_type = Column(Integer, nullable=False)
    attachment_link = Column(String, nullable=False)

    def __init__(
            self,
            messageid,
            attachment_type,
            attachment_link
    ):
        self.messageid = messageid
        self.attachment_type = attachment_type
        self.attachment_link = attachment_link

    def __repr__(self):
        return str(self.dict)

    @property
    def dict(self):
        return {
            "attachment_type": self.attachment_type,
            "attachment_link": self.attachment_link
        }


class Chat(Base, Model):
    __tablename__ = "chats"
    _rowid_ = Column(Integer, primary_key=True, nullable=False, autoincrement=True, unique=True)
    chatid = Column(Integer, nullable=False)
    userid = Column(Integer, nullable=False)

    def __init__(
            self,
            chatid: int,
            userid: int
    ):
        self.chatid = chatid
        self.userid = userid

    def __repr__(self):
        return str(self.dict)

    @property
    def dict(self):
        return {
            "chatid": self.chatid,
            "userid": self.userid
        }
