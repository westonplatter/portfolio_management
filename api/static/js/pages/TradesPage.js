// external packages
import React, { Component, useMemo, useState } from 'react';
import { useQuery } from '@apollo/react-hooks';
import gql from 'graphql-tag';
import { withApollo } from 'react-apollo';
import { render } from 'react-dom';
import AsyncSelect from 'react-select/async';

// internal packages
import {QUERY_TRADES, QUERY_ACCOUNTS} from '../GraphQueries.js'


class TradesPage extends React.Component {
  constructor(props) {
    super()

    this.client = props.client

    this.state = {
      symbols: [],
      accountIds: [],
      data: [],
    }

    this.fetchTrades = this.fetchTrades.bind(this);
    this.handleAsyncLoadAccounts = this.handleAsyncLoadAccounts.bind(this)
    this.formOnChangeSymbols = this.formOnChangeSymbols.bind(this);
    this.formOnChangeAccounts = this.formOnChangeAccounts.bind(this)
  }

  handleAsyncLoadAccounts(inputValue) {
    let graphqlQueryExpression = {
      query: QUERY_ACCOUNTS
    }

    const transformDataIntoValueLabel = (data) => {
      return data.accounts.accounts.map(ix => {
        return { value: ix.accountId, label: ix.accountId }
      })
    }

    return new Promise(resolve => {
      this.client.query(graphqlQueryExpression).then(response => {
        resolve(transformDataIntoValueLabel(response.data))
      })
    });
  }

  formOnChangeAccounts(inputs) {
    let accountIds = inputs.map(x => x.value)
    this.setState({accountIds: accountIds})
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
        accountIds: this.state.accountIds,
      }
    }

    const formatResponse = (response) => {
      let trades = response.data.trades.trades
      return trades
    }

    this.client.query(graphqlQueryExpression).then(response => {
      this.setState({data: formatResponse(response)})
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

            <div className="form-group">
              <div className="select-index-input" style={{width: 400, display: "inline-block"}}>
                <AsyncSelect
                  onChange={this.formOnChangeAccounts}
                  isMulti={true}
                  cacheOptions={true}
                  defaultOptions={true}
                  loadOptions={this.handleAsyncLoadAccounts} />
              </div>
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
              <th>Date</th>
              <th>Symbol</th>
              <th>Underlying Symbol</th>
              <th>Open/Close</th>
              <th>Proceeds</th>
              <th>PnL</th>
              <th>AccountId</th>
            </tr>
          </thead>

          <tbody>
            {this.state.data.map(trade => {
                return (
                  <tr key={trade.id}>
                    <td>{trade.id}</td>
                    <td>{trade.dateTime}</td>
                    <td>{trade.symbol}</td>
                    <td>{trade.underlyingSymbol}</td>
                    <td>{trade.openCloseIndicator}</td>
                    <td>{trade.proceeds}</td>
                    <td>{trade.fifoPnlRealized}</td>
                    <td>{trade.accountId}</td>
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
