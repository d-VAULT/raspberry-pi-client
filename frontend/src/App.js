import React, { Component } from 'react';
import axios from 'axios';

import SupplierButton from './components/SupplierButton';

import './App.css';

class App extends Component {
  constructor() {
    super();
    this.state = {
      identity: "loading",
      suppliers: [
        'nuon',
        'budget-energie',
        'vandebron',
      ],
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
    const { identity, suppliers, selectedSupplier } = this.state;
    return (
      <div className="App">
        <div id="wrap">
          <div id="tabs"><img src="/images/tab.png" id="tabs-bar"/></div>

        	<div id="supplier">
        		<div id="title">Supplier</div>
            { suppliers.map(supplier =>
              <SupplierButton key={supplier} supplierName={supplier} selected={selectedSupplier===supplier} onClick={() => this.selectSupplier(supplier)}/>
            )}
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
        		<div id="title"></div>

        		<div id="usage_sub">
        			<div id="title_sub">My usage</div>
        		  <span>1000</span>
        		</div>

        		<div id="usage_sub">
        			<div id="title_sub">Generating</div>
        		  <span>300</span>
        		</div>

        		<div id="usage_sub">
        			<div id="title_sub">Demand</div>
        		  <span>700</span>
        		</div>

        		<div id="usage_sub">
        			<div id="title_sub">Supply</div>
        		  <span>0</span>
        		</div>
        	</div>

        </div>
      </div>
    );
  }
}

export default App;
