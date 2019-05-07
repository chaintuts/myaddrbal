## General
____________

### Author
* Josh McIntyre

### Website
* jmcintyre.net

### Overview
* MyAddrBal provides a REST API for understanding/working with current address balances

## Development
________________

### Git Workflow
* master for releases (merge development)
* development for bugfixes and new features

### Building
* make build
Build the application
* make clean
Clean the build directory

### Features
* Show address balance information with associated UTXOs. 
This mid-level abstraction can help a user better understand or work with an address balance by pulling 
relevant data from raw transactions and UTXOs associated with an address
* Show the balance information in a formatted table with the React web client
* Pull raw data from commonly available APIs. Currently supported: rest.bitcoin.com (BCH)

### Requirements
* Requires Python 3 for API
* Requires NPM for React web client

### Platforms
* Firefox
* Chrome

## Usage
____________

### API usage
* Visit the root url with and address (/<address>/<currency>) for information
* Address should be a valid address for the specified currency
* Supported currency tickers: "bch", "btc"

### Web client usage
* Enter the address in the text input and click "Retrieve balance info"
* Information will be fetched and shown in a formatted table
