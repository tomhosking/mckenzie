from flask import Flask, render_template, request

import json, datetime, os

from tinydb import TinyDB, Query
from tinydb.storages import JSONStorage
from tinydb.middlewares import CachingMiddleware
import tinydb

app = Flask(__name__)

import sqlite3


class SQLite():
    def __init__(self, file='./db/mckenzie_proxy.sqlite'):
        self.file=file
    def __enter__(self):
        self.conn = sqlite3.connect(self.file)
        self.conn.row_factory = sqlite3.Row
        return self.conn.cursor()
    def __exit__(self, type, value, traceback):
        self.conn.commit()
        self.conn.close()

def ensure_table_exists():

    with SQLite() as c:

        # Create table
        c.execute('''CREATE TABLE IF NOT EXISTS status
             (id INTEGER PRIMARY KEY, last_updated TEXT, count_waiting INTEGER, count_running INTEGER, count_errors INTEGER, progress TEXT)''')

        c.execute('''CREATE TABLE IF NOT EXISTS ips
             (id text PRIMARY KEY, last_updated TEXT, ip TEXT)''')


@app.route('/')
def home():
    
    return "Mckenzie Proxy is running"

@app.route('/api/update', methods=['POST'])
def update():
    
    try:
        # os.makedirs('./db', exist_ok=True)
        with SQLite() as db:
            # table = db.table('status')

            # c = conn.cursor()

            ensure_table_exists()

            update_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            status = request.get_json()
            db.execute(
                "INSERT OR REPLACE INTO status (id, last_updated, count_waiting, count_running, count_errors, progress) VALUES (1,?,?,?,?,?)",
                 (update_time, status['count_waiting'], status['count_running'], status['count_errors'], json.dumps(status['progress'])))

            return 'ok'

    except Exception as e:
        return str(e)

    # finally:
    #     return "OK"

@app.route('/api/ip_responder')
def ip_responder():
    
    try:
        # os.makedirs('./db', exist_ok=True)

        node_id = request.args.get('node')
        ip = request.args.get('ip', None)

        ensure_table_exists()

        with SQLite() as db:
            

            if ip is not None:
                update_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                db.execute('INSERT OR REPLACE INTO ips (id, ip, last_updated) VALUES (?,?,?)', (node_id,ip, update_time))
                

            stat_obj = db.execute('SELECT * FROM ips WHERE id = ?', (node_id,)).fetchone()
            if stat_obj is not None:
                return json.dumps(dict(stat_obj))
            else:
                return json.dumps({})

    except Exception as e:
        raise e
        return str(e)


@app.route('/api/get')
def get():
    try:
        # os.makedirs('./db', exist_ok=True)
        with SQLite() as db:

            ensure_table_exists()
            # table = db.table('status')

            # stat_objs = table.search(Query().type == 'status')
            stat_objs = db.execute('SELECT * FROM status').fetchall()
            if len(stat_objs) > 0:
                status = dict(stat_objs[0])
                status['progress'] = json.loads(status['progress'])
                return json.dumps()
            else:
                return json.dumps({})

    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0', port=5004)