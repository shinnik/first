from flask import Flask, redirect, url_for, session, request, jsonify, json
from authlib.flask.client import OAuth

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
    client_kwargs={'scope': 'user_id email', 'response_type': 'token', 'v': 5.87, \
                   'display': 'page'},
)


@app.route('/login')
def login():
    redirect_uri = url_for('authorize', _external=True)
    print(redirect_uri)
    #redirect_uri = 'https://oauth.vk.com/blank.html'
    resp = oauth.vk.authorize_redirect(redirect_uri)
    print(json.dumps(resp.data))
    return oauth.vk.authorize_redirect(redirect_uri)


@app.route('/authorize')
def authorize():
    # this is a pseudo method, you need to implement it yourself
    print(token)
    return redirect(url_for('profile'))


@app.route('/profile')
def twitter_profile():
    resp = oauth.vk.get('account/verify_credentials.json')
    profile = resp.json()
    print(profile)
