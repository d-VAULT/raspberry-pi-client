import React, { Component } from 'react';

const styles = {
  width: '200px',
  paddingBottom: '20px',
};

class SupplierButton extends Component {
  render() {
    const { supplierName, selected } = this.props;
    return (
    	<img src={"/images/" + supplierName + "_" + (selected ? 'on' : 'off') + ".png"}
           style={styles} alt={supplierName} onClick={this.props.onClick}/>
    );
  }
}

export default SupplierButton;
