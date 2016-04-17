import base64
import json
from datetime import datetime

class Command():

	def __init__(self, cmd, **args):

		self.cmd = cmd
		self.date = str(datetime.now())
		self.args = args

	#abstract
	def validate(self):
		pass

	#abstract
	def encode(self):
		pass

	#abstract
	def decode(self):
		pass

a = Command('oi', user='name', passwd='1234')