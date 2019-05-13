#! /usr/bin/python3
import redis
from app import app
# from werkzeug.contrib.profiler import ProfilerMiddleware
from flask_script import Manager
from flask_migrate import MigrateCommand


manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
    # app.config['PROFILE'] = True
    # app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[30])
    app.run(debug=True)
    # manager.run()

