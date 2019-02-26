
# known-good imports
from __future__ import print_function

class ModuleNotFound (Exception):
	def __str__ (self):
		return "Could not import required module."
class InvalidAction (Exception):
	def __str__ (self):
		return "Requested action does not exist."

import agents

# dependency imports
try:
	from bs4 import BeautifulSoup
	import requests
	import termcolor
	import mechanize
except Exception:
	raise ModuleNotFound()

# standard library imports
import socket, time
import sys, string, urlparse

# some private variables
__webpage_url = None # string value
__session = requests.Session() 

__default_headers = __session.headers 
__user_agents = agents.all_user_agents

action_options = [
	"1) Dump response headers", 
	"2) Perform stealth port scan",
	"3) Fuzz webpage for input fields",
	"4) Test for any WAF security",
	"5) Attempt to bypass WAF"]

action_modules = [] # fill with functions later

"""NOTE: Please focus on modularity AND THEN optimization."""
def dump_response_headers ():

	try:
		__webpage_url = raw_input('\nwebpage URL> ')
	except KeyboardInterrupt:
		print(termcolor.colored(
			"\n[!] User requested shutdown. Quitting now.", "red"))
		sys.exit(0)

	# use default user agent (python-requests)
	webpage_response = __session.get(__webpage_url, headers=__default_headers)
	webpage_content = str(webpage_response.content)

	# check status code and then dump headers
	if webpage_response.status_code == 200 or 302 and webpage_content:
		print(termcolor.colored(
			"\n[*] Response headers successfully retrieved.","green"))
		for key, value in webpage_response.headers.items():
			print("%s: %s" % (str(key), str(value)))

	elif webpage_response.status_code != 200 or 302:
		print(termcolor.colored(
			"[!] Unsuccessfull HTTP GET/ connection. Check webpage and try again.", "red"))

def stealth_port_scan ():
	# make get request to nmap API and scrape results
	try:
		__webpage_url = raw_input('\nwebpage URL> ')
	except KeyboardInterrupt:
		print(termcolor.colored(
			"\n[!] User requested shutdown. Quitting now.", "red"))
		sys.exit(0)

	bad_components = ['http', 'https', '//', ':', 'www.']
	for component in bad_components:

		if component in __webpage_url: 
			__webpage_url = __webpage_url.replace(
				component, "")

	try:
		nmap_api_response = __session.get('http://api.hackertarget.com/nmap/?q='+__webpage_url)
	except Exception:
		print(termcolor.colored(
			"\n[!] Nmap scan on target webpage seems to have failed.", "red"))

	if 'PORT' and 'SERVICE' in nmap_api_response.content:
		print(nmap_api_response.content)

	elif 'PORT' or 'SERVICE' not in nmap_api_response:
		print(termcolor.colored(
			"\n[!] Nmap scan on target webpage seems to have failed.", "red"))

def fuzz_webpage ():
	# make get request to website and parse markup
	# to find input fields and form data
	try:
		__webpage_url = raw_input('\nwebpage URL> ')
	except KeyboardInterrupt:
		print(termcolor.colored(
			"\n[!] User requesred shutdown. Quitting now.", "red"))
		sys.exit(0)

	try:
		webpage_response = __session.get(__webpage_url, 
			headers=__default_headers)
	except Exception:
		print(termcolor.colored(
			"\n[!] Input-field fuzz operation seems to have failed.", "red"))

	if webpage_response.status_code == 200 or 302:

		# build html parser here
		html_parser = BeautifulSoup(webpage_response.content, 'html.parser')
		fuzzed_forms = html_parser.findAll('form')

		# normalize list of forms into script names
		form_names = {}
		for fuzzed_form in fuzzed_forms:
			form_names[fuzzed_form['action']] = [fuzzed_form['name'], fuzzed_form]
		'''
		for name, form_object in form_names.items():
			print(termcolor.colored("-> %s" % name, "green"))
		'''
		# all user-input fields present in each form
		user_input_fields = {}
		for name, form_object in form_names.items():
			user_input_fields[name] = [form_object[0], form_object[1].findAll('input')]

		# present final fields
		for form, fields in user_input_fields.items():
			print(termcolor.colored("-> ACTION: %s, NAME: %s" % (form,fields[0]), "green"))

			for field in fields[1]: 
				print(termcolor.colored("   %s" % field['name'], "white"))

	elif webpage_response.status_code != 200 or 301:
		print(termcolor.colored(
			"\n[!] Input-field fuzz operation seems to have failed.", "red"))

def test_for_WAF_security ():
	# test a post request to webpage and attempt small injection
	# if denied, then WAF is present
	try:
		__webpage_url = raw_input('\nwebpage URL> ')
		__input_form = raw_input('target form> ')
		__form_field = raw_input('input field> ')

	except KeyboardInterrupt:
		print(termcolor.colored(
			"\n[!] User requesred shutdown. Quitting now.", "red"))
		sys.exit(0)

	test_request = mechanize.Browser()

	test_request.open(__webpage_url)
	test_request.select_form(__input_form)

	test_payload = '<svg><script>alert&grave;1&grave;<p>'
	test_request.form[__form_field] = test_payload

	test_request.submit()
	webpage_response = test_request.response().read()
	print(termcolor.colored(webpage_response, "green"))

# export all module data
action_modules.append(dump_response_headers)
action_modules.append(stealth_port_scan)
action_modules.append(fuzz_webpage)
action_modules.append(test_for_WAF_security)


