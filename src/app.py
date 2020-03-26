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
            archived INTEGER,
            PRIMARY KEY (id, partition)
            )''')


        c.execute('''CREATE TABLE IF NOT EXISTS logs
            (job_id INTEGER,
            partition TEXT,
            msg TEXT,
            status TEXT,
            time TEXT,
            PRIMARY KEY (job_id, partition)
            )''')

        


def check_auth():
    return True

@app.route('/')
def home():
    
    # return render_template('index.htm')
    return render_template('index.html')



@app.route('/api/get_jobs')
def get_jobs():
    
    # db = TinyDB('./db/db.json')

    with SQLite() as db:

        ensure_table_exists()
    
        rows = db.execute('SELECT * FROM jobs').fetchall()
        return json.dumps({'job_list': [dict(row) for row in rows]})


@app.route('/api/delete_job/<partition>/<job_id>', methods=['GET'])
def delete_job(partition, job_id):

    # db = TinyDB('./db/db.json')
    
    with SQLite() as db:
        db.execute('DELETE FROM jobs WHERE id = ? AND partition = ?', (job_id, partition))
    update_proxy()
    return "Removed"

@app.route('/hooks/update_job/', methods=['POST'])
def update_job():
    

    # print(request.form)

    if not check_auth():
        return "Permission denied! Check your access token"

    if 'partition' not in request.form:
        print('Missing partition:')
        print(request.form)

    with SQLite() as db:
        jobid = request.form['jobid']
        partition = request.form['partition']
        if request.form.get('status', '') == "submitted":
            # app.table.insert({'status': 'submitted', 'id': request.form['jobid'], 'submit_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
            db.execute("INSERT INTO jobs (id, partition, status) VALUES (?,?,'submitted')", (jobid, partition))
        elif request.form.get('status', '') != '':
            query = "UPDATE jobs SET "
            params = []
            clauses = []

            if request.form.get('status', '') == "warmup":
                clauses.append(" node = ?")
                params.append(request.form['hostname'])

            if request.form.get('jobname', '') != '':
                clauses.append(" name = ?")
                params.append(request.form['jobname'])

            if request.form.get('status', '') != '':   
                clauses.append(" status = ?")
                params.append(request.form['status'])

            if request.form.get('progress', '') != '' and request.form.get('metric', '') != '':
                clauses.append(" score = ?, progress = ?")
                params.append(request.form['metric'])
                params.append(float(request.form['progress']))

            query += ", ".join(clauses)
            query += " WHERE id = ? and partition = ?"
            params.extend([jobid, partition])
            
            db.execute(query, params)

        if 'configfile' in request.files:
            f = request.files['configfile']
            os.makedirs(f'./db/job_data/{partition}_{jobid}')
            f.save(f'./db/job_data/{partition}_{jobid}/config.json')
            query = "UPDATE jobs SET has_config = 1 WHERE id = ? and partition = ?"
            db.execute(query, (jobid, partition))

        if 'outputfile' in request.files:
            f = request.files['outputfile']
            os.makedirs(f'./db/job_data/{partition}_{jobid}')
            f.save(f'./db/job_data/{partition}_{jobid}/output.txt')
            query = "UPDATE jobs SET has_output = 1 WHERE id = ? and partition = ?"
            db.execute(query, (jobid, partition))

        if 'resultsfile' in request.files:
            f = request.files['resultsfile']
            os.makedirs(f'./db/job_data/{partition}_{jobid}')
            f.save(f'./db/job_data/{partition}_{jobid}/metrics.json')
            query = "UPDATE jobs SET has_results = 1 WHERE id = ? and partition = ?"
            db.execute(query, (jobid, partition))
        
    update_proxy()
    return 'Updated job status!\n'

def update_proxy():
    """ Send summary of status to proxy responder """
    
    if 'MCKENZIE_PROXY' not in os.environ:
        return

    try:
        headers = {'Content-Type' : 'application/json'}

        with SQLite() as db:
            jobs = db.execute("SELECT * FROM jobs").fetchall()

            stat_obj = {
                # 'count_total': len(jobs),
                'count_waiting': len([1 for x in jobs if x['status'] == 'submitted']),
                'count_errors': len([1 for x in jobs if x['status'] == 'error']),
                'count_running': len([1 for x in jobs if x['status'] in ['running','warmup']]),
                'progress': [x['progress'] for x in jobs if x['status'] == 'running' and 'progress' in x]
            }

            r = requests.post(
                os.environ['MCKENZIE_PROXY'] + '/api/update',
                data=json.dumps(stat_obj),
                headers=headers)

            if r.status_code != 200 or r.text != 'ok':
                print(r.status_code, r.content)
        
    except Exception as e:
        print('Error updating proxy: ', e)


if __name__ == '__main__':

    # with TinyDB('./db/db.json', storage=CachingMiddleware(JSONStorage)) as db:
    #     app.table = db.table('jobs')


        

    #     with app.app_context():
    #         # app.run(host="0.0.0.0", port=5004, processes=1)

            
                

            
    #         update_proxy()

    update_proxy()
    app.run(debug=True,host='0.0.0.0', port=5002)
    