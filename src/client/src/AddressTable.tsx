import React, { Component } from 'react';
import './App.css';
import { IAddressData } from './AddressInfoTypes';


interface IAddressTableProps
{
	data: IAddressData;
}

export class AddressTable extends Component<IAddressTableProps, {}>
{
	constructor(props : IAddressTableProps)
	{
		super(props);
	}

	render()
	{
    
	var table : JSX.Element;
		var utxo_rows : JSX.Element[] = [];
		for (var i = 0; i < this.props.data.utxos.length; i++)
		{
			utxo_rows.push( (
				<tr>	
					<td>{ this.props.data.utxos[i].tx_id }</td>
					<td>{ this.props.data.utxos[i].amount }</td>
					<td>{ this.props.data.utxos[i].spendable.toString() }</td>
					<td>{ this.props.data.utxos[i].sending_addrs.join(", ") }</td>
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
							<td>{ this.props.data.balance }</td>
						</tr>
						<tr>
							<th>All Spendable?</th>
							<td>{ this.props.data.all_spendable.toString() }</td>
						</tr>
						<tr>
							<th>Total transactions (current balance only)</th>
							<td>{ this.props.data.total_txs }</td>
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

		return (
			<div>
				{ table }
			</div>
		);
	}
}

