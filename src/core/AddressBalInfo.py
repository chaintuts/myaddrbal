#!/usr/bin/python3

from ApiWrappers import BchApiWrapper
import bitutil
import json

# This class contains code that extracts useful stats for understanding UTXOs
# from a more raw data set that can be retrieved via common blockchain APIs
#
# Some examples:
# Spendability can be determined by the number of confirmations (6+ usually)
# Sending addresses can be gained from the pubKeyHash in the scriptSig
# The script type can be guessed by looking at the scriptPubKey (using a regex pattern)
#
class AddressBalInfo:

	def __init__(self, address):

		# Fetch the desired information from the API, parse, and precompute relevant stats
		self.address = address

		api = BchApiWrapper()
		self.raw_info = api.get_standard_info(self.address)

		# Parse information we want to output from the raw info
		self.parse_info()

	# Take the raw information pulled from the API
	# and parse it into the information we actually want to display
	# This will help make the concept of the UTXO more understandable
	def parse_info(self):

		address_info = {}

		# Parse out core UTXO information
		utxos = []
		for raw in self.raw_info:
			utxo = {}

			utxo["amount"] = raw["amount"]
			utxo["tx_id"] = raw["tx_id"]

			utxo["spendable"] = True if int(raw["confirmations"]) > 6 else False

			sending_addrs = []
			for ssig in raw["sending_scripts"]:
				address = bitutil.address_from_scriptsig(ssig)
				sending_addrs.append(address) 
			utxo["sending_addrs"] = sending_addrs

			utxo["script_type"] = bitutil.get_script_pubkey_type(raw["script"]) 

			utxos.append(utxo)

		# Parse out overall address stats
		balance = 0.00
		all_spendable = True
		transactions = set()
		for utxo in utxos:
			balance += utxo["amount"]
			if utxo["spendable"] == False:
				all_spendable = False
			transactions.add(utxo["tx_id"])

		# Fill in the address information dictionary
		address_info["utxos"] = utxos
		address_info["balance"] = balance
		address_info["all_spendable"] = all_spendable
		address_info["total_txs"] = len(transactions)

		# Store this info in the object
		self.address_info = address_info

	# Return the parsed information
	def get_info(self):

		return json.dumps(self.address_info)
