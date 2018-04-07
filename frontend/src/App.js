import React, { Component } from 'react';
import axios from 'axios';

import SupplierButton from './components/SupplierButton';
import ImageCheckbox from './components/ImageCheckbox';

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
      profile: {
        'bulb': true,
        'car': false,
        'wind': false,
      },
      selectedSupplier: "nuon",
    };
  }

  selectSupplier(newSelectedSupplier) {
    this.setState({
      selectedSupplier: newSelectedSupplier,
    });
  }

  toggleProfile(profileFactor) {
    this.setState({
      profile: {
        ...this.state.profile,
        [profileFactor]: !this.state.profile[profileFactor],
      },
    });
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
    const { identity, suppliers, selectedSupplier, profile } = this.state;
    return (
      <div className="App">
        <div id="wrap">
          <div id="tabs"><img alt="tabs" src="/images/tab.png" id="tabs-bar"/></div>

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
            <ImageCheckbox name="bulb" enabled={profile.bulb} enabledImage="/images/bulb_on.gif"  disabledImage="/images/bulb_off.png" onClick={() => this.toggleProfile('bulb')}/>
            <ImageCheckbox name="car" enabled={profile.car} enabledImage="/images/car_on.gif"  disabledImage="/images/car_off.png" onClick={() => this.toggleProfile('car')}/>
            <ImageCheckbox name="wind" enabled={profile.wind} enabledImage="/images/wind_on.gif"  disabledImage="/images/wind_off.png" onClick={() => this.toggleProfile('wind')}/>
        	</div>

        	<div id="usage">
        		<div id="title"></div>

        		<div id="usage_sub">
        			<div id="title_sub">My usage</div>
        		  <span>1000 Wh</span>
        		</div>

        		<div id="usage_sub">
        			<div id="title_sub">Generating</div>
        		  <span>300 Wh</span>
        		</div>

        		<div id="usage_sub">
        			<div id="title_sub">Demand</div>
        		  <span>700 Wh</span>
        		</div>

        		<div id="usage_sub">
        			<div id="title_sub">Supply</div>
        		  <span>0 Wh</span>
        		</div>
        	</div>

        </div>
      </div>
    );
  }
}

export default App;
