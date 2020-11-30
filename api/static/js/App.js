import React, { Component } from "react";
import {
  Route,
  NavLink,
  Link,
  HashRouter
} from "react-router-dom";

import HomePage from "./pages/HomePage";
import TradesPage from "./pages/TradesPage";
 
const App = () => {
  return (
    <HashRouter>
      <header>
        <nav className="navbar navbar-expand-md navbar-dark fixed-top bg-dark">
          <a className="navbar-brand" href="#">Portfolio Manager</a>
          <button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarCollapse" aria-controls="navbarCollapse" aria-expanded="false" aria-label="Toggle navigation">
            <span className="navbar-toggler-icon"></span>
          </button>
          <div className="collapse navbar-collapse" id="navbarCollapse">
            <ul className="navbar-nav mr-auto">
              {/* <li className="nav-item active">
                <a className="nav-link" href="#">Home <span className="sr-only">(current)</span></a>
              </li> */}
              <li>
                <NavLink className="nav-link" exact to="/">Home</NavLink>
              </li>
              <li className="nav-item">
                <Link className="nav-link" exact to="/trades">Trades</Link>
              </li>
            </ul>
            <form className="form-inline mt-2 mt-md-0">
              <input className="form-control mr-sm-2" type="text" placeholder="Search" aria-label="Search" />
              <button className="btn btn-outline-success my-2 my-sm-0" type="submit">Search</button>
            </form>
          </div>
        </nav>
      </header>

      <main role="main" className="container">
        <div className="">
          <Route exact path="/" component={HomePage}/>
          <Route path="/trades" component={TradesPage}/>
        </div>
      </main>

      <footer className="footer">
        <div className="container">
          <span className="text-muted"><small>&copy; Copyright 2020, Weston Platter</small></span>
        </div>
      </footer>
    </HashRouter>
  )
}

export default App;
