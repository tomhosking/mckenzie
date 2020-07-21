
import React from 'react';

import JobFilter from './JobFilter';

import Modal from 'react-bootstrap/Modal'


class JobHistory extends React.Component {
    constructor(props) {
        super(props);
        this.state = { 
            job_list: [],
            filter: {},
            modalContent: '',
            modalType: null,
            modalShow: false
        };
        this.updateStatus = this.updateStatus.bind(this)
        this.filterChange = this.filterChange.bind(this)
        this.getArtifact = this.getArtifact.bind(this)
        this.handleClose = this.handleClose.bind(this)
        this.starJob = this.starJob.bind(this)
      }
  
  
    updateStatus(filterState = null) {
        filterState = filterState == null ? this.state : filterState;
          fetch('/api/get_history',
            {
                method: 'POST',
                body: JSON.stringify(filterState.filter),
                headers: {
                    'Content-Type': 'application/json'
                }
            }
            )
          .then((response) => response.json())
          .then((data) => this.setState(
              {
                  ...this.state,
                  job_list: data['job_list']
              })
          )
          .catch((err) => console.log(err))
      }

    filterChange(filterState) {
        var newState = {filter: filterState};
        this.setState(newState);
        this.updateStatus(newState);
    }

    getArtifact(type, partition,  jobid) {
        fetch('/api/get_artifact/'+type+'/'+partition +'/'+jobid)
          .then((response) => response.text())
          .then((data) => this.setState({modalContent: data, modalShow: true, modalType: type}))
          .catch((err) => console.log(err))
    }

    starJob(partition, jobid, value)
    {
        fetch('/api/star_job/'+partition+'/'+jobid + '/' + value)
        .then((response) => this.updateStatus())
    }
      
  
      componentDidMount()
      {
          this.updateStatus();
      }

      handleClose() {
          this.setState({modalShow: false});
      }

      render() {
        return <div>

                <JobFilter onChange={this.filterChange} />
                
                <table className="table table-striped table-sm table-hover small">
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
                        <th scope="col">&nbsp;</th>
                        </tr>
                    </thead>
                    <tbody>
                        {
                            
                            
                            this.state.job_list.map( (job) => {
                                
                                var statusIcon;
                                if (job.status === 'running')
                                {
                                    statusIcon = <div className="loader">Running</div>
                                }
                                else if (job.status === 'submitted')
                                {
                                    statusIcon = <span className="fa fa-clock-o" aria-hidden="true" style={{color: "#C0D14F"}}></span>
                                }
                                else if (job.status === 'warmup')
                                {
                                    statusIcon = <span className="fa fa-flash" aria-hidden="true" style={{color: "#C0D14F"}}></span>
                                }
                                else if (job.status === 'error')
                                {
                                    statusIcon = <span className="fa fa-warning" aria-hidden="true" style={{color: "#CF4062"}}></span>
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
                                    <td style={{textAlign: 'center'}}><small>{job.id} @ {job.partition}::{job.node}</small></td>
                                    <td>{job.name}</td>
                                    {/* <td>{job.submit_time}</td> */}
                                    <td>{statusIcon}</td>
                                    <td>{job.score}</td>
                                    <td>
                                        <button type="button" className="btn btn-sm btn-outline-secondary px-1 py-0 mr-1" onClick={() => (this.getArtifact('config', job.partition, job.id))}><i className="fa fa-cogs" aria-hidden="true" /></button>
                                        <button type="button" className="btn btn-sm btn-outline-secondary px-1 py-0 mr-1" onClick={() => (this.getArtifact('metrics', job.partition, job.id))}><i className="fa fa-line-chart" aria-hidden="true" /></button>
                                        <button type="button" className="btn btn-sm btn-outline-secondary px-1 py-0 mr-1" onClick={() => (this.getArtifact('output', job.partition, job.id))}><i className="fa fa-comments" aria-hidden="true" /></button>
                                        <button type="button" className="btn btn-sm btn-outline-secondary px-1 py-0 mr-1" onClick={() => (this.getArtifact('logs', job.partition, job.id))}><i className="fa fa-clock-o" aria-hidden="true" /></button>
                                    </td>
                                </tr>
                            )} )
                        }
                    </tbody>
                </table>

                
                <Modal show={this.state.modalShow} onHide={this.handleClose}>
                <Modal.Header closeButton>
                    <Modal.Title>
                        {this.state.modalType === 'config' && 'Config'}
                        {this.state.modalType === 'metrics' && 'Metrics'}
                        {this.state.modalType === 'output' && 'Output'}
                        {this.state.modalType === 'logs' && 'Logs'}
                    </Modal.Title>
                </Modal.Header>
                <Modal.Body><pre>{this.state.modalContent}</pre></Modal.Body>
                <Modal.Footer>
                </Modal.Footer>
            </Modal>
            </div>
    }
}

export default JobHistory;