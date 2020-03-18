from flask import Flask, render_template, request

import json, datetime, os

from tinydb import TinyDB, Query
from tinydb.storages import JSONStorage
from tinydb.middlewares import CachingMiddleware
import tinydb

from apscheduler.schedulers.background import BackgroundScheduler

import requests


# app = Flask(__name__)

app = Flask(__name__, static_folder="ui/build/static", template_folder="ui/build")



def check_auth():
    return True

@app.route('/')
def home():
    
    # return render_template('index.htm')
    return render_template('index.html')



@app.route('/api/get_jobs')
def get_jobs():
    
    # db = TinyDB('./db/db.json')
    
    rows = app.table.all()
    return json.dumps({'job_list': rows})


@app.route('/api/delete_job/<job_id>', methods=['GET'])
def delete_job(job_id):

    # db = TinyDB('./db/db.json')
    

    app.table.remove(Query().id == job_id)
    update_proxy()
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
    update_proxy()
    return 'Updated job status!\n'


if __name__ == '__main__':

    with TinyDB('./db/db.json', storage=CachingMiddleware(JSONStorage)) as db:
        app.table = db.table('jobs')


        

        with app.app_context():
            # app.run(host="0.0.0.0", port=5004, processes=1)

            def update_proxy():
                """ Send summary of status to proxy responder """
                
                if 'MCKENZIE_PROXY' not in os.environ:
                    return

                try:
                    headers = {'Content-Type' : 'application/json'}

                    jobs = app.table('jobs').all()

                    stat_obj = {
                        'count_total': len(jobs),
                        'count_waiting': len([1 for x in jobs if x['status'] == 'submitted']),
                        'count_errors': len([1 for x in jobs if x['status'] == 'error']),
                        'count_running': len([1 for x in jobs if x['status'] in ['running','warmup']]),
                        'running_progress': [x['progress'] for x in jobs if x['status'] == 'running' and 'progress' in x]
                    }

                    r = requests.post(
                        os.environ['MCKENZIE_PROXY'] + '/api/update',
                        data=json.dumps(stat_obj),
                        headers=headers)
                    
                except Exception as e:
                    print('Error updating proxy: ', e)
                

            
            update_proxy()


            app.run(debug=False,host='0.0.0.0', port=5002)
    