
import React from 'react';


class Dashboard extends React.Component {
    constructor(props) {
        super(props);

        this.state = { 
            status: {}
        };
        this.updateStatus = this.updateStatus.bind(this)
    }


    updateStatus(retrigger = true) {
        fetch('/api/get_summary')
        .then((response) => response.json())
        .then((data) => this.setState(
            {
                ...this.state,
                status: data
        })
        )
        .catch((err) => console.log(err))

        console.log(this.state)
        
        if(retrigger)
        {
            this.timeoutId = setTimeout(this.updateStatus, 10000)
        }
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
        return <div className="card-deck p-1 text-center">
                    <div className="card border-success">
                        <div className="card-header p-1">
                            <strong>Running</strong>
                        </div>
                        <div className="card-body p-1 text-success">
                            <h3>{this.state.status.count_running}</h3>
                        </div>
                    </div>
                    <div className="card border-warning">
                        <div className="card-header p-1">
                            <strong>Waiting</strong>
                        </div>
                        <div className="card-body p-1 text-warning">
                            <h3>{this.state.status.count_waiting}</h3>
                        </div>
                    </div>
                    <div className="card border-danger">
                        <div className="card-header p-1">
                            <strong>Errors</strong>
                        </div>
                        <div className="card-body p-1 text-danger">
                            <h3>{this.state.status.count_errors}</h3>
                        </div>
                    </div>
                </div>
    }
}

export default Dashboard;