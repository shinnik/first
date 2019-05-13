from app import app
from werkzeug.contrib.profiler import ProfilerMiddleware

# app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[30])
