from app import db
from flask import jsonify
import datetime


def get_chat_ids(user_id):
    ids = []
    chats_where_member = db.query_all("""
        SELECT chat_id FROM members
        WHERE user_id = %(user_id)s
        """, user_id=int(user_id))

    for key, value in chats_where_member.items():
        ids.append(value['chat_id'])

    return ids


def list_chats(user_id, limit=5):
    chats = {}
    ids = get_chat_ids(user_id)

    for index, chat_id in enumerate(ids):
        chats.update({index: db.query_one("""
        SELECT * FROM chats
        WHERE chat_id = %(chat_id)s""", chat_id=chat_id)})
    return chats


def get_users_by_query(query, limit):
    query = query+':*'
    return db.query_all("""
    SELECT * FROM users
    WHERE to_tsvector(nick) @@ to_tsquery(%(query)s)
    OR to_tsvector(name) @@ to_tsquery(%(query)s)
    LIMIT %(limit)s""", query=str(query), limit=int(limit))


def create_new_chat():
    return db.execute_and_return_new("""
        INSERT INTO chats (is_group_chat, topic, last_message) 
        VALUES (false, '', '')
        RETURNING chat_id""")


def create_new_message(id, cid, content):
    return db.execute_and_return_new("""
        INSERT INTO messages (user_id, content, chat_id)
        VALUES (%(id)s, %(content)s, %(cid)s)
        RETURNING message_id""", id=id, cid=cid, content=content)


def create_p_chat(id1, id2):
    ids1 = set(get_chat_ids(id1))
    ids2 = set(get_chat_ids(id2))
    matches = list(ids1 & ids2)
    if not matches:
        last_id = create_new_chat()
        db.execute("""
        INSERT INTO members (user_id, chat_id, new_messages, last_read_message_id)
        VALUES (%(id1)s, %(last_id)s, 0, 0)""", id1=id1, last_id=last_id)
        db.execute("""
        INSERT INTO members (user_id, chat_id, new_messages, last_read_message_id)
        VALUES (%(id2)s,%(last_id)s, 0, 0)""", id2=id2, last_id=last_id)
        return 'OK'
    else:
        id = matches[0]
        return db.query_one("""
        SELECT * FROM chats
        WHERE chat_id=%(id)s
        AND is_group_chat=false""", id=id)


def send(user_id, chat_id, content):
    last_message_id = create_new_message(user_id, chat_id, content)
    db.execute("""
        UPDATE chats
        SET last_message=%(content)s
        WHERE chat_id=%(chat_id)s""", content=content, chat_id=chat_id)
    db.execute("""
        UPDATE members
        SET new_messages=new_messages+1
        WHERE chat_id=%(chat_id)s
        AND user_id<>%(user_id)s""", chat_id=chat_id, user_id=user_id)
    db.execute("""
        UPDATE chats
        SET new_messages=new_messages+1
        WHERE chat_id=%(chat_id)s
        """, chat_id=chat_id, user_id=user_id)
    message = {
        'message_id': last_message_id,
        'user_id': user_id,
        'content': content,
        'added_at': str(datetime.datetime.time(datetime.datetime.now())),
        'chat_id': chat_id
    }
    return message


def list_messages_by_chat(chat_id, limit):
    return db.query_all("""
        SELECT user_id, nick, name,
        message_id, content, added_at
        FROM messages
        JOIN users USING (user_id)
        WHERE chat_id = %(chat_id)s
        ORDER BY added_at DESC
        LIMIT %(limit)s
        """, chat_id=int(chat_id), limit=int(limit))


def read(user_id, message_id):
    print(message_id)
    target_chat = db.query_one("""
    SELECT chat_id FROM messages
    WHERE message_id=%(message_id)s""", message_id=message_id)
    chat_id = target_chat['chat_id']
    print(chat_id)

    db.execute("""
    UPDATE members
    SET new_messages=new_messages-1,
    last_read_message_id=%(message_id)s
    WHERE user_id=%(user_id)s
    AND chat_id=%(chat_id)s""", user_id=user_id, chat_id=chat_id, message_id=message_id)

    db.execute("""
    UPDATE chats
    SET new_messages=new_messages-1,
    last_read_message_id=%(message_id)s
    WHERE chat_id=%(chat_id)s""", chat_id=chat_id, message_id=message_id)

    return db.query_one("""
    SELECT * FROM chats
    WHERE chat_id=%(chat_id)s""", chat_id=chat_id)


def create_user(vk_user_id):
    # check if user is in the database or not
    try:
        return db.query_one("""
        SELECT * FROM users
        WHERE vk_id=%(vk_user_id)s""", vk_user_id=vk_user_id)
    except TypeError:
        return db.execute_and_return_new("""
                INSERT INTO users (nick, name, vk_id) 
                VALUES ('new_nick', 'new_name', 'vk_user_id')
                RETURNING user_id""")
