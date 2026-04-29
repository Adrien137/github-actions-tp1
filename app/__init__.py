from flask import Flask
from prometheus_flask_exporter import PrometheusMetrics

from .routes import api


def create_app():
    app = Flask(__name__)
    PrometheusMetrics(app)
    app.register_blueprint(api)
    return app
