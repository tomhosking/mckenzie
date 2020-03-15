from flask import Flask, render_template, request

import json, datetime

from tinydb import TinyDB, Query
from tinydb.storages import JSONStorage
from tinydb.middlewares import CachingMiddleware
import tinydb

app = Flask(__name__)


@app.route('/')
def home():
    
    return "Mckenzie Proxy is running"