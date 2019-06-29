export interface IUTXO 
{
	tx_id: string;
	amount: string;
	spendable: boolean;
	sending_addrs: string[];
}

export interface IAddressData
{
	balance: number;
	all_spendable: boolean;
	total_txs: number;
	utxos: IUTXO[];
}
