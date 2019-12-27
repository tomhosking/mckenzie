from flask import Flask, render_template, request

import json, datetime

from tinydb import TinyDB, Query


app = Flask(__name__)

@app.route('/')
def home():
    
    return render_template('index.htm')



@app.route('/api/get_jobs')
def get_jobs():
    
    db = TinyDB('./db/db.json')
    table = db.table('jobs')
    rows = table.all()
    return json.dumps({'job_list': rows})


@app.route('/hooks/update_job/', methods=['POST'])
def update_job():
    db = TinyDB('./db/db.json')
    table = db.table('jobs')

    print(request.form)

    if request.form.get('status', '') == "submitted":
        table.insert({'status': 'submitted', 'id': request.form['jobid'], 'submit_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
    else:
        # TODO: This is a disgrace
        time = {}
        node = {}
        msg = {}
        jobname = {}
        status = {}
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

        table.update({**node, **status, **time, **msg, **jobname}, Query().id == request.form['jobid'])
    return 'Updated job status!\n'


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=5002)