from flask import Flask, redirect, url_for, request, jsonify, json, abort, render_template, make_response, Response
from app import jsonrpc
# from app import model
from app import app, db
# from app import cache
from app.tasks import send_mail
from app.database.models import Member, Chat, Users, Message, Attachment
from .utils import is_authorized
from .utils import crossdomain
from base64 import b64encode


from authlib.flask.client import OAuth
import requests
from app.forms import SearchUsersForm

from .instance.auth_config import VK_CREDENTIALS as config

app.secret_key = 'development'

session = {'user_id': None, 'access_token': None}

oauth = OAuth(app)

vkontakte = oauth.register(
    'vk',
    client_id=config['consumer_id'],
    client_secret=config['consumer_secret'],
    access_token_method='POST',
    api_base_url='https://api.vk.com/method/',
    access_token_url=' https://oauth.vk.com/access_token',
    authorize_url='https://oauth.vk.com/authorize',
    client_kwargs={'scope': 'user_id email', 'response_type': 'code', 'v': 5.92, \
                   'display': 'page'},
)


@app.route('/check_auth', methods=["POST", "OPTIONS"])
@crossdomain(origin='*')
def check_auth():
    data = json.loads(request.get_data())
    if data['email'] == 'admin@mail.ru' and data['password'] == 'admin01':
        sum_ = (data['email'] + '&' + data['password']).encode('utf-8')
        stub = {"token": b64encode(sum_)}
        print(stub)
        return jsonify(stub)
    else:
        return abort(401)


@app.route('/login')
def login():
    redirect_uri = url_for('authorize', _external=True)
    return oauth.vk.authorize_redirect(redirect_uri)


@app.route('/authorize')
def authorize():
    redirect_uri = url_for('authorize', _external=True)
    code = request.args.get('code')
    cid = config['consumer_id']
    csecret = config['consumer_secret']
    resp = requests.get(
        f'https://oauth.vk.com/access_token?client_id={cid}&client_secret={csecret}&redirect_uri={redirect_uri}&code={code}')
    json_ = json.loads(resp.content)
    session['access_token'] = json_['access_token']
    session['user_id'] = json_['user_id']
    # new_user = model.create_user(str(json_['user_id']))
    user = Users(name='test_oauth_name', nick='test_oauth_nick')
    db.session.add(user)
    db.session.commit()
    return redirect('/')


#@is_authorized(session['user_id'])
@jsonrpc.method('list_chats(user_id=Number) -> Object', validate=True)
def list_chats(user_id):
    members = Member.query.filter_by(user_id=user_id).all()
    chats_info = list(map(lambda el: el.chat_.as_dict(), members))
    return chats_info


#@is_authorized(session['user_id'])
# @crossdomain(origin='*')
@jsonrpc.method('search_users', validate=True)
def search_users(query, limit):
    # print(*request.form)
    form = SearchUsersForm(query=query, limit=limit)
    print(form.validate())
    if form.validate():
        users = Users.query.filter(Users.nick.like(f'%{query}%')).limit(limit).all()
        searched_users_info = list(map(lambda el: el.as_dict(), users))
        return searched_users_info


@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
    name = request.args.get('name')
    nick = request.args.get('nick')
    user = Users(name=name, nick=nick)
    db.session.add(user)
    db.session.commit()
    print(user.as_dict(), 'USER')
    return jsonify(user.as_dict())

@jsonrpc.method('delete_user(id=Number) -> Object', validate=True)
def delete_user(id):
    user = Users.query.filter(Users.id == id).delete()
    # db.session.add(user)
    db.session.commit()
    return 'OK'



#@is_authorized(session['user_id'])
@jsonrpc.method('create_pers_chat(user_id=Number, companion_id=Number) -> Object', validate=True)
# @app.route('/create_chat')
def create_pers_chat(user_id, companion_id):
    # cache.set(f'{user_id}', {}, timeout=86400)
    chat = Chat(is_group_chat=False)
    db.session.add(chat)
    db.session.commit()
    member1 = Member(user_id=user_id, chat_id=chat.id)
    member2 = Member(user_id=companion_id, chat_id=chat.id)
    db.session.add(member1)
    db.session.add(member2)
    db.session.commit()

    task = send_mail.delay()
    return chat.as_dict()

#@is_authorized(session['user_id'])
@jsonrpc.method('send_message(user_id=Number, chat_id=Number, content=String) -> Object', validate=True)
# @crossdomain(origin='*')
def send_message(user_id, chat_id, content):
    message = Message(chat_id=chat_id, user_id=user_id, content=content)
    db.session.add(message)
    db.session.commit()
    message.chat.last_message = content
    # TO-DO: fix group and non-group chat messages
    if message.chat.users[0] != user_id and message.chat.is_group_chat is False:
        if message.chat.users[0].new_messages:
            message.chat.users[0].new_messages += 1
        else:
            message.chat.users[0].new_messages = 1
    else:
        if message.chat.users[1].new_messages:
            message.chat.users[1].new_messages += 1
        else:
            message.chat.users[1].new_messages = 1

    db.session.commit()

    return 'OK'


#@is_authorized(session['user_id'])
@jsonrpc.method('list_messages(chat_id=Number, limit=Number) -> Object', validate=True)
def list_messages(chat_id, limit):
    messages = Message.query.filter_by(chat_id=chat_id).limit(limit).all()
    list_ = list(map(lambda el: el.as_dict(), messages))
    return list_


#@is_authorized(session['user_id'])
@jsonrpc.method('read_message(message_id=Number) -> Object', validate=True)
def read(message_id):
    return Message.query.filter_by(message_id=message_id).first().as_dict()



# @app.route('/', methods=['GET', 'POST', 'OPTIONS'])
# @crossdomain(origin='*')
# def index():
#     if request.method == 'POST' or request.method == 'OPTIONS':
#         data = json.loads(request.get_data())
#         print(data)
#         if data['method'] == "list_chats":
#             chats = model.list_chats(data['params']['user_id'])
#             print(chats)
#             return jsonify(chats)
#         return abort(500)
#
#     else:
#         return render_template('root.html')
