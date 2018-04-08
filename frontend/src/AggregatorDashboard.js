import React, { Component } from 'react';
import axios from 'axios';

const sortNewestFirst = (recordA, recordB) => {
  return recordA.timestamp < recordB.timestamp;
};

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
    const pollTimerId = setInterval(this.poll, 2000, this);
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
        const dataWithCycleID = data.filter((item) => {
          return item.json_message.cycle_id
        })
        const reportRecords = dataWithCycleID.reduce((result, item, i) => {
          const cycleId = item.json_message.cycle_id;
          const reportRecord = result.find((record) => { return record.cycleId === cycleId });
          if (typeof reportRecord === 'undefined') {
            result.push({
              cycleId,
              reports: [item],
            });
          } else {
            reportRecord.reports.push(item);
          }
          return result;
        }, []);
        const viewData = reportRecords.map((record) => {
          return {
            cycleId: record.cycleId,
            averageTotalUsage: Math.round(record.reports[0].json_message.total_energy_usage * 100) / 100,
            numResults: record.reports.length,
            timestamp: record.reports[0].timestamp,
          }
        }).sort(sortNewestFirst).slice(0,8);
        // const mockData = [{
        //   cycleId: 286798123,
        //   averageTotalUsage: 1000,
        // }]
        self.setState({
          data: viewData
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
                      {
                        data.map(record => <td>{ record.averageTotalUsage }</td>)
                      }
                    </tr>
      				      <tr>
                      <td className="bold">Generation</td>
                      {
                        data.map(record => <td> 0 </td>)
                      }
                    </tr>
      				      <tr>
                      <td className="bold">Demand</td>
                      {
                        data.map(record => <td> 0 </td>)
                      }
                    </tr>
      				      <tr>
                      <td className="bold">Supply</td>
                      {
                        data.map(record => <td> 0 </td>)
                      }
                    </tr>
      				      <tr>
                      <td className="bold">Real</td>
                      {
                        data.map(record => <td> { Math.round(record.numResults / 6 * 100 * 100 ) / 100 }% </td>)
                      }
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
