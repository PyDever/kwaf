

"""
entry point main (control script)
"""

# known-good imports
from __future__ import print_function

class ModuleNotFound (Exception):
	def __str__ (self):
		return "Could not import required module."
class InvalidAction (Exception):
	def __str__ (self):
		return "Requested action does not exist."

from core import action_modules, action_options
"""display kwaf banner"""
# do this later

"""present opening options"""
def main ():

	for action in action_options:
		print(action)
	try:
		action_choice = raw_input('action> ')
		#try:
		action_modules[int(action_choice)-1]()
		'''
		except Exception:
			raise InvalidAction()
		'''
	except KeyboardInterrupt:
		print(termcolor.colored(
			"\n[!] User requested shutdown. Quitting now.", "red"))
		sys.exit(0)

if __name__ == '__main__':
	main()

