import React, { Component } from 'react';
import './App.css';
import axios from "axios";
import { AddressTable } from './AddressTable';
import { IAddressData } from './AddressInfoTypes';

interface IAppState
{
	address: string;
	currency: string;
	data: IAddressData;
}

class App extends Component<{}, IAppState>
{

	// This constructor initializes component state
	constructor(props : any) 
	{
		super(props);

		// Set component state
		this.state = {
			address : "",
			currency: "bch",
			data : {
				 balance: 0.00,
				 all_spendable: false,				 
				 total_txs: 0,
				 utxos : []
			}
		}
	
		// Bind custom internal methods
		this.handleCurrencyChange = this.handleCurrencyChange.bind(this);
		this.renderCurrencySelect = this.renderCurrencySelect.bind(this);
		this.updateAddress = this.updateAddress.bind(this);
		this.loadData = this.loadData.bind(this);
	}

	// Update the desired address in the internal state
	updateAddress(event: React.FormEvent<HTMLInputElement>) 
	{
		this.setState({ address: (event.target as HTMLInputElement).value });
	}

	// Load the address balance information from the API
	async loadData()
	{
		const apiHandle = axios.create({
			baseURL : "https://jmcintyre.net/sites/myaddrbal/myaddrbal.py/",
			timeout : 3000
		});

		const urlTail : string= this.state.address + "/" + this.state.currency;
		const response = await apiHandle.get(urlTail);

		const data : IAddressData = response.data;
		this.setState({ data : data });
	}

	handleCurrencyChange(event: React.FormEvent<HTMLSelectElement>)
	{
		this.setState({ currency : (event.target as HTMLSelectElement).value });
	}

	renderCurrencySelect()
	{
		return (
			<select value={ this.state.currency } onChange={ this.handleCurrencyChange }>
			<option value="bch">Bitcoin Cash (BCH)</option>
			<option value="btc">Bitcoin (BTC) </option>
			</select>
		);
	}

	render() 
	{

		return (
			<div className="App">
				<header>
					<h2>Address details for: { this.state.address }</h2>
					<p>
						Enter Address: <input id="address" onChange={this.updateAddress}></input>
						<button onClick={ this.loadData }>Retrieve Balance Info</button>
					</p>

					{ this.renderCurrencySelect() }

					<AddressTable data={this.state.data} />

				</header>
			</div>
		);
	}
}

export default App;
