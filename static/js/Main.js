import React, { Component } from "react";
import {
  Route,
  NavLink,
  HashRouter
} from "react-router-dom";

import Home from "./Home";
import Trades from "./Trades";

 
class Main extends Component {
  render() {
    return (
      <HashRouter>
        <div>
          <h1>Simple SPA</h1>
          <ul className="header">
            <li><NavLink exact to="/">Home</NavLink></li>
            <li><NavLink exact to="/trades">Trades</NavLink></li>
          </ul>
          <div className="content">
            <Route exact path="/" component={Home}/>
            <Route path="/trades" component={Trades}/>
          </div>
        </div>
      </HashRouter>
    );
  }
}
 
export default Main;
