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

@app.route('/api/update')
def update():
    
    try:
        with TinyDB('./db/db.json', storage=CachingMiddleware(JSONStorage)) as db:
            table = db.table('status')

            stat_objs = table.search(Query().type == 'status')
            if len(stat_objs) < 1:
                table.insert({'type': 'status'})

            new_status = {
                'updated': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            table.update(new_status, Query().type == 'status')

    except Exception as e:
        return str(e)

    finally:
        return "OK"




@app.route('/api/get')
def get():
    try:
        with TinyDB('./db/db.json', storage=CachingMiddleware(JSONStorage)) as db:
            table = db.table('status')

            stat_objs = table.search(Query().type == 'status')

            if len(stat_objs) < 1:
                table.insert({'type': 'status'})

            stat_obj = table.search(Query().type == 'status')[0]

            return json.dumps(stat_obj)

    except Exception as e:
        return str(e)