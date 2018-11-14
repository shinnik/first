from flask import request, jsonify, render_template
from app import jsonrpc
from app import model
from app import app


@jsonrpc.method('list_chats(user_id=Number) -> Object', validate=True)
def chats(user_id):
    chats = model.list_chats(user_id)
    return jsonify(chats)


@jsonrpc.method('search_users(query=String, limit=Number) -> Object', validate=True)
def search_users(query, limit):
    users = model.get_users_by_query(query, limit)
    return jsonify(users)


@jsonrpc.method('create_pers_chat(user_id=Number, companion_id=Number) -> Object', validate=True)
def create_pers_chat(user_id, companion_id):
    # user_id will be taken from authorization
    rv = model.create_p_chat(user_id, companion_id)
    return jsonify(rv)


@jsonrpc.method('send_message(user_id=Number, chat_id=Number, content=String) -> Object', validate=True)
def send_message(user_id, chat_id, content):
    rv = model.send(user_id, chat_id, content)
    return jsonify(rv)


@jsonrpc.method('list_messages(chat_id=Number, limit=Number) -> Object', validate=True)
def list_messages(chat_id, limit):
    rv = model.list_messages_by_chat(chat_id, limit)
    return jsonify(rv)


@jsonrpc.method('read_message(user_id=Number, message_id=Number) -> Object', validate=True)
def read(user_id, message_id):
    rv = model.read(user_id, message_id)
    return jsonify(rv)
