from urllib import request
import requests as req
from flask import jsonify
import unittest
from jsondiff import diff
import json
import sys
import os


def change_path_to_import_app():
    if sys.path[0] == '':
        sys.path[0] = os.getcwd()
    for num, el in enumerate(sys.path[0][::-1]):
        if el != '/':
            continue
        else:
            end_symbol_num = num
            break
    new_path = sys.path[0][:len(sys.path[0])-end_symbol_num:]
    sys.path.insert(0, new_path)

change_path_to_import_app()
from app import app


def are_jsons_same(json1, json2):
    result = diff(json1, json2)
    if result == {}:
        return True
    else:
        return False


class TestAPI(unittest.TestCase):

        def test_search_users(self):
            with app.app_context():

                api = 'search_users'
                params = 'query=li&limit=5'

                expected_data = {
                    "0": {
                        "avatar": None,
                        "name": "Asya",
                        "nick": "lisa",
                        "user_id": 2
                    }
                }

                r = req.get(f'http://127.0.0.1:5050/api/{api}/?{params}')
                obtained_data = json.loads(r.content.decode('utf-8'))

                self.assertEqual(r.status_code, 200)
                self.assertEqual(r.headers["Content-Type"], 'application/json')
                self.assertTrue(are_jsons_same(obtained_data, expected_data))

        def test_get_chat_list(self):
            with app.app_context():

                api = 'list_chats'
                params = 'user_id=4'

                expected_data = {
                    '0': {
                        'chat_id': 10,
                        'is_group_chat': False,
                        'last_message': 'hello',
                        'last_read_message_id': 28,
                        'new_messages': None,
                        'topic': ''
                    }}

                r = req.get(f'http://127.0.0.1:5050/api/{api}/?{params}')
                obtained_data = json.loads(r.content.decode('utf-8'))

                self.assertEqual(r.status_code, 200)
                self.assertEqual(r.headers["Content-Type"], 'application/json')
                self.assertTrue(are_jsons_same(obtained_data, expected_data))

        def test_create_pers_chat(self):
            with app.app_context():

                user_id = 2

                api = 'create_pers_chat'

                expected_data = {
                    "chat_id": 1,
                    "is_group_chat": False,
                    "last_message": "",
                    "last_read_message_id": None,
                    "new_messages": None,
                    "topic": ""
                }

                r = req.post(f'http://127.0.0.1:5050/api/{api}/', data={"companion_id": 3})
                obtained_data = json.loads(r.content.decode('utf-8'))

                self.assertEqual(r.status_code, 200)
                self.assertEqual(r.headers["Content-Type"], 'application/json')
                self.assertTrue(are_jsons_same(obtained_data, expected_data))




if __name__ == "__main__":
    with app.app_context():
        unittest.main()


