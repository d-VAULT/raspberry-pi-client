import React, { Component } from 'react';

const styles = {
  width: '135px',
  paddingRight: '20px',
};

class ImageCheckbox extends Component {
  render() {
    const { name, enabled, enabledImage, disabledImage } = this.props;
    return (
    	<img src={(enabled===true ? enabledImage : disabledImage)}
           style={styles} alt={name} onClick={this.props.onClick}/>
    );
  }
}

export default ImageCheckbox;
