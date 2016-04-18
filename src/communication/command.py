import base64
import json
from datetime import datetime

class Command():

	def __init__(self, cmd, args=None):
		print(cmd)

		self.cmd = cmd
		self.date = str(datetime.now())
		self.args = args
		self.keyargs = []

	def validate(self):
		if self.keyargs:
			if not list(self.args) == self.keyargs:
				return False
		return True

	def encode(self):
		if self.args:
			encodedCommand = {'cmd' : self.cmd, 'datetime' : self.date}
		else:
			encodedCommand = {'cmd' : self.cmd, 'datetime' : self.date, 'params' : self.args}
		encodedCommand = json.dumps(encodedCommand)

	#abstract
	def decode(self):
		pass

class Register(Command):

	def __init__(self, cmd, **args):
		print(cmd)
		super().__init__(cmd, args)
		self.keyargs = ['username', 'login']

a = Register('oi', user='name', passwd='1234')
print(a)