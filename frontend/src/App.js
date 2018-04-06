import React, { Component } from 'react';
import axios from 'axios';
import logo from './logo.svg';
import './App.css';

class App extends Component {
  constructor() {
    super();
    this.state = { identity: "loading" };
  }

  componentDidMount() {
    axios.get('/api/identity')
      .then(response => {
        this.setState({
          identity: response.data
        });
      })
      .catch(error => {
        console.error(error);
      });
  }

  render() {
    const { identity } = this.state;
    return (
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h1 className="App-title">D-Vault</h1>
        </header>
        <p className="App-intro">
          { identity }
        </p>
      </div>
    );
  }
}

export default App;
