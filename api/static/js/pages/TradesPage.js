import React from 'react';
import { useQuery } from '@apollo/react-hooks';
import gql from 'graphql-tag';

const QUERY_TRADES = gql`
  query($symbol: String)  {
    trades(symbol: $symbol) {
      success, errors
      trades {
        id,
        symbol,
        accountId,
        transactionID,
        tradeID,
        description,
        strike
      }
    }
  }
`;

const TradesPage = () => {
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
        <h1 className="mt-5">Trades Page</h1>

        <table className="table">
          <thead>
            <tr>
              <th>Id</th>
            </tr>
          </thead>
          <tbody>
            {data.trades.trades.map(trade => (
              <tr key={trade.id}>
                <td>{trade.id}</td>
              </tr>)
            )}
          </tbody>
        </table>
      </div>
    </>
  );
};

export default TradesPage;
