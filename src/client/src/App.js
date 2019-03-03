import React, { Component } from 'react';
import './App.css';
import axios from "axios";

class App extends Component {

  // This constructor initializes component state
  constructor(props) {
    super(props);

    // Set componenet state
    this.state = {
      address : "",
      data : ""
    }

    // Bind custom internal methods
    this.updateAddress = this.updateAddress.bind(this);
    this.loadData = this.loadData.bind(this);
  }

  componentDidMount() {

  }

  componentWillUnmount() {

  }

  // Update the desired address in the internal state
  updateAddress(event) {
    this.setState({ address: event.target.value });
  }

  // Load the address balance information from the API
  async loadData() {
     const apiHandle = axios.create({
         baseURL : "https://jmcintyre.net/sites/myaddrbal/myaddrbal.py/",
	 timeout : 3000
     });

     const response = await apiHandle.get(this.state.address);
     console.log(response.data);
     const data = response.data;
     this.setState({ data : data });
  }

  render() {

    var table = "";
    if (this.state.data != "")
    {
        var utxo_rows = [];
	for (var i = 0; i < this.state.data.utxos.length; i++)
        {
            utxo_rows.push( (
		<tr>
		    <td>{ this.state.data.utxos[i].tx_id }</td>
		    <td>{ this.state.data.utxos[i].amount }</td>
		    <td>{ this.state.data.utxos[i].spendable.toString() }</td>
		    <td>{ this.state.data.utxos[i].sending_addrs.join(", ") }</td>
		</tr>
	    ) );
	}

        table = (

            <div>
		<h3>Summary</h3>
	    	<table>
		    <tbody>
	                <tr>
	                    <th>Available Balance</th>
	                    <td>{ this.state.data.balance }</td>
	                </tr>
	                <tr>
	                    <th>All Spendable?</th>
	                    <td>{ this.state.data.all_spendable.toString() }</td>
	                </tr>
	                <tr>
	                    <th>Total transactions (current balance only)</th>
	                    <td>{ this.state.data.total_txs }</td>
	                </tr>
		    </tbody>
	        </table>

		<h3>Unspect Transaction Outputs</h3>
		<table>
		    <tbody>
		        <tr>
                            <th>Transaction ID</th>
                            <th>Amount</th>
                            <th>Spendable?</th>
                            <th>Sending Addresses</th>
		        </tr>
			{ utxo_rows }
		    </tbody>
		</table>
           </div>
       );
    }

    return (
      <div className="App">
        <header>
		<h2>Address details for: { this.state.address }</h2>
	    	<p>
                    Enter Address: <input id="address" onChange={this.updateAddress}></input>
	            <button onClick={ this.loadData }>Retrieve Balance Info</button>
	        </p>

                { table }

	    </header>
      </div>
    );
  }
}

export default App;
