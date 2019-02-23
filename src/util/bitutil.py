# This file contains utility code for parsing UTXO information
#
# Author: Josh McIntyre
#

import base58
import binascii
import hashlib
import re

# This helper function gets an address from a scriptSig
def address_from_scriptsig(script_sig):

	# Get the pubkey from the scriptSig
	ascii_pubkey = script_sig.split(" ")[1]

	# Convert to byte objects
	pubkey = binascii.unhexlify(ascii_pubkey)
	version = binascii.unhexlify("00")

	# Compute necessary hashes
	first = hashlib.sha256(pubkey).digest()
	ripemd = hashlib.new("ripemd160")
	ripemd.update(first)
	pubkey_hash = ripemd.digest()

	checksum = hashlib.sha256(hashlib.sha256(version + pubkey_hash).digest()).digest()[:4]

	# Generate the adress
	address = base58.b58encode(version + pubkey_hash + checksum).decode("utf-8")

	return address

# This helper function detects common scriptPubKey patterns
# and returns a string with the script type
def get_script_pubkey_type(script_pubkey):

	script_types = { "Pay to Public Key Hash" :  "OP_DUP OP_HASH160 [0-9a-fA-F]+ OP_EQUALVERIFY OP_CHECKSIG" }

	script_pubkey_type = "unknown"
	for stype, regex in script_types.items():
		if re.match(regex, script_pubkey):
			script_pubkey_type = stype
 
	return script_pubkey_type
