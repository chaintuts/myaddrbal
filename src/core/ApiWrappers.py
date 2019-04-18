#!/usr/bin/python3

# This file contains abstractions for retrieving UTXO information from the blockchain
# The easiest way to get this information is using a publicly available API
# Multiple APIs could be used to get the standard/common information that the AddressBalInfo
# class will later parse into our desired info
# This ApiWrapper abstraction will allow multiple data sources to be used as desired

import urllib.request, urllib.parse
import json

# ApiWrapper base class
# Each ApiWrapper subclass will make the appropriate API requests and 
# return UTXO info in the following standard format. The idea is that
# most APIs will return this fairly raw transaction/UTXO data, and that
# AddressBalInfo can later parse out the stuff we really want. For example,
# We can't really expect that every API will show the source address of an input,
# but most will show scriptSig. We can parse out the address from the pubkeyHash, etc.
#
# [
#	{
#		"amount" : "Amount in whole currency units (BCH, BTC, etc.)",
#		"tx_id" : "Hash ID of the source transaction"
#		"confirmations" : "Number of confirmations for this tx",
#		"sending_scripts" : [ "scriptSigs", "for", "inputs" ],
#		"script" : "scriptPubKey for output"
#
#	}
# ]

class ApiWrapper:

	pass

# This class defines a wrapper around the Bitcoin.com Bitcoin Cash API
class BchApiWrapper(ApiWrapper):

	def __init__(self):

		self.UTXO_URL = "https://rest.bitcoin.com/v2/address/utxo/"
		self.TX_URL = "https://rest.bitcoin.com/v2/address/transactions/"

	# The public call to get standardized information
	# This function will perform the call to the desired API,
	# It will then parse the information into a standardized format that will
	# be consumed by the AddressBalInfo class
	def get_standard_info(self, address):

		# Perform the API calls
		self.fetch_info(address)

		# Parse the raw information from the API into a standard format
		standard_info = self.parse_info()

		return standard_info

	def fetch_info(self, address):

		try:
			# Create the request URLs with the base and desired address
			url_utxo = urllib.parse.urljoin(self.UTXO_URL, address)
			url_tx = urllib.parse.urljoin(self.TX_URL, address)

			# Create the Request and add a user agent header to avoid 403 Forbidden errors
			req_utxo = urllib.request.Request(url_utxo)
			req_utxo.add_header("User-Agent", "Mozilla/5.0")

			req_tx = urllib.request.Request(url_tx)
			req_tx.add_header("User-Agent", "Mozilla/5.0")

			# Get the JSON response and parse
			response_utxo = urllib.request.urlopen(req_utxo).read()
			self.raw_info_utxo = json.loads(response_utxo.decode("utf-8"))

			response_tx = urllib.request.urlopen(req_tx).read()
			self.raw_info_tx = json.loads(response_tx.decode("utf-8"))

		except urllib.error.HTTPError as e:
			print(e.msg)

	def parse_info(self):

		# Pull out UTXO's and other relevant information and store in a dictionary
		standard_info= []
		for out in self.raw_info_utxo["utxos"]:

			utxo = {}

			# Retrieve basic utxo information from the UTXO results
			utxo["amount"] = out["amount"]
			utxo["tx_id"] = out["txid"]
			utxo["confirmations"] = out["confirmations"]

			# Get further UTXO info we want from the transaction it came from
			raw_txs = self.raw_info_tx["txs"]
			txs = filter(lambda tx : tx["txid"] == utxo["tx_id"], raw_txs)
			tx = list(txs)[0]

			sending_scripts = set([ vin["scriptSig"]["asm"] for vin in tx["vin"] ])
			utxo["sending_scripts"] = list(sending_scripts)

			utxo["script"] = tx["vout"][out["vout"]]["scriptPubKey"]["asm"]

			standard_info.append(utxo)

		return standard_info
