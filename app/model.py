from app import db
import json


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
    return db.create("""
        INSERT INTO chats (is_group_chat, topic, last_message) 
        VALUES (false, '', '')
        RETURNING chat_id""")

def create_p_chat(id1, id2):
    ids1 = set(get_chat_ids(id1))
    ids2 = set(get_chat_ids(id2))
    matches = list(ids1 & ids2)
    if not matches:
        last_id = create_new_chat()
        db.insert("""
        INSERT INTO members (user_id, chat_id, new_messages, last_read_message_id)
        VALUES (%(id1)s, %(last_id)s, 0, 0)""", id1=id1, last_id=last_id)
        db.insert("""
        INSERT INTO members (user_id, chat_id, new_messages, last_read_message_id)
        VALUES (%(id2)s,%(last_id)s, 0, 0)""", id2=id2, last_id=last_id)
        return 'OK'
    else:
        id = matches[0]
        return db.query_one("""
        SELECT * FROM chats
        WHERE chat_id=%(id)s
        AND is_group_chat=false""", id=id)