from sqlalchemy import Column, String, Integer
from database.database import Base, db_session


class Message(Base):
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

    def put(self):
        db_session.add(self)
        db_session.commit()

    #why not?
    @staticmethod
    def clear_all():
        deleted = Message.query.delete()
        db_session.commit()
        return deleted

    @property
    def dict(self):
        return \
            {
                "_rowid_": self._rowid_,
                "text": self.text,
                "sender":
                    User.query.filter(User.userid==self.sender)
                        .first()
                        .username
            }


class User(Base):
    __tablename__ = "users"
    userid = Column(Integer, primary_key=True, nullable=False, autoincrement=True, unique=True)
    username = Column(String(), nullable=False)
    telephone = Column(String(), nullable=False)
    status = Column(String())
    avatar = Column(String())

    def __init__(self, username, telephone, status="", avatar = ""):
        self.username = username
        self.telephone = telephone
        self.status = status
        self.avatar = avatar

    def __repr__(self):
        return str(self.dict)

    def put(self):
        db_session.add(self)
        db_session.commit()

    # why not?
    @staticmethod
    def clear_all():
        deleted = Message.query.delete()
        db_session.commit()
        return deleted

    @property
    def dict(self):
        return \
            {
                "userid":    self.userid,
                "username":  self.username,
                "status":    self.status,
                "avatar":    self.avatar,
                "telephone": self.telephone
            }
