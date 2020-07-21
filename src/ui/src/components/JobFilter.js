
import React from 'react';

import { ButtonGroup, ToggleButton } from 'react-bootstrap';


class JobFilter extends React.Component {
    constructor(props) {
      super(props);
      this.state = {
          search_text: '',
          starred: false,
          running: false,
          failed: false,
          finished: false
        };
  
      this.handleSearchChange = this.handleSearchChange.bind(this);
      this.handleStarred = this.handleStarred.bind(this);
      this.handleRunning = this.handleRunning.bind(this);
      this.handleFailed = this.handleFailed.bind(this);
      this.handleFinished = this.handleFinished.bind(this);
    }
  
    handleSearchChange(event) {
        var newState = {...this.state, search_text: event.target.value}
      this.setState(newState);
      this.props.onChange(newState)
    }

    handleStarred(event) {
        var newState = {...this.state, starred: event.target.checked}
      this.setState(newState);
      this.props.onChange(newState)
    }

    handleRunning(event) {
        var newState = {...this.state, running: event.target.checked}
      this.setState(newState);
      this.props.onChange(newState)
    }

    handleFailed(event) {
        var newState = {...this.state, failed: event.target.checked}
      this.setState(newState);
      this.props.onChange(newState)
    }

    handleFinished(event) {
        var newState = {...this.state, finished: event.target.checked}
      this.setState(newState);
      this.props.onChange(newState)
    }


    render() {
        return <div>
                <form className="form-inline mb-2">

                    <div className="input-group mr-sm-2">
                        <div className="input-group-prepend">
                            <div className="input-group-text">Search</div>
                        </div>
                        <input type="text" className="form-control" id="inlineFormInputGroupUsername2" placeholder="..."  value={this.state.search_text} onChange={this.handleSearchChange} />
                    </div>

                    <ButtonGroup toggle className="m-0 mr-1">
                        <ToggleButton
                            type="checkbox"
                            variant={this.state.running ? "info" : "outline-info"}
                            checked={this.state.running}
                            value="1"
                            onChange={this.handleRunning}
                        >
                        Running
                        </ToggleButton>
                        <ToggleButton
                            type="checkbox"
                            variant={this.state.failed ? "info" : "outline-info"}
                            checked={this.state.failed}
                            value="1"
                            onChange={this.handleFailed}
                        >
                        Failed
                        </ToggleButton>
                        <ToggleButton
                            type="checkbox"
                            variant={this.state.finished ? "info" : "outline-info"}
                            checked={this.state.finished}
                            value="1"
                            onChange={this.handleFinished}
                        >
                        Finished
                        </ToggleButton>
                    </ButtonGroup>

                    <ButtonGroup toggle className="mr-1">
                        <ToggleButton
                            type="checkbox"
                            variant={null}
                            checked={this.state.starred}
                            value="1"
                            onChange={this.handleStarred}
                        >
                        <i className="fa fa-star" aria-hidden="true" style={{color: (this.state.starred ? '#e3b707' : '#aaa')}} />
                        </ToggleButton>
                    </ButtonGroup>

                </form>

            </div>
    }
}

export default JobFilter;