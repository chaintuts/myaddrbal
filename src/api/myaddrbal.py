#!/usr/bin/python3

# This file contains the main entry point for the address balance information web service
#
# Author: Josh McIntyre
#

import web
from AddressBalInfo import AddressBalInfo

# Define important constants
web.config.debug = True

# Define URL handling
urls = (
		"/(.*)/(.*)", "address_info"
	)


# This function is the main entry point for the program
class address_info:

	def GET(self, address, currency):

		web.header("Content-Type", "text/json")

		if not address:
			response = "Please specify an address"
			return response

		if not currency:
			addr = AddressBalInfo(address)
		else:
			addr = AddressBalInfo(address, currency)

		response = addr.get_info()

		return response

if __name__ == "__main__":

	app = web.application(urls, globals())
	app.run()
