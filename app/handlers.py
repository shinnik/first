from flask import Flask, redirect, url_for, request, jsonify, json, abort, render_template
from app import jsonrpc
from app import model
from app import app
from .utils import is_authorized


from authlib.flask.client import OAuth
import requests

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
    new_user = model.create_user(str(json_['user_id']))
    return redirect('/')


@is_authorized(session['user_id'])
@jsonrpc.method('list_chats(user_id=Number) -> Object', validate=True)
def chats(user_id):
    chats = model.list_chats(user_id)
    return jsonify(chats)


@is_authorized(session['user_id'])
@jsonrpc.method('search_users(query=String, limit=Number) -> Object', validate=True)
def search_users(query, limit):
    users = model.get_users_by_query(query, limit)
    return jsonify(users)


@is_authorized(session['user_id'])
@jsonrpc.method('create_pers_chat(user_id=Number, companion_id=Number) -> Object', validate=True)
def create_pers_chat(user_id, companion_id):
    # user_id will be taken from authorization
    rv = model.create_p_chat(user_id, companion_id)
    return jsonify(rv)


@is_authorized(session['user_id'])
@jsonrpc.method('send_message(user_id=Number, chat_id=Number, content=String) -> Object', validate=True)
def send_message(user_id, chat_id, content):
    rv = model.send(user_id, chat_id, content)
    return jsonify(rv)


@is_authorized(session['user_id'])
@jsonrpc.method('list_messages(chat_id=Number, limit=Number) -> Object', validate=True)
def list_messages(chat_id, limit):
    rv = model.list_messages_by_chat(chat_id, limit)
    return jsonify(rv)


@is_authorized(session['user_id'])
@jsonrpc.method('read_message(message_id=Number) -> Object', validate=True)
def read(message_id):
    user_id = session['user_id']
    rv = model.read(user_id, message_id)
    return jsonify(rv)


@is_authorized(session['user_id'])
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('root.html')