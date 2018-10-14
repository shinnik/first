import pprint
import json
import datetime

def wsgi_application(environ, start_response):
	status = '200 OK'
	headers = [('content-type', 'application/json')]
	time = str(datetime.datetime.now().time())
	info = json.dumps(
	{"data": {"time": time, "url": 			environ["HTTP_HOST"].encode("utf-8")},
	"content-type": "application/json"}
	)
	start_response(status, headers)
	return [ info ]
