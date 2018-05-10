# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import flask
import importlib
import json
import logging
import os
import sys

from dash.dependencies import Input, Output
from flask import Flask

from metaswitch_tinder.config_model import MetaswitchTinder
from metaswitch_tinder.layout import create_app_layout

log = logging.getLogger(__name__)


def configure_logging():
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    ch = logging.StreamHandler(sys.stderr)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)


def load_config_from_file() -> MetaswitchTinder:
    if len(sys.argv) > 1:
        # Strip the .py extension
        config_file = os.path.splitext(sys.argv[1])[0]
        config_module = importlib.import_module(config_file)
        config_dict = config_module.config
    else:
        config_dict = {}

    cfg = MetaswitchTinder(config_dict, partial=False)
    cfg.validate()
    return cfg


def load_config_from_env() -> MetaswitchTinder:
    cfg = MetaswitchTinder(json.loads(os.environ['ALL_CONFIG']), partial=False)
    cfg.validate()
    return cfg


try:
    config = load_config_from_env()
except KeyError:
    config = load_config_from_file()

server = Flask(__name__)
server.secret_key = os.environ.get('secret_key', 'secret')

app = dash.Dash(name=__name__, server=server)
app.layout = create_app_layout(config)

app.css.append_css({"external_url": config.css_cdn})


if __name__ == "__main__":
    configure_logging()
    app.run_server(threaded=True, port=int(os.environ.get('PORT', 80)), debug=True)
