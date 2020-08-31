# PnL Reporting

## Goals

Mark-to-Market statments are great for seeing aggregate PnL, but they lack
detailed reporting on a per account and per strategy basic. For example,
what's the ROI of my covered call strategies on tech vs energy names? Or,
within the tech covered call strategy, what's been working well - 30 delta
weeklies or 45 delta quarterlies?

Therefore,

- [ ] Download data from IB's Flex Reports and story in Postgres
- [ ] Create a simple but functional UI to display trade data
- [ ] Enable users to group trades into strategies (ie, all covered call transactions in 1 group)
- [ ] Enable users to aggregate groups and trades into strategies
- [ ] Financial ROI reporting at the strategy level

## License
MIT. See license file.

