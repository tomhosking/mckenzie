import React from 'react';
import logo from './slurms.png';
import './App.css';
import JobList from './components/JobList';
import { FaList, FaHistory, FaTachometerAlt, FaQuestion } from 'react-icons/fa';
import {
    BrowserRouter as Router,
    Switch,
    Route,
    Link,
    NavLink,
    Redirect
  } from "react-router-dom";
import Dashboard from './components/Dashboard';
import JobHistory from './components/JobHistory';
import HelpPage from './components/Help';

class App extends React.Component {
  constructor(props) {
    super(props);
  }


  render() {
    return <Router>
            <nav className="navbar navbar-expand-lg navbar-light bg-light py-0">
                <a className="navbar-brand" onClick={window.openPopup}>
                    <img src={logo} style={{width: "32px", height: "32px"}} />
                </a>
                <div className="navbar-nav nav mr-auto">
                    <NavLink activeClassName='active' className="nav-item nav-link mx-2" to="/dashboard"><FaTachometerAlt /></NavLink>
                    <NavLink activeClassName='active' className="nav-item nav-link mx-2" to="/list"><FaList /></NavLink>
                    <NavLink activeClassName='active' className="nav-item nav-link mx-2" to="/history"><FaHistory /></NavLink>
                </div>
                <div className="navbar-nav nav">
                    <NavLink activeClassName='active' className="nav-item nav-link mx-2" to="/help"><FaQuestion /></NavLink>
                    
                </div>
            </nav>  
                    
            <div className="container p-2">
                <Switch>
                    <Route path="/" exact>
                        <Redirect to="/dashboard" />
                    </Route>
                    <Route path="/dashboard">
                        <Dashboard />
                    </Route>
                    <Route path="/list">
                        <JobList />
                    </Route>
                    <Route path="/history">
                        <JobHistory />
                    </Route>
                    <Route path="/help">
                        <HelpPage />
                    </Route>
                </Switch>   
            </div>
        </Router>
  }
}

export default App;
