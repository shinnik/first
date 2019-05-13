from app import app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)


class Member(db.Model):

    user_id = db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
    chat_id = db.Column('chat_id', db.Integer, db.ForeignKey('chat.id'))
    new_messages = db.Column('new_messages', db.Integer)
    last_read_message_id = db.Column('last_read_message_id', db.Integer, db.ForeignKey('message.message_id'))

    user = db.relationship('Users', backref='chats', lazy=True)
    chat = db.relationship('Chat', backref='users', lazy=True)

    __table_args__= (db.PrimaryKeyConstraint('user_id', 'chat_id'),)

    def __repr__(self):
        return f'member {self.user_id}, {self.chat_id}'


class Users(db.Model):

    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(30), nullable=False)
    nick = db.Column('nick', db.String(30), unique=True, nullable=False)
    avatar = db.Column('avatar', db.String(200))

    messages = db.relationship('Message', backref='user', lazy=True)
    attachments = db.relationship('Attachment', backref='user', lazy=True)
    # chats = db.relationship('Chat', secondary=members, lazy='subquery', backref=db.backref('users', lazy=True))
    chats = db.relationship('Member', backref='user', lazy=True)

    def __repr__(self):
        return f'user {self.id}, {self.name}'


class Chat(db.Model):

    id = db.Column('id', db.Integer, primary_key=True)
    is_group_chat = db.Column('is_group_chat', db.BOOLEAN, nullable=False)
    topic = db.Column('topic', db.String)
    last = db.Column('last_message', db.String)

    messages = db.relationship('Message', backref='chat', lazy=True)
    users = db.relationship('Member', backref='chat', lazy=True)

    def __repr__(self):
        return f'chat number {self.id}'


class Message(db.Model):

    message_id = db.Column('message_id', db.Integer, primary_key=True)
    chat_id = db.Column('chat_id', db.Integer, db.ForeignKey('chat.id'))
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
    content = db.Column('content', db.String, nullable=False)
    added_at = db.Column('added_at', db.TIMESTAMP, nullable=False)

    def __repr__(self):
        return f'message number {self.mess_id} with chat {self.chat_id} and user_id {self.user_id}'


class Attachment(db.Model):

    attach_id = db.Column('attach_id', db.Integer, primary_key=True)
    chat_id = db.Column('chat_id', db.Integer, db.ForeignKey('chat.id'))
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
    message_id = db.Column('message_id', db.Integer, db.ForeignKey('message.message_id'))
    type = db.Column('type', db.String, nullable=False)
    url = db.Column('url', db.String, nullable=False)

    def __repr__(self):
        return f'attachment number {self.attach_id} with chat {self.chat_id} and user_id {self.user_id}'


if __name__ == "__main__":
    db.create_all()

