from flask import Flask, render_template, request

import json, datetime, os

from tinydb import TinyDB, Query
from tinydb.storages import JSONStorage
from tinydb.middlewares import CachingMiddleware
import tinydb

app = Flask(__name__)


@app.route('/')
def home():
    
    return "Mckenzie Proxy is running"

@app.route('/api/update', methods=['POST'])
def update():
    
    try:
        os.makedirs('./db', exist_ok=True)
        with TinyDB('./db/db.json', storage=JSONStorage) as db:
            table = db.table('status')

            stat_objs = table.search(Query().type == 'status')
            if len(stat_objs) < 1:
                table.insert({'type': 'status'})

            new_status = {
                'updated': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                **request.get_json()
            }

            table.update(new_status, Query().type == 'status')

            stat_objs = table.search(Query().type == 'status')
            return json.dumps(stat_objs)

    except Exception as e:
        return str(e)

    # finally:
    #     return "OK"

@app.route('/api/ip_responder')
def update():
    
    try:
        os.makedirs('./db', exist_ok=True)

        node_id = request.args.get('node')
        ip = request.args.get('ip', None)

        with TinyDB('./db/db.json', storage=JSONStorage) as db:
            table = db.table('ip')

            if ip is not None:
                stat_objs = table.search(Query().id == node_id)
                if len(stat_objs) < 1:
                    table.insert({'id': node_id, 'ip': ip})
                else:
                
                    table.update({'ip': ip}, Query().id == node_id)

            stat_objs = table.search(Query().ip == node_id)
            return json.dumps(stat_objs)

    except Exception as e:
        return str(e)


@app.route('/api/get')
def get():
    try:
        os.makedirs('./db', exist_ok=True)
        with TinyDB('./db/db.json', storage=JSONStorage) as db:
            table = db.table('status')

            stat_objs = table.search(Query().type == 'status')

            if len(stat_objs) < 1:
                table.insert({'type': 'status'})

            stat_obj = table.search(Query().type == 'status')[0]

            return json.dumps(stat_obj)

    except Exception as e:
        return str(e)