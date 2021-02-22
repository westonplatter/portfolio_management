import gql from 'graphql-tag';

const QUERY_TRADES = gql`
  query($underlyingSymbols: [String], $accountIds: [String], $openClose: String, $pageSize: Int, $pageIndex: Int)  {
    trades(underlyingSymbols: $underlyingSymbols, accountIds: $accountIds, openClose: $openClose, pageSize: $pageSize, pageIndex: $pageIndex) {
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
        notes
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
