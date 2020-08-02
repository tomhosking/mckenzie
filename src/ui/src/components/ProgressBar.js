
import React from 'react';


class ProgressBar extends React.Component {
    // constructor(props) {
    //     super(props);
    // }

    render() {
        return <div>
                <span className="badge" style={{'float': 'left', 'marginTop':'2px', 'width': '10%', 'textAlign': 'right'}}>{this.props.title}</span>
                <div className="progress m-0" style={{height: '20px', 'fontSize': '10px', 'fontWeight': 'bold'}}>
                    {/* + (this.props.progress < 100 ? ' progress-bar-animated' : '') */}
                        <div className={'p-1 progress-bar progress-bar-striped ' + ( this.props.progress < 100 ? 'bg-warning' : 'bg-success') } role="progressbar" style={{width: this.props.progress+'%'}}>{parseFloat(this.props.progress).toFixed(1)}%</div>
                    </div>
            </div>
    }
}

export default ProgressBar;