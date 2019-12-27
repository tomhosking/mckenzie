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
                        <th scope="col">Submitted</th>
                        <th scope="col">Status</th>
                        <th scope="col">Output</th>
                        </tr>
                    </thead>
                    <tbody>
                        {
                            this.state.job_list.map( (job) => (
                            
                                <tr key={job.id}>
                                    <th scope="row" style={{textAlign: 'center'}}>{job.id}</th>
                                    <td>{job.partition}</td>
                                    <td>{job.hostname}</td>
                                    <td>{job.submit_time}</td>
                                    <td>{job.status}</td>
                                    <td>{job.msg}</td>
                                </tr>
                             ) )
                        }
                    </tbody>
                </table>
            </div>
  }
}





const domContainer = document.querySelector('#react_root');


ReactDOM.render(e(App), domContainer);