'use strict';

const e = React.createElement;



class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = { 
        job_list: []
    };
    this.updateStatus = this.updateStatus.bind(this)
  }


  updateStatus() {
      fetch('/api/get_jobs')
      .then((response) => response.json())
      .then((data) => this.setState(
          {
              ...this.state,
              job_list: data['job_list']
        })
        )
      .catch((err) => console.log(err))

      console.log(this.state)
      

      setTimeout(this.updateStatus, 10000)
  }

  componentDidMount()
  {
      this.updateStatus()
  }


  render() {
    return <div className="container p-2">
                
                <table class="table">
                    <thead>
                        <tr>
                        <th scope="col" style={{textAlign: 'center'}}>
                            <a onClick={window.openPopup}>
                                <img src="./static/slurms.png" style={{width: "32px", height: "32px"}} />
                            </a>
                        </th>
                        <th scope="col">Partition</th>
                        <th scope="col">Node</th>
                        <th scope="col">Name</th>
                        <th scope="col">Submitted</th>
                        <th scope="col">Status</th>
                        <th scope="col">Output</th>
                        </tr>
                    </thead>
                    <tbody>
                        {
                            
                            status = 
                            this.state.job_list.map( (job) => {
                                console.log(job.status);
                                var statusIcon;
                                if (job.status == 'running')
                                {
                                    statusIcon = <div class="loader">Running</div>
                                }
                                else if (job.status == 'submitted')
                                {
                                    statusIcon = <span class="fa fa-clock-o" aria-hidden="true" style={{color: "#C0D14F"}}></span>
                                }
                                else if (job.status == 'warmup')
                                {
                                    statusIcon = <span class="fa fa-flash" aria-hidden="true" style={{color: "#C0D14F"}}></span>
                                }
                                else if (job.status == 'error')
                                {
                                    statusIcon = <span class="fa fa-warning" aria-hidden="true" style={{color: "#CF4062"}}></span>
                                }
                                else if (job.status == 'timeout')
                                {
                                    statusIcon = <i className="fa fa-hourglass-end" aria-hidden="true" style={{color: "#EE74EF"}}></i>
                                }
                                else if (job.status == 'cancelled')
                                {
                                    statusIcon = <i className="fa fa-ban" aria-hidden="true" style={{color: "#490E7D"}}></i>
                                }
                                else if (job.status == 'complete')
                                {
                                    statusIcon = <i className="fa fa-check" aria-hidden="true" style={{color: "#C0D14F"}}></i>
                                }
                                else
                                {
                                    statusIcon = <span>{job.status}</span>
                                }
                                return (
                            
                                <tr key={job.id}>
                                    <th scope="row" style={{textAlign: 'center'}}>{job.id}</th>
                                    <td>{job.partition}</td>
                                    <td>{job.hostname}</td>
                                    <td>{job.jobname}</td>
                                    <td>{job.submit_time}</td>
                                    <td>{statusIcon}</td>
                                    <td>{job.msg}</td>
                                </tr>
                             )} )
                        }
                    </tbody>
                </table>
            </div>
  }
}





const domContainer = document.querySelector('#react_root');


ReactDOM.render(e(App), domContainer);