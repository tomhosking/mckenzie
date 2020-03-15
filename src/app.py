from flask import Flask, render_template, request

import json, datetime, os

from tinydb import TinyDB, Query
from tinydb.storages import JSONStorage
from tinydb.middlewares import CachingMiddleware
import tinydb

from apscheduler.schedulers.background import BackgroundScheduler

import requests


app = Flask(__name__)


def check_auth():
    return True

@app.route('/')
def home():
    
    return render_template('index.htm')



@app.route('/api/get_jobs')
def get_jobs():
    
    # db = TinyDB('./db/db.json')
    
    rows = app.table.all()
    return json.dumps({'job_list': rows})


@app.route('/api/delete_job/<job_id>', methods=['GET'])
def delete_job(job_id):

    # db = TinyDB('./db/db.json')
    

    app.table.remove(Query().id == job_id)

    return "Removed"

@app.route('/hooks/update_job/', methods=['POST'])
def update_job():
    

    # print(request.form)

    if not check_auth():
        return "Permission denied! Check your access token"

    if request.form.get('status', '') == "submitted":
        app.table.insert({'status': 'submitted', 'id': request.form['jobid'], 'submit_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
    else:
        # TODO: This is a disgrace
        time = {}
        node = {}
        msg = {}
        jobname = {}
        status = {}
        inplay = {}
        if request.form.get('status', '') == "warmup":
            node = {'partition': request.form['partition'], 'hostname': request.form['hostname']}
            time = {'warmup_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        if request.form.get('msg', '') == "running":
            node = {'partition': request.form['partition'], 'hostname': request.form['hostname']}
            time = {'running_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        if request.form.get('msg', '') == "complete" or request.form.get('msg', '') or request.form.get('msg', '') == "timeout":
            time = {'complete_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        if request.form.get('msg', '') != '':
            msg = {'msg': request.form['msg']}
        if request.form.get('jobname', '') != '':
            jobname = {'jobname': request.form['jobname']}
        if request.form.get('status', '') != '':   
            status = {'status': request.form['status']}
        if request.form.get('progress', '') != '' and request.form.get('metric', '') != '':
            inplay = {'metric': request.form['metric'], 'progress': request.form['progress']}

        app.table.update({**node, **status, **time, **msg, **jobname, **inplay}, Query().id == request.form['jobid'])
    return 'Updated job status!\n'


if __name__ == '__main__':

    with TinyDB('./db/db.json', storage=CachingMiddleware(JSONStorage)) as db:
        app.table = db.table('jobs')


        def update_proxy():
            """ Send summary of status to proxy responder """

            try:
                headers = {'Content-Type' : 'application/json'}

                jobs = db.table('jobs').all()

                stat_obj = {
                    'count_total': len(jobs),
                    'count_waiting': len([1 for x in jobs if x['status'] == 'submitted']),
                    'count_errors': len([1 for x in jobs if x['status'] == 'error']),
                    'count_running': len([1 for x in jobs if x['status'] == 'running']),
                    'running_progress': [x['progress'] for x in jobs if x['status'] == 'running']
                }

                r = requests.post(
                    os.environ['MCKENZIE_PROXY'] + '/api/update',
                    data=json.dumps(stat_obj),
                    headers=headers)
                
            except Exception as e:
                print('Error updating proxy: ', e)
            

        if 'MCKENZIE_PROXY' in os.environ:
            sched = BackgroundScheduler(daemon=True)
            sched.add_job(update_proxy,'interval',minutes=5)
            sched.start()
            update_proxy()

        with app.app_context():
            # app.run(host="0.0.0.0", port=5004, processes=1)
            app.run(debug=True,host='0.0.0.0', port=5002)

        if 'MCKENZIE_PROXY' in os.environ:
            sched.shutdown()
    