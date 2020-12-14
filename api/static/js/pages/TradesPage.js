import React, { useMemo, useState } from 'react';
import { useQuery } from '@apollo/react-hooks';
import gql from 'graphql-tag';
import { useTable, usePagination} from "react-table";
import { withApollo } from 'react-apollo';


const QUERY_TRADES = gql`
  query($symbol: String, $pageSize: Int, $pageIndex: Int)  {
    trades(symbol: $symbol, pageSize: $pageSize, pageIndex: $pageIndex) {
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


function Table({
    columns,
    data,
    fetchData,
    loading,
    pageCount: controlledPageCount,
  }) {
    const {
      getTableProps,
      getTableBodyProps,
      headerGroups,
      rows,
      prepareRow,
      page,
      canPreviousPage,
      canNextPage,
      pageOptions,
      pageCount,
      gotoPage,
      nextPage,
      previousPage,
      setPageSize,
      state: { pageIndex, pageSize },
    } = useTable({
      columns,
      data,
      initialState: { pageIndex: 0 }, // Pass our hoisted table state
      manualPagination: true, // Tell the usePagination
      pageCount: controlledPageCount,
    },
    usePagination
  )

  React.useEffect(() => {
    fetchData({ pageIndex, pageSize })
  }, [fetchData, pageIndex, pageSize, controlledPageCount])

  // Render the UI for your table
  return (
    <>
      <pre>
        <code>
          {JSON.stringify(
            {
              pageIndex,
              pageSize,
              pageCount,
              canNextPage,
              canPreviousPage,
            },
            null,
            2
          )}
        </code>
      </pre>
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
          <tr>
            {loading ? (
              // Use our custom loading state to show a loading indicator
              <td colSpan="10000">Loading...</td>
            ) : (
              <td colSpan="10000">
                Showing {page.length} of ~{controlledPageCount * pageSize}{' '}
                results
              </td>
            )}
          </tr>
        </tbody>
      </table>
      <div className="pagination">
        <button onClick={() => gotoPage(0)} disabled={!canPreviousPage}>
          {'<<'}
        </button>{' '}
        <button onClick={() => previousPage()} disabled={!canPreviousPage}>
          {'<'}
        </button>{' '}
        <button onClick={() => nextPage()} disabled={!canNextPage}>
          {'>'}
        </button>{' '}
        <button onClick={() => gotoPage(pageCount - 1)} disabled={!canNextPage}>
          {'>>'}
        </button>{' '}
        <span>
          Page{' '}
          <strong>
            {pageIndex + 1} of {pageOptions.length}
          </strong>{' '}
        </span>
        <span>
          | Go to page:{' '}
          <input
            type="number"
            defaultValue={pageIndex + 1}
            onChange={e => {
              console.log("hi")
              const page = e.target.value ? Number(e.target.value) - 1 : 0
              gotoPage(page)
            }}
            style={{ width: '100px' }}
          />
        </span>{' '}
        <select
          value={pageSize}
          onChange={e => {
            setPageSize(Number(e.target.value))
          }}
        >
          {[10, 20, 30, 40, 50].map(pageSize => (
            <option key={pageSize} value={pageSize}>
              Show {pageSize}
            </option>
          ))}
        </select>
      </div>
    </>
  )
}

const BaseTradesPage = (props) => {
  // https://react-table.tanstack.com/docs/examples/pagination-controlled
  // https://codesandbox.io/s/react-table-controlled-table-forked-t7fv8?file=/index.js:1717-1759

  // TODO - enable the increment and decrement page buttons
  // TODO - stop the fetchData function from being constantly called

  const client = props.client
  const [data, setData] = React.useState([])
  const [loading, setLoading] = React.useState(false)
  const [pageCount, setPageCount] = React.useState(0)
  const fetchIdRef = React.useRef(0)

  const columns = React.useMemo(
    () =>
      [
          {
            Header: 'AccountId',
            accessor: 'accountId',
          },
          {
            Header: "AssetCategory",
            accessor: 'assetCategory'
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

  const fetchData = React.useCallback(({ pageSize, pageIndex }) => {
    // This will get called when the table needs new data
    // You could fetch your data from literally anywhere,
    // even a server. But for this example, we'll just fake it.

    // Give this fetch an ID
    const fetchId = ++fetchIdRef.current

    if (fetchId === fetchIdRef.current) {
      // Set the loading state
      setLoading(true)
      let graphqlQueryExpression = {
        query: QUERY_TRADES,
        variables: {
          symbol: "",
          pageSize: pageSize,
          pageIndex: pageIndex
        }
      }

      client.query(graphqlQueryExpression).then(response => {
        setData(response.data.trades.trades)
        // setPageCount(response.data.totalCount/100)
        setPageCount(10)
        setLoading(false)
      })
    }
  }, [])


  if (loading) return <p>Loading ...</p>;

  return (
    <>
      <div className="row">
        <div className="col-md-12">
          <h1>Trades</h1>
        </div>
      </div>

      <div className="row" style={{marginTop: 10, marginBottom: 100}}>
        <div className="col-md-12">
          <Table
            columns={columns}
            data={data}
            fetchData={fetchData}
            pageCount={pageCount}
            loading={loading}
          />
        </div>
      </div>
    </>
  )
};

const TradesPage = withApollo(BaseTradesPage);

export default TradesPage;
