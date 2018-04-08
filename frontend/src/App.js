import React, { Component } from 'react';
import { BrowserRouter, Route } from 'react-router-dom'

import PiDashboard from './PiDashboard';
import AggregatorDashboard from './AggregatorDashboard';

class App extends Component {
  render() {
    return (
      <BrowserRouter>
        <div>
          <Route path="/pi" component={PiDashboard}/>
          <Route path="/aggregator" component={AggregatorDashboard}/>
        </div>
      </BrowserRouter>
    );
  }
}

export default App;
