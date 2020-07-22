from flask import Flask, render_template, request

import json, datetime, os

from tinydb import TinyDB, Query
from tinydb.storages import JSONStorage
from tinydb.middlewares import CachingMiddleware
import tinydb

from apscheduler.schedulers.background import BackgroundScheduler

import requests

from sqlite import SQLite

# app = Flask(__name__)

app = Flask(__name__, static_folder="ui/build/static", template_folder="ui/build")



def ensure_table_exists():

    with SQLite() as c:

        # Create table
        c.execute('''CREATE TABLE IF NOT EXISTS jobs
            (id INTEGER,
            partition TEXT,
            node TEXT,
            name TEXT,
            status TEXT,
            progress REAL,
            score TEXT,
            has_config INTEGER,
            has_output INTEGER,
            has_results INTEGER,
            archived INTEGER DEFAULT 0,
            starred INTEGER DEFAULT 0,
            PRIMARY KEY (id, partition)
            )''')


        c.execute('''CREATE TABLE IF NOT EXISTS logs
            (job_id INTEGER,
            partition TEXT,
            msg TEXT,
            status TEXT,
            time TEXT
            )''')

        


def check_auth():
    return True

@app.route('/', defaults={'url_path': ''})
@app.route('/<path:url_path>')
def home(url_path):
    
    # return render_template('index.htm')
    return render_template('index.html')



@app.route('/api/get_summary')
def get_summary():
    summ_obj = get_summary_obj()
    return json.dumps(summ_obj)

@app.route('/api/get_running')
def get_running():
    
    # db = TinyDB('./db/db.json')

    with SQLite() as db:

        ensure_table_exists()
    
        rows = db.execute('SELECT * FROM jobs WHERE archived = 0 or archived IS NULL').fetchall()
        return json.dumps({'job_list': [dict(row) for row in rows]})

@app.route('/api/get_history', methods=['POST'])
def get_history():
    
    # db = TinyDB('./db/db.json')

    with SQLite() as db:

        ensure_table_exists()

        print(request.json)

        query = 'SELECT * FROM jobs WHERE 1 {:} LIMIT 100'  #ORDER BY id DESC
        filter_query = ''

        if 'search_text' in request.json:
            filter_query += "AND name LIKE '%{:}%' ".format(request.json['search_text'])
        
        if request.json.get('starred', 0) == 1:
            filter_query += "AND starred = 1"
        if request.json.get('running', 0) == 1:
            filter_query += "AND (status = 'running' or status = 'warmup' or status = 'finalising')"
        if request.json.get('failed', 0) == 1:
            filter_query += "AND (status = 'error' OR status = 'timeout' or status = 'cancelled')"
        if request.json.get('finished', 0) == 1:
            filter_query += "AND status = 'complete'"
        
        query = query.format(filter_query)
        
    
        rows = db.execute(query).fetchall()
        return json.dumps({'job_list': [dict(row) for row in rows]})


@app.route('/api/archive_job/<partition>/<job_id>', methods=['GET'])
def archive_job(partition, job_id):

    # db = TinyDB('./db/db.json')
    
    with SQLite() as db:
        db.execute('UPDATE jobs SET archived = 1 WHERE id = ? AND partition = ?', (job_id, partition))
    update_proxy()
    return "Removed"

@app.route('/api/star_job/<partition>/<job_id>/<value>', methods=['GET'])
def star_job(partition, job_id, value):

    # db = TinyDB('./db/db.json')

    print(job_id, value)
    
    with SQLite() as db:
        db.execute('UPDATE jobs SET starred = ? WHERE id = ? AND partition = ?', (value, job_id, partition))
    update_proxy()
    return "Star flipped"

@app.route('/api/get_artifact/<type>/<partition>/<job_id>', methods=['GET'])
def get_artifact(type, partition, job_id):
    

    if type == 'config':
        file_path = f'./db/job_data/{partition}_{job_id}/config.json'
    elif type == 'metrics':
        file_path = f'./db/job_data/{partition}_{job_id}/metrics.json'
    elif type == 'output':
        file_path = f'./db/job_data/{partition}_{job_id}/output.txt'
    elif type == 'logs':
        return json.dumps([dict(row) for row in get_logs(partition, job_id)], indent=2)
    else:
        return "Unknown artifact type!"

    print(file_path)

    if not os.path.exists(file_path):
        return "File not found"

    with open(file_path) as f:
        content = f.read()
    return content

