import unittest
import json

from app import app


class JSONRPCTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_list_chats(self):
        rpc_query = {"jsonrpc": "2.0", "method": "list_chats", \
                     "params": {"user_id": 4}, "id": 1}

        rv = self.app.post('/api', data=json.dumps(rpc_query), content_type='application/json')
        print(json.loads(rv.data)["0"]["last_message"])
        self.assertEqual(json.loads(rv.data)["0"]["last_message"], "hello")

    def test_search_users(self):
        rpc_query = {"jsonrpc": "2.0", "method": "search_users", \
                     "params": {"query": "li", "limit": "5"}, "id": 1}

        rv = self.app.post('/api', data=json.dumps(rpc_query), content_type='application/json')
        #print(json.loads(rv.data)["0"]["last_message"])
        self.assertEqual(json.loads(rv.data)["0"]["name"], "Asya")

    def test_create_pers_chat(self):
        rpc_query = {"jsonrpc": "2.0", "method": "create_pers_chat", \
                     "params": {"user_id": "2", "companion_id": "4"}, "id": 1}

        rv = self.app.post('/api', data=json.dumps(rpc_query), content_type='application/json')
        #print(json.loads(rv.data))
        self.assertEqual(json.loads(rv.data)["chat_id"], 10)

    def test_send_message(self):
        rpc_query = {"jsonrpc": "2.0", "method": "send_message", \
                     "params": {"user_id": "2", "chat_id": "10", "content": "hello"}, "id": 1}

        rv = self.app.post('/api', data=json.dumps(rpc_query), content_type='application/json')
        #print(json.loads(rv.data))
        self.assertEqual(json.loads(rv.data)["content"], "hello")

    def test_list_messages(self):
        rpc_query = {"jsonrpc": "2.0", "method": "list_messages", \
                     "params": {"chat_id": "0", "limit": "5"}, "id": 1}
        rv = self.app.post('/api', data=json.dumps(rpc_query), content_type='application/json')
        #print(json.loads(rv.data))
        self.assertEqual(json.loads(rv.data)["0"]["message_id"], 0)

    def test_read(self):
        rpc_query = {"jsonrpc": "2.0", "method": "read_message", \
                     "params": {"user_id": "4", "message_id": "28"}, "id": 1}
        rv = self.app.post('/api', data=json.dumps(rpc_query), content_type='application/json')
        #print(json.loads(rv.data))
        self.assertEqual(json.loads(rv.data)["last_read_message_id"], 28)



if __name__ == "__main__":
    unittest.main()