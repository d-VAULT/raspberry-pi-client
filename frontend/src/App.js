import React, { Component } from 'react';
import axios from 'axios';
// import logo from './logo.svg';
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
        <div id="wrap">

        	<div id="supplier">
        		<div id="title">
        		Supplier
        		</div>
          	<img src="/images/nuon_off.png" id="image1"/>
          	<img src="/images/budget_off.png" id="image1"/>
          	<img src="/images/bron_off.png" id="image1"/>

        		<img src="/images/share.png" id="image2"/>
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

        	<div id="logo">
        		<img src="/images/logo.png" id="image3" />

        	</div>


        	</div>

        </div>
      </div>
    );
  }
}

export default App;
