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
      selectedSupplier: "nuon",
    };
  }

  componentDidMount() {
    axios
      .get('/api/identity')
      .then(response => {
        this.setState({
          identity: response.data.identity,
          profile: response.data.profile,
        });
        if (!this.state.pollTimerId) {
          this.startPolling();
        }
      })
      .catch(error => {
        console.error(error);
      });
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
      .get('/api/data')
      .then(response => response.data)
      .then(data => {
        self.setState({
          data
        })
      })
  }

  selectSupplier(newSelectedSupplier) {
    this.setState({
      selectedSupplier: newSelectedSupplier,
    });
  }

  toggleProfile(profileFactor) {
    const newProfile = {
      ...this.state.profile,
      [profileFactor]: !this.state.profile[profileFactor],
    };
    axios
      .post('/api/update-profile', newProfile, {
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
      })
      .then(response => response.data)
      .then(data => {
        this.setState({
          profile: data.profile,
        });
      });

  }

  render() {
    const { identity, suppliers, selectedSupplier, profile, data } = this.state;
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

          { profile ? (
          	<div id="power">
          		<div id="title">
          		  My power ({ identity })
          		</div>
              <ImageCheckbox name="bulb" enabled={profile.bulb} enabledImage="/images/bulb_on.gif"  disabledImage="/images/bulb_off.png" onClick={() => this.toggleProfile('bulb')}/>
              <ImageCheckbox name="car" enabled={profile.car} enabledImage="/images/car_on.gif"  disabledImage="/images/car_off.png" onClick={() => this.toggleProfile('car')}/>
              <ImageCheckbox name="wind" enabled={profile.wind} enabledImage="/images/wind_on.gif"  disabledImage="/images/wind_off.png" onClick={() => this.toggleProfile('wind')}/>
        	  </div>
          ) : "" }

        	{ data ? (
            <div id="usage">
          		<div id="title"></div>

          		<div id="usage_sub">
          			<div id="title_sub">My usage</div>
          		  <span>{ data.usage } W</span>
          		</div>

          		<div id="usage_sub">
          			<div id="title_sub">Generating</div>
          		  <span>{ data.generation } W</span>
          		</div>

          		<div id="usage_sub">
          			<div id="title_sub">Demand</div>
          		  <span>{ data.demand } W</span>
          		</div>

          		<div id="usage_sub">
          			<div id="title_sub">Supply</div>
          		  <span>{ data.supply } W</span>
          		</div>
          	</div>
          ) : "loading data" }

        </div>
      </div>
    );
  }
}

export default App;
