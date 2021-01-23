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
      underlyingSymbols: [],
      accountIds: [],
      openClose: "C",
      data: [],
    }

    this.fetchTrades = this.fetchTrades.bind(this)
    this.handleAsyncLoadAccounts = this.handleAsyncLoadAccounts.bind(this)
    this.formOnChangeSymbols = this.formOnChangeSymbols.bind(this)
    this.formOnChangeUnderlyingSymbols = this.formOnChangeUnderlyingSymbols.bind(this)
    this.formOnChangeAccounts = this.formOnChangeAccounts.bind(this)
    this.formOnChangeOpenClose = this.formOnChangeOpenClose.bind(this)

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
    const getAccountIds = (inputs) => {
      if (inputs != null) {
        return inputs.map(x => x.value)
      } else {
        return []
      }
    }

    this.setState({accountIds: getAccountIds(inputs)}, () => {
      this.fetchTrades()
    })
  }

  formOnChangeSymbols(event) {
    let input = event.target.value;
    let symbols = input.split(",").filter(x => x != "" && x != "")
    this.setState({symbols: symbols}, () => {
      this.fetchTrades()
    })
  }

  formOnChangeUnderlyingSymbols(event) {
    let input = event.target.value;
    let us = input.split(",").filter(x => x != "" && x != "")
    this.setState({underlyingSymbols: us}, () => {
      this.fetchTrades()
    })
  }

  formOnChangeOpenClose(event) {
    let input = event.target.value;
    this.setState({openClose: input}, () => {
      this.fetchTrades()
    })
  }

  fetchTrades() {
    const variables = {
      symbols: this.state.symbols,
      underlyingSymbols: this.state.underlyingSymbols,
      accountIds: this.state.accountIds,
      openClose: this.state.openClose,
    }

    console.log(variables)

    const graphqlQueryExpression = {
      query: QUERY_TRADES,
      variables: variables
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
      <div style={{width: "100%"}}>
        <h1 className="mt-5">Trades</h1>

        <hr/>
        <h4>Filters</h4>

        <div className="row">
          <div className="col-md-4">

            <div className="form-group">
              <label>Open/Close</label>
              <input
                className="form-control"
                onChange={this.formOnChangeOpenClose}
                onBlur={this.formOnChangeOpenClose}
                value={this.state.openClose} />
            </div>

            <div className="form-group">
              <label>Symbols</label>
              <input
                className="form-control"
                onChange={this.formOnChangeSymbols}
                onBlur={this.formOnChangeSymbols} />
            </div>

            <div className="form-group">
              <label>Underlying Symbols</label>
              <input
                className="form-control"
                onChange={this.formOnChangeUnderlyingSymbols}
                onBlur={this.formOnChangeUnderlyingSymbols} />
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

        <br/>
        <br/>

        <table className="table">
          <thead>
            <tr>
              <th>Id</th>
              <th>Date</th>
              <th>Symbol</th>
              <th>Underlying Symbol</th>
              <th>Strike</th>
              <th>Open/Close</th>
              <th>Proceeds</th>
              <th>PnL</th>
              <th>Notes</th>
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
                    <td>{trade.strike}</td>
                    <td>{trade.openCloseIndicator}</td>
                    <td>{trade.proceeds}</td>
                    <td>{trade.fifoPnlRealized}</td>
                    <td>{trade.notes}</td>
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
