import gql from 'graphql-tag';

const QUERY_TRADES = gql`
  query($symbols: [String], $accountIds: [String], $pageSize: Int, $pageIndex: Int)  {
    trades(symbols: $symbols, accountIds: $accountIds, pageSize: $pageSize, pageIndex: $pageIndex) {
      success
      errors
      totalCount
      trades {
        id
        ibExecId
        ibOrderId
        symbol
        underlyingSymbol
        assetCategory
        accountId
        dateTime
        buySell
        expiry
        fifoPnlRealized
        openCloseIndicator
        proceeds
        putCall
        quantity
        strike
      }
    }
  }
`;

const QUERY_ACCOUNTS = gql`
  query {
    accounts {
      success
      errors
      accounts {
        accountId
      }
    }
  }
`


export {
  QUERY_TRADES,
  QUERY_ACCOUNTS
}
