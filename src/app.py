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

    if request.form['status'] == "submitted":
        table.insert({'status': 'submitted', 'id': request.form['jobid'], 'submit_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
    else:
        time = {}
        node = {}
        msg = {}
        if request.form['status'] == "warmup":
            time = {'warmup_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        if request.form['status'] == "running":
            node = {'partition': request.form['partition'], 'hostname': request.form['hostname']}
            time = {'running_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        if request.form['status'] == "complete" or request.form['status'] == "error" or request.form['status'] == "timeout":
            time = {'complete_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        if request.form.get('msg', '') != '':
            msg = {'msg': request.form['msg']}

        table.update({**node, 'status': request.form['status'], **time, **msg}, Query().id == request.form['jobid'])
    return 'Updated job status!\n'


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=5002)