import React from 'react';
import ProgressBar from './ProgressBar';

import { FaPlayCircle } from 'react-icons/fa';

class JobList extends React.Component {
    constructor(props) {
      super(props);
      this.state = { 
          job_list: []
      };
      this.updateStatus = this.updateStatus.bind(this)
    }


  updateStatus(retrigger = true) {
        fetch('/api/get_running')
        .then((response) => response.json())
        .then((data) => this.setState(
            {
                ...this.state,
                job_list: data['job_list']
        })
        )
        .catch((err) => console.log(err))
        
        if(retrigger)
        {
            this.timeoutId = setTimeout(this.updateStatus, 10000)
        }
    }

    archiveJob(partition, jobid)
    {
        fetch('/api/archive_job/'+partition+'/'+jobid)
        .then((response) => this.updateStatus(false))
    }

    starJob(partition, jobid, value)
    {
        fetch('/api/star_job/'+partition+'/'+jobid + '/' + value)
        .then((response) => this.updateStatus(false))
    }

    componentDidMount()
    {
        this.updateStatus()
    }
    componentWillUnmount()
    {
        clearTimeout(this.timeoutId)
    }


    render() {
        return <div>
                
                <table class="table table-striped table-sm table-hover small">
                    <thead>
                        <tr>
                            <th scope="col">&nbsp;</th>
                            <th scope="col" style={{textAlign: 'center'}}>
                                &nbsp;
                            </th>
                            <th scope="col">Name</th>
                            {/* <th scope="col">Submitted</th> */}
                            <th scope="col">Status</th>
                            <th scope="col">Score</th>
                            <th scope="col">Progress</th>
                            {/* <th scope="col">Output</th> */}
                            <th scope="col">&nbsp;</th>
                        </tr>
                    </thead>
                    <tbody>
                        {
                            
                            
                            this.state.job_list.map( (job) => {
                                
                                var statusIcon;
                                if (job.status === 'running')
                                {
                                    // statusIcon = <div class="loader">Running</div>
                                    statusIcon = <FaPlayCircle style={{color: "#C0D14F"}} />
                                }
                                else if (job.status === 'submitted')
                                {
                                    statusIcon = <span class="fa fa-clock-o" aria-hidden="true" style={{color: "#C0D14F"}}></span>
                                }
                                else if (job.status === 'warmup')
                                {
                                    statusIcon = <span class="fa fa-flash" aria-hidden="true" style={{color: "#C0D14F"}}></span>
                                }
                                else if (job.status === 'error')
                                {
                                    statusIcon = <span class="fa fa-warning" aria-hidden="true" style={{color: "#CF4062"}}></span>
                                }
                                else if (job.status === 'timeout')
                                {
                                    statusIcon = <i className="fa fa-hourglass-end" aria-hidden="true" style={{color: "#EE74EF"}}></i>
                                }
                                else if (job.status === 'cancelled')
                                {
                                    statusIcon = <i className="fa fa-ban" aria-hidden="true" style={{color: "#490E7D"}}></i>
                                }
                                else if (job.status === 'complete')
                                {
                                    statusIcon = <i className="fa fa-check" aria-hidden="true" style={{color: "#C0D14F"}}></i>
                                }
                                else if (job.status === 'validating')
                                {
                                    statusIcon = <i className="fa fa-tachometer" aria-hidden="true" style={{color: "#C0D14F"}}></i>
                                }
                                else if (job.status === 'finalising')
                                {
                                    statusIcon = <i className="fa fa-upload" aria-hidden="true" style={{color: "#C0D14F"}}></i>
                                }
                                else
                                {
                                    statusIcon = <span>{job.status}</span>
                                }
                                return (
                            
                                <tr key={job.id}>
                                    <td>
                                        <button onClick={() => (this.starJob(job.partition, job.id, (job.starred ? 0 : 1)))} className="btn p-0 m-0 mr-1">
                                            <i className="fa fa-star" aria-hidden="true" style={{color: (job.starred ? '#e3b707' : '#aaa')}} />
                                        </button>
                                    </td>
                                    <th scope="row" style={{textAlign: 'center'}}><small>{job.id} @ {job.partition}::{job.node}</small></th>
                                    <td>{job.name}</td>
                                    {/* <td>{job.submit_time}</td> */}
                                    <td>{statusIcon}</td>
                                    <td>{job.score}</td>
                                    <td>{job.progress != null ? <ProgressBar progress={job.progress} /> : ''}</td>
                                    {/* <td>{job.msg}</td> */}
                                    <td>
                                        <button onClick={() => (this.archiveJob(job.partition, job.id))} className="btn p-0 m-0 mr-1"><i className="fa fa-times-circle" aria-hidden="true" style={{color: "red"}}></i></button>
                                        
                                    </td>
                                </tr>
                            )} )
                        }
                    </tbody>
                </table>
            </div>
    }
}


export default JobList;