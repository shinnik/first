from urllib import request
from flask import jsonify
import unittest
from jsondiff import diff
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


def api_post(api_name, datatype):

    data = b'this_is_post_request'
    req = request.urlopen(f'http://127.0.0.1:5050/api/{api_name}/', data)

    if datatype == 'code':
        return req.getcode()
    if datatype == 'mime-type':
        return req.info()['Content-Type']
    if datatype == 'data':
        with req as resp:
            result_json = resp.read().decode('utf-8')
            return result_json


def api_get(api_name, get_params, datatype):

    data = None
    req = request.urlopen(f'http://127.0.0.1:5050/api/{api_name}/?{get_params}', data)

    if datatype == 'code':
        return req.getcode()
    if datatype == 'mime-type':
        return req.info()['Content-Type']
    if datatype == 'data':
        with req as resp:
            result_json = resp.read().decode('utf-8')
            return result_json


def are_jsons_same(json1, json2):
    result = diff(json1, json2)
    if result == {}:
        return True
    else:
        return False


class TestStubs(unittest.TestCase):

        def test_search_users(self):
            with app.app_context():

                api = 'search_users'
                params = 'query=1&limit=5'

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

                expected_data = jsonify({"users": [user1, user2]}).data.decode('utf-8')
                obtained_data = api_get(api, params, 'data')

                self.assertEqual(api_get(api, params, 'code'), 200)
                self.assertEqual(api_get(api, params, 'mime-type'), 'application/json')
                self.assertTrue(are_jsons_same(obtained_data, expected_data))

        def test_search_chats(self):
            with app.app_context():

                api = 'search_chats'
                params = 'query=1&limit=5'

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

                expected_data = jsonify({"chats": [chat1, chat2]}).data.decode('utf-8')
                obtained_data = api_get(api, params, 'data')

                self.assertEqual(api_get(api, params, 'code'), 200)
                self.assertEqual(api_get(api, params, 'mime-type'), 'application/json')
                self.assertTrue(are_jsons_same(obtained_data, expected_data))


        def test_get_chat_list(self):
            with app.app_context():

                api = 'list_chats'
                params = ''

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

                expected_data = jsonify({"chats": [chat1, chat2]}).data.decode('utf-8')
                obtained_data = api_get(api, params, 'data')

                self.assertEqual(api_get(api, params, 'code'), 200)
                self.assertEqual(api_get(api, params, 'mime-type'), 'application/json')
                self.assertTrue(are_jsons_same(obtained_data, expected_data))

        def test_create_pers_chat(self):
            with app.app_context():

                api = 'create_pers_chat'
                params = 'user_id=3'

                chat = {
                    'chat_id': 3,
                    'is_group_chat': False,
                    'topic': 'Rampart',
                    'last_message': 'Centaurus win',
                    'new_messages': 41,
                    'last_read_message_id': 55
                }

                expected_data = jsonify({"chat": chat}).data.decode('utf-8')
                obtained_data = api_post(api, 'data')

                self.assertEqual(api_post(api, 'code'), 200)
                self.assertEqual(api_post(api, 'mime-type'), 'application/json')
                self.assertTrue(are_jsons_same(obtained_data, expected_data))

        def test_create_group_chat(self):
            with app.app_context():
                api = 'create_group_chat'
                params = 'user_id=3'

                chat = {
                    'chat_id': 4,
                    'is_group_chat': False,
                    'topic': 'Necropolis',
                    'last_message': 'We need to kick Septienna off',
                    'new_messages': 111,
                    'last_read_message_id': 201
                }

                expected_data = jsonify({"chat": chat}).data.decode('utf-8')
                obtained_data = api_post(api, 'data')

                self.assertEqual(api_post(api, 'code'), 200)
                self.assertEqual(api_post(api, 'mime-type'), 'application/json')
                self.assertTrue(are_jsons_same(obtained_data, expected_data))

        def test_add_members_to_group_chat(self):
            with app.app_context():

                api = 'add_members_to_group_chat'
                params = 'user_id=3'

                expected_data = jsonify({}).data.decode('utf-8')
                obtained_data = api_post(api, 'data')

                self.assertEqual(api_post(api, 'code'), 200)
                self.assertEqual(api_post(api, 'mime-type'), 'application/json')
                self.assertTrue(are_jsons_same(obtained_data, expected_data))

        def test_leave_group_chat(self):
            with app.app_context():

                api = 'leave_group_chat'
                params = 'user_id=3'

                expected_data = jsonify({}).data.decode('utf-8')
                obtained_data = api_post(api, 'data')

                self.assertEqual(api_post(api, 'code'), 200)
                self.assertEqual(api_post(api, 'mime-type'), 'application/json')
                self.assertTrue(are_jsons_same(obtained_data, expected_data))

        def test_send_message(self):
            with app.app_context():

                api = 'send_message'

                message = {
                    'message_id': '198',
                    'chat_id': 'chat_id',
                    'user_id': '22',
                    'content': 'content',
                    'added_at': '1540198594'
                }

                expected_data = jsonify({'message': message}).data.decode('utf-8')
                obtained_data = api_post(api, 'data')

                self.assertEqual(api_post(api, 'code'), 200)
                self.assertEqual(api_post(api, 'mime-type'), 'application/json')
                self.assertTrue(are_jsons_same(obtained_data, expected_data))

        def test_read_message(self):
            with app.app_context():

                api = 'read_message'
                params = 'message_id=198'

                chat = {
                    'chat_id': '5',
                    'is_group_chat': 'False',
                    'topic': 'Inferno',
                    'last_message': 'Get through gate of hell',
                    'new_messages': '123',
                    'last_read_message_id': '321'
                }

                expected_data = jsonify({'chat': chat}).data.decode('utf-8')
                obtained_data = api_get(api, params, 'data')

                self.assertEqual(api_get(api, params, 'code'), 200)
                self.assertEqual(api_get(api, params, 'mime-type'), 'application/json')
                self.assertTrue(are_jsons_same(obtained_data, expected_data))

        def test_load_file(self):
            with app.app_context():

                api = 'upload_file'

                attach = {
                    'attach_id': '1',
                    'message_id': '155',
                    'chat_id': '5',
                    'user_id': '44',
                    'type': 'image',
                    'url': 'pics/r83Jdf1Jd38d912n.jpg'
                }

                expected_data = jsonify({'attach': attach}).data.decode('utf-8')
                obtained_data = api_post(api, 'data')

                self.assertEqual(api_post(api, 'code'), 200)
                self.assertEqual(api_post(api, 'mime-type'), 'application/json')
                self.assertTrue(are_jsons_same(obtained_data, expected_data))


if __name__ == "__main__":
    with app.app_context():
        unittest.main()


