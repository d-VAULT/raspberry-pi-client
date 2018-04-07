import React, { Component } from 'react';
import axios from 'axios';
import './App.css';

class App extends Component {
  constructor() {
    super();
    this.state = {
      identity: "loading",
      selectedSupplier: "nuon",
    };
  }

  selectSupplier(newSelectedSupplier) {
    this.setState({
      selectedSupplier: newSelectedSupplier,
    })
  }

  componentDidMount() {
    axios
      .get('/api/identity')
      .then(response => {
        this.setState({
          identity: response.data,
        });
      })
      .catch(error => {
        console.error(error);
      });
  }

  render() {
    const { identity, selectedSupplier } = this.state;
    return (
      <div className="App">
        <div id="wrap">
          <div id="tabs">
            <img src="/images/tab.png" id="tabs-bar"/>
          </div>

        	<div id="supplier">
        		<div id="title">
        		Supplier
        		</div>
          	<img src={"/images/nuon_" + (selectedSupplier==='nuon' ? 'on' : 'off') + ".png"} id="image1" onClick={() => this.selectSupplier('nuon')}/>
          	<img src={"/images/budget_" + (selectedSupplier==='budget-energie' ? 'on' : 'off') + ".png"} id="image1" onClick={() => this.selectSupplier('budget-energie')}/>
          	<img src={"/images/bron_" + (selectedSupplier==='vandebron' ? 'on' : 'off') + ".png"} id="image1" onClick={() => this.selectSupplier('vandebron')}/>


        	</div>



        	<div id="power">
        		<div id="title">
        		  My power ({ identity })
        		</div>
          	<img src="/images/bulb_off.png" id="image2"/>
          	<img src="/images/car_off.png" id="image2"/>
          	<img src="/images/mill_off.png" id="image2"/>
        	</div>



        	<div id="usage">
        		<div id="title">
        		</div>

        		<div id="usage_sub">
        			<div id="title_sub">
        			My usage
        			</div>
        		1000
        		</div>

        		<div id="usage_sub">
        			<div id="title_sub">
        			Generating
        			</div>
        		300
        		</div>

        		<div id="usage_sub">
        			<div id="title_sub">
        			Demand
        			</div>
        		700
        		</div>

        		<div id="usage_sub">
        			<div id="title_sub">
        			Supply
        			</div>
        		0
        		</div>

        	</div>

        </div>
      </div>
    );
  }
}

export default App;
