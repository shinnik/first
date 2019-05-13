import postgresql
from random import randint
import time
import datetime

with postgresql.open(user = "quack", host = "localhost", port = "5432", password = "quack") as db:
    ins_users = db.prepare("INSERT INTO users (nick, name) VALUES ($1, $2)")
    ins_chats = db.prepare("INSERT INTO chats (is_group_chat, topic, last_message,  new_messages, last_read_message_id) VALUES ($1, $2, $3, $4, $5)")
    ins_members = db.prepare("INSERT INTO members (user_id, chat_id, new_messages, last_read_message_id) VALUES ($1, $2, $3, $4)")
    ins_messages = db.prepare("INSERT INTO messages (user_id, content, chat_id) VALUES ($1, $2, $3)")
    for i in range(10):
        ins_messages(4, f"message {i}", 17)


