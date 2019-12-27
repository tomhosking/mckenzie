from flask import Flask, render_template, request

import json

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


@app.route('/hooks/create_job/', methods=['POST'])
def create_job():
    db = TinyDB('./db/db.json')
    table = db.table('jobs')

    print(request.form)

    # table.update({'partition': 'PGR-Fake', 'hostname': 'damnii69', 'status': 'waiting', 'submit_date': '10 mins ago', 'msg':''}, Query().id == 0)
    # table.update({'partition': 'PGR-Fake', 'hostname': request.args['hostname'], 'status': 'waiting', 'submit_date': '10 mins ago', 'msg': request.args['msg']}, Query().id == 0)
    return 'Registered job! Missing all the details though'


@app.route('/hooks/update_job/', methods=['POST'])
def update_job():
    return 'Updated job status! Missing all the details though'


@app.route('/hooks/finalise_job/', methods=['POST'])
def finalise_job():
    return 'Updated job status! Missing all the details though'


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=5002)