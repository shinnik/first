import pprint
import json
import datetime

def wsgi_application(environ, start_response):
	status = '200 OK'
	headers = [('content-type', 'application/json')]
	time = str(datetime.datetime.now().time())
	uri = "".join([environ["HTTP_HOST"], environ["RAW_URI"]])
	info = json.dumps(
	{"data": {"time": time, "uri": uri},
	"content-type": "application/json"}
	)
	start_response(status, headers)
	return [ info ]