@app.route('/hooks/update_job/', methods=['POST'])
def update_job():
    

    # print(request.form)

    if not check_auth():
        return "Permission denied! Check your access token"

    if 'partition' not in request.form:
        print('Missing partition!')

    print(request.form)

    with SQLite() as db:
        jobid = request.form['jobid']
        partition = request.form['partition']
        if request.form.get('status', '') == "submitted":
            # app.table.insert({'status': 'submitted', 'id': request.form['jobid'], 'submit_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
            db.execute("INSERT INTO jobs (id, partition, status) VALUES (?,?,'submitted')", (jobid, partition))
        else:
            query = "UPDATE jobs SET "
            params = []
            clauses = []

            if request.form.get('status', '') == "warmup":
                clauses.append("node = ?")
                params.append(request.form['hostname'])

            if request.form.get('jobname', '') != '':
                clauses.append("name = ?")
                params.append(request.form['jobname'])

            if request.form.get('status', '') != '':   
                clauses.append("status = ?")
                params.append(request.form['status'])
                if request.form.get('status', '') == 'complete':
                    clauses.append("progress = ?")
                    params.append(100)

            if request.form.get('progress', '') != '' and request.form.get('metric', '') != '':
                clauses.append("score = ?, progress = ?")
                params.append(request.form['metric'])
                params.append(float(request.form['progress']))

            query += ", ".join(clauses)
            query += " WHERE id = ? and partition = ?"
            params.extend([jobid, partition])
            if len(clauses) > 0:
                db.execute(query, params)

        if 'configfile' in request.files:
            f = request.files['configfile']
            os.makedirs(f'./db/job_data/{partition}_{jobid}', exist_ok=True)
            f.save(f'./db/job_data/{partition}_{jobid}/config.json')
            query = "UPDATE jobs SET has_config = 1 WHERE id = ? and partition = ?"
            db.execute(query, (jobid, partition))

        if 'outputfile' in request.files:
            f = request.files['outputfile']
            os.makedirs(f'./db/job_data/{partition}_{jobid}', exist_ok=True)
            f.save(f'./db/job_data/{partition}_{jobid}/output.txt')
            query = "UPDATE jobs SET has_output = 1 WHERE id = ? and partition = ?"
            db.execute(query, (jobid, partition))

        if 'resultsfile' in request.files:
            f = request.files['resultsfile']
            os.makedirs(f'./db/job_data/{partition}_{jobid}', exist_ok=True)
            f.save(f'./db/job_data/{partition}_{jobid}/metrics.json')
            query = "UPDATE jobs SET has_results = 1 WHERE id = ? and partition = ?"
            db.execute(query, (jobid, partition))


        if request.form.get('status', '') != '':
            msg = '-'
            status = request.form.get('status', '')
            db.execute("INSERT INTO logs (job_id, partition, msg, status, time) VALUES (?, ?, ?, ?, strftime('%s','now'))", (jobid, partition, msg, status))
        
    update_proxy()
    return 'Updated job status!\n'

def get_logs(partition, job_id):
    with SQLite() as db:
        logs = db.execute("SELECT * FROM logs WHERE partition = ? AND job_id = ?", (partition, job_id)).fetchall()
        # logs = db.execute("SELECT * FROM logs").fetchall()
    print(len(logs))
    print([dict(row) for row in logs])
    return logs

def get_summary_obj():
    with SQLite() as db:
        jobs = db.execute("SELECT * FROM jobs WHERE archived = 0 or archived IS NULL").fetchall()

        stat_obj = {
            # 'count_total': len(jobs),
            'count_waiting': len([1 for x in jobs if x['status'] == 'submitted']),
            'count_errors': len([1 for x in jobs if x['status'] == 'error']),
            'count_running': len([1 for x in jobs if x['status'] in ['running','warmup']]),
            'progress': [x['progress'] for x in jobs if x['status'] == 'running' and 'progress' in x.keys()]
        }
    return stat_obj

def update_proxy():
    """ Send summary of status to proxy responder """
    
    if 'MCKENZIE_PROXY' not in os.environ:
        return

    try:
        headers = {'Content-Type' : 'application/json'}

        stat_obj = get_summary_obj()

        r = requests.post(
            os.environ['MCKENZIE_PROXY'] + '/api/update',
            data=json.dumps(stat_obj),
            headers=headers)

        if r.status_code != 200 or r.text != 'ok':
            print(r.status_code, r.content)
        
    except Exception as e:
        print('Error updating proxy: ', e)


if __name__ == '__main__':

    update_proxy()
    app.run(debug=True,host='0.0.0.0', port=5002, processes=1)
    