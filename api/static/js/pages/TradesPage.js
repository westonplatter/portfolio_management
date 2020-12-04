import React, { useMemo } from 'react';
import { useQuery } from '@apollo/react-hooks';
import gql from 'graphql-tag';
import { useTable } from "react-table";

const QUERY_TRADES = gql`
  query($symbol: String)  {
    trades(symbol: $symbol) {
      success, errors
      trades {
        id,
        accountId,

        transactionID,
        tradeID,

        symbol,
        underlyingSymbol,

        conId,
        securityID,
        securityIDType,
        underlyingConid,
        underlyingSecurityID,
        description,
        strike
      }
    }
  }
`;


function Table({columns, data}) {
  // Use the state and functions returned from useTable to build your UI
  const {
    getTableProps,
    getTableBodyProps,
    headerGroups,
    rows,
    prepareRow,
  } = useTable({
    columns,
    data
  })

  // Render the UI for your table
  return (
    <table className='table' {...getTableProps()}>
      <thead>
        {headerGroups.map(headerGroup => (
          <tr {...headerGroup.getHeaderGroupProps()}>
            {headerGroup.headers.map(column => (
              <th {...column.getHeaderProps()}>{column.render('Header')}</th>
            ))}
          </tr>
        ))}
      </thead>
      <tbody {...getTableBodyProps()}>
        {rows.map((row, i) => {
          prepareRow(row)
          return (
            <tr {...row.getRowProps()}>
              {row.cells.map(cell => {
                return <td {...cell.getCellProps()}>{cell.render('Cell')}</td>
              })}
            </tr>
          )
        })}
      </tbody>
    </table>
  )
}

const TradesPage = () => {
  const columns = React.useMemo(
    () =>
      [
          {
            Header: 'Id',
            accessor: 'id',
          },
          {
            Header: 'Underlying Symbol',
            accessor: 'underlyingSymbol',
          },
          {
            Header: 'Symbol',
            accessor: 'symbol',
          },
        ],
    []
  )

  const { loading, error, data } = useQuery(QUERY_TRADES, {
    variables: {
      symbol: "",
    }
  })

  if (loading) return <p>Loading ...</p>;
  if (error) return <p>Error ...</p>;

  return (
    <>
      <div className="row">
        <div className="col-md-12">
          <h1>Trades</h1>
        </div>
      </div>

      <div className="row" style={{marginTop: 10}}>
        <div className="col-md-12">
          <Table columns={columns} data={data.trades.trades} />
        </div>
      </div>
    </>
  )
};

export default TradesPage;
