import React, { Component, useMemo, useState } from 'react';
import { useQuery } from '@apollo/react-hooks';
import gql from 'graphql-tag';
import { withApollo } from 'react-apollo';
import { render } from 'react-dom';


const QUERY_TRADES = gql`
  query($symbols: [String], $pageSize: Int, $pageIndex: Int)  {
    trades(symbols: $symbols, pageSize: $pageSize, pageIndex: $pageIndex) {
      success,
      errors,
      totalCount,
      trades {
        id,
        accountId,
        assetCategory,
        symbol,
        underlyingSymbol,
        description,
      }
    }
  }
`;


class TradesPage extends React.Component {
  constructor(props) {
    super()

    this.client = props.client

    this.state = {
      symbols: [],
      data: [],
    }

    this.fetchTrades = this.fetchTrades.bind(this);
    this.formOnChangeSymbols = this.formOnChangeSymbols.bind(this);
  }

  formOnChangeSymbols(event) {
    let input = event.target.value;
    let symbols = input.split(",")
    this.setState({symbols: symbols})
  }

  fetchTrades() {
    const graphqlQueryExpression = {
      query: QUERY_TRADES,
      variables: {
        symbols: this.state.symbols,
      }
    }

    this.client.query(graphqlQueryExpression).then(response => {
      this.setState({data: response.data.trades.trades})
    })
  }

  render() {
    return (
      <div>
        <h1 className="mt-5">Trades</h1>

        <hr/>
        <h4>Filters</h4>

        <div className="row">
          <div className="col-md-4">
            <div className="form-group">
              <label>Symbols</label>
              <input className="form-control" onChange={this.formOnChangeSymbols} />
            </div>
          </div>
        </div>

        <button onClick={this.fetchTrades}>Search</button>

        <br/>
        <br/>

        <table className="table">
          <thead>
            <tr>
              <th>Id</th>
              <th>Symbol</th>
            </tr>
          </thead>

          <tbody>
            {this.state.data.map(trade => {
                return (
                  <tr key={trade.id}>
                    <td>{trade.id}</td>
                    <td>{trade.symbol}</td>
                  </tr>
                )
              })
            }
          </tbody>
        </table>

      </div>
    )
  }
};


const FinalTradesPage = withApollo(TradesPage)

export default FinalTradesPage;
