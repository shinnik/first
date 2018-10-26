from flask import json, request, abort, jsonify, make_response, render_template, Response

from app import app


@app.route("/login/")
def login():

    """
    oauth2 authentification will be here
    """
    pass


@app.route("/api/search_users/", methods=["GET"])
def search():
    if request.method == "GET":
        args = request.args.to_dict()
        query = str(args['query'])
        limit = int(args['limit'])

        # it will be database logic on this place

        user1 = {
            'user_id': 1,
            'nick': 'Septienna',
            'name': 'Vokial',
            'avatar': 'avatar1.png'
        }

        user2 = {
            'user_id': 2,
            'nick': 'Lord Haart',
            'name': 'Sandro',
            'avatar': 'avatar2.png'
        }

        resp = jsonify({"users": [user1, user2]})
        resp.content_type = 'application/json'
        resp.status_code = 200

        return resp

    else:
        resp = jsonify({})
        resp.status_code = 404
        return resp


@app.route("/api/search_chats/", methods=["GET"])
def search_chat():
    if request.method == "GET":
        args = request.args.to_dict()
        query = str(args['query'])
        limit = int(args['limit'])

        # it will be database logic here

        chat1 = {
            'chat_id': 1,
            'is_group_chat': True,
            'topic': 'Necropolis',
            'last_message': 'I am vampire lord',
            'new_messages': 14,
            'last_read_message_id': 149
        }

        chat2 = {
            'chat_id': 2,
            'is_group_chat': False,
            'topic': 'Castle',
            'last_message': 'I am looking forward to Monday',
            'new_messages': 11,
            'last_read_message_id': 87
        }

        resp = jsonify({"chats": [chat1, chat2]})
        resp.content_type = 'application/json'
        resp.headers['status_code'] = 200

        return resp

    else:
        resp = jsonify({})
        resp.status_code = 404
        return resp


@app.route("/api/list_chats/", methods=["GET"])
def get_chat_list():
    if request.method == "GET":

        # database logic will be here

        chat1 = {
            'chat_id': 1,
            'is_group_chat': True,
            'topic': 'Necropolis',
            'last_message': 'I am vampire lord',
            'new_messages': 14,
            'last_read_message_id': 149
        }

        chat2 = {
            'chat_id': 2,
            'is_group_chat': False,
            'topic': 'Castle',
            'last_message': 'I am looking forward to Monday',
            'new_messages': 11,
            'last_read_message_id': 87
        }

        resp = jsonify({"chats": [chat1, chat2]})
        resp.content_type = 'application/json'
        resp.headers['status_code'] = 200

        return resp

    else:
        resp = jsonify({})
        resp.status_code = 404
        return resp


@app.route("/api/create_pers_chat/", methods=["GET", "POST"])
def create_chat():
    if request.method == "GET":
        user_id = int(request.args.post('user_id'))

    if request.method == "POST":

        # database logic will be here

        chat = {
            'chat_id': 3,
            'is_group_chat': False,
            'topic': 'Rampart',
            'last_message': 'Centaurus win',
            'new_messages': 41,
            'last_read_message_id': 55
        }

        resp = jsonify({'chat': chat})
        resp.status_code = 200
        resp.content_type = 'application/json'

        return resp
    else:
        resp = jsonify({})
        resp.status_code = 404
        return resp


@app.route("/api/create_group_chat/", methods=["GET", "POST"])
def create_group_chat():

    if request.method == "GET":
        topic = str(request.args.get('topic'))

    if request.method == "POST":

        #database logic here

        chat = {
            'chat_id': 4,
            'is_group_chat': False,
            'topic': 'Necropolis',
            'last_message': 'We need to kick Septienna off',
            'new_messages': 111,
            'last_read_message_id': 201
        }

        resp = jsonify({'chat': chat})
        resp.status_code = 200
        resp.content_type = 'application/json'

        return resp


@app.route("/api/add_members_to_group_chat/", methods=["GET", "POST"])
def add_user_to_chat():

    if request.method == "GET":

        chat_id = request.args.get('chat_id')
        user_ids = request.args.getlist('user_ids')

    if request.method == "POST":

        # database logic will be here

        resp = jsonify({})
        resp.status_code = 200
        resp.content_type = 'application/json'

        return resp


@app.route("/api/leave_group_chat/", methods=["GET", "POST"])
def quit_chat():

    if request.method == "GET":
        chat_id = int(request.args.get('chat_id'))

    if request.method == "POST":

       # database logic will be here

        resp = jsonify({})
        resp.status_code = 200
        resp.content_type = 'application/json'

        return resp


@app.route("/api/send_message/", methods=["GET","POST"])
def send_message():

    if request.method == "GET":
        args = request.args.to_dict()
        chat_id = int(args['chat_id'])
        content = str(args['content'])
        attach_id = int(args['attach_id'])

    if request.method == "POST":

        message = {
            'message_id': '198',
            'chat_id': 'chat_id',
            'user_id': '22',
            'content': 'content',
            'added_at': '1540198594'
        }

        resp = jsonify({'message': message})
        resp.status_code = 200
        resp.content_type = 'application/json'

        return resp



@app.route("/api/read_message/", methods=["GET"])
def read_message():
    if request.method == "GET":
        message_id = int(request.args.get('message_id'))

        chat = {
            'chat_id': '5',
            'is_group_chat': 'False',
            'topic': 'Inferno',
            'last_message': 'Get through gate of hell',
            'new_messages': '123',
            'last_read_message_id': '321'
        }

        resp = jsonify({'chat': chat})
        resp.status_code = 200
        resp.content_type = 'application/json'

        return resp

    else:
        resp = jsonify({})
        resp.status_code = 404
        return resp


@app.route("/api/upload_file/", methods=["GET", "POST"])
def load_file():

    if request.method == "GET":
        args = request.args.to_dict()
        chat_id = args['chat_id']
        content = args['content']

    if request.method == "POST":

        attach = {
            'attach_id': '1',
            'message_id': '155',
            'chat_id': '5',
            'user_id': '44',
            'type': 'image',
            'url': 'pics/r83Jdf1Jd38d912n.jpg'
        }

        resp = jsonify({'attach': attach})
        resp.status_code = 200
        resp.content_type = 'application/json'

        return resp


