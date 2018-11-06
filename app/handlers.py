from flask import request, jsonify, render_template
from app import model
from app import app


@app.route('/api/list_chats/')
def chats():
    user_id = int(request.args.get('user_id'))
    chats = model.list_chats(user_id)
    return jsonify(chats)


@app.route('/api/search_users/')
def search_users():
    query = str(request.args.get('query'))
    limit = int(request.args.get('limit'))
    users = model.get_users_by_query(query, limit)
    return jsonify(users)


@app.route('/api/create_pers_chat/', methods=['GET', 'POST'])
def create_pers_chat():
    # it will be taken from authorization
    user_id = 2
    if request.method == 'GET':
        return render_template('create_pers_chat.html')
    if request.method == 'POST':
        print(request.form)
        companion_id = int(request.form['companion_id'])
        rv = model.create_p_chat(user_id, companion_id)
        return jsonify(rv)

