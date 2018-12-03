from flask import Flask, redirect, url_for, session, request, jsonify, json, abort
from authlib.flask.client import OAuth
import requests

from app import model
from .instance.auth_config import VK_CREDENTIALS as config
from app import app

app.secret_key = 'development'

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
    session['user'] = json_['user_id']
    new_user = model.create_user(str(json_['user_id']))
    return jsonify(new_user)


@app.route('/')
def root():
   return "main page"



