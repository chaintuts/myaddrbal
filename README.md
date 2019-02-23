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
* Pull raw data from commonly available APIs. Currently supported: rest.bitcoin.com (BCH)

### Requirements
* Requires Python 3

### Platforms
* Firefox
* Chrome

## Usage
____________

### Command line usage
* Visit the root url with and address (/<address>) for information
