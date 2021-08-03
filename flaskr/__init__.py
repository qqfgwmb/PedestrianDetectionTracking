# gevent
from gevent import monkey
from gevent.pywsgi import WSGIServer
# 下面这句不加也能启动服务，但是你会发现Flask还是单线程，在一个请求未返回时，其他请求也会阻塞，所以请添加这句
monkey.patch_all()

import os

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for,
    send_from_directory)

from flask import Flask

UPLOAD_PATH = os.path.join(os.path.dirname(__file__), 'static/upload')


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True, static_folder='static')
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import video
    app.register_blueprint(video.bp)

    @app.route('/')
    def index():
        return render_template("index.html")

    @app.route('/welcome')
    def welcome():
        return render_template("welcome.html")

    @app.route('/upload/<filename>', methods=['GET', 'POST'])
    def get_image(filename):
        return send_from_directory(UPLOAD_PATH, filename)

    return app


if __name__ == '__main__':
    app = create_app()
    http_server = WSGIServer(('127.0.0.1', int(5000)), app)
    http_server.serve_forever()
