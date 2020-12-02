import React from 'react';
import {
  Route,
  NavLink,
  Link
} from 'react-router-dom';

import HomePage from './pages/HomePage';
import TradesPage from './pages/TradesPage';

const App = () => (
  <>
    <header>
      <nav className="navbar navbar-expand-md navbar-dark fixed-top bg-dark">
        <a className="navbar-brand" href="#">Portfolio Manager</a>
        <button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarCollapse" aria-controls="navbarCollapse" aria-expanded="false" aria-label="Toggle navigation">
          <span className="navbar-toggler-icon" />
        </button>
        <div className="collapse navbar-collapse" id="navbarCollapse">
          <ul className="navbar-nav mr-auto">
            <li>
              <NavLink exact className="nav-link" to="/">Home</NavLink>
            </li>
            <li className="nav-item">
              <Link className="nav-link" to="/trades">Trades</Link>
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
      <Route exact path="/" component={HomePage} />
      <Route path="/trades" component={TradesPage} />
    </main>

    <footer className="footer">
      <div className="container">
        <span className="text-muted"><small>&copy; Copyright 2020, Weston Platter</small></span>
      </div>
    </footer>
  </>
);

export default App;
