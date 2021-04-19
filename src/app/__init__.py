import json
from flask import Flask
from src.app.VcfParser import VcfParser
from src import __VCF_FILE__, __SCHEMA__


def create_app():
    """Initialize the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('src.config.DevConfig')
    app.register_blueprint(error_handlers.blueprint)

    return app


