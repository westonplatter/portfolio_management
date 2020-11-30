import React, { Component } from "react";

 
class TradesPage extends Component {
  constructor() {
    super()
    this.state = {
      trades: {},
    }
  }

  componentDidMount() {
    console.log("this");
  }

  render() {
    return (
      <div className="row">
        <h1 className="mt-5">Trades Page</h1>
      </div>
    );
  }
}
 
export default TradesPage;