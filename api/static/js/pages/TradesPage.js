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
        super(props)

        this.client = props.client

        this.state = {
            symbols: [],
            underlyingSymbols: [],
            accountIds: [],
            openClose: "C",
            data: [],
            dataSelected: [],
        }

        // this.renderDataSelected = this.renderDataSelected.bind(this)

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
            underlyingSymbols: this.state.underlyingSymbols,
            accountIds: this.state.accountIds,
            openClose: this.state.openClose,
        }

        const graphqlQueryExpression = {
            query: QUERY_TRADES,
            variables: variables
        }

        const formatResponse = (res) => res.data.trades.trades

        this.client.query(graphqlQueryExpression).then(res => {
            this.setState({data: formatResponse(res)})}
        )
    }

    selectedDataToggle = (id) => {
        if (this.state.dataSelected.map(x => x).indexOf(id) == -1) {
            // add it
            this.state.data.map(trade => {
                if (trade.id == id) {
                    this.setState({ dataSelected: [...this.state.dataSelected, id] })
                }
            })

        } else {
            // remove it
            // console.log(`Removing tradeId = ${id}`)
        }
    }

    renderDataSelected = () => {
        // collected the selected trades
        let selectedTrades = this.state.data.filter(trade => this.state.dataSelected.indexOf(trade.id) != -1)

        // create aggregated metrics
        let aggProceeds = selectedTrades.map(trade => parseFloat(trade.proceeds)).reduce((a, b) => a + b, 0);
        let aggPNL = selectedTrades.map(trade => parseFloat(trade.fifoPnlRealized)).reduce((a, b) => a + b, 0);

        // render row
        if (this.state.dataSelected.length > 0) {
            return (
                <tr>
                    <td>Rows: {this.state.dataSelected.length}</td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td></td>
                    <td>{aggProceeds}</td>
                    <td>{aggPNL}</td>
                </tr>
            )
        }
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

            <table className="table pm-small-font">
            <thead>
                <tr>
                    <th>
                        <button className="btn btn-secondary btn-sm" href="#">All</button>&nbsp;
                        <button className="btn btn-secondary btn-sm" href="#">None</button>
                    </th>
                    <th>Date</th>
                    <th>Symbol</th>
                    <th>Underlying Symbol</th>
                    <th>Expiration</th>
                    <th>Strike</th>
                    <th>Open/Close</th>
                    <th>Proceeds</th>
                    <th>PnL</th>
                    <th>Notes</th>
                    <th>AccountId</th>
                </tr>
            </thead>

            <tbody>
                {this.renderDataSelected()}

                {this.state.data.map(trade => {
                    return (
                        <tr key={trade.id}>
                            <td>
                                <div>
                                    <input
                                        className="form-check-input"
                                        type="checkbox"
                                        onClick={() => this.selectedDataToggle(trade.id) }
                                    ></input>
                                </div>
                            </td>
                            <td>{trade.dateTime}</td>
                            <td>{trade.symbol}</td>
                            <td>{trade.underlyingSymbol}</td>
                            <td>{trade.expiry}</td>
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
