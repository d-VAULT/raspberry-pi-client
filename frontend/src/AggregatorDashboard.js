import React, { Component } from 'react';
import axios from 'axios';

class AggregatorDashboard extends Component {
  constructor() {
    super();
    this.state = {};
  }

  componentDidMount() {
    if (!this.state.pollTimerId) {
      this.startPolling();
    }
  }

  startPolling() {
    const pollTimerId = setInterval(this.poll, 1000, this);
    this.setState({ pollTimerId });
  }

  stopPolling() {
    if (this.state.pollTimerId) {
      clearInterval(this.state.pollTimerId);
      this.setState({ pollTimerId: undefined });
    }
  }

  poll(self) {
    axios
      .get('/api/aggregated-data')
      .then(response => response.data)
      .then(data => {
        self.setState({
          data
        })
      })
  }

  render() {
    const { data } = this.state;
    return (
      <div className="App">
        <div id="a-wrap" style={{ 'marginRight': 'auto', 'marginLeft':'auto', 'width':'1920px', 'padding': '20px', 'height':'1080px', 'backgroundColor': '#6699ff'}}>
      		<div id="title">
      		  Grid insights, netgebied Groningen
      		</div>
          <div id="supplier">
    				<div id="supllogo">
    					<img src="images/nuon_on.png" alt="nuon" id="image1" />
    				</div>

            { data ? (
      				<div id="data" style={{ 'fontSize':'26px', 'padding':'0 0 0 20px', color: 'white'}}>
        				<table>
                  <tbody>
            				<tr className="light">
                      <td></td>
                      <td>t</td>
                      <td>t-1</td>
                      <td>t-2</td>
                    </tr>
          				  <tr>
                      <td className="bold">Usage</td>
                      <td>1000</td>
                      <td>900</td>
                      <td>1100</td>
                    </tr>
      				      <tr>
                      <td className="bold">Generation</td>
                      <td>200</td>
                      <td>150</td>
                      <td>0</td>
                    </tr>
      				      <tr>
                      <td className="bold">Demand</td>
                      <td>800</td>
                      <td>750</td>
                      <td>1100</td>
                    </tr>
      				      <tr>
                      <td className="bold">Supply</td>
                      <td>0</td>
                      <td>0</td>
                      <td>0</td>
                    </tr>
      				      <tr>
                      <td className="bold">Real</td>
                      <td>80%</td>
                      <td>65%</td>
                      <td>89%</td>
                    </tr>
                  </tbody>
        				</table>
      				</div>
            ) : <div></div> }
    			</div>
      	</div>
      </div>
    );
  }
}

export default AggregatorDashboard;
