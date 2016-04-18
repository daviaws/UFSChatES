import base64
import json
from datetime import datetime
from copy import deepcopy

class Protocol():

	def encode(self, cmd):
		cmd_name = type(cmd).__name__
		date = str(datetime.now())
		if cmd.has_args():
			encodedCommand = {'cmd' : cmd_name, 'datetime' : date}
		else:
			encodedCommand = {'cmd' : cmd_name, 'datetime' : date, 'params' : cmd.get_args}
		encodedCommand = json.dumps(encodedCommand)
		encodedCommand = encodedCommand.encode('ascii')
		encodedCommand = base64.b64encode(encodedCommand)
		return encodedCommand

class Command():

	def __init__(self, args=None):
		self.args = args
		self.keyargs = []

	def has_args(self):
		if self.args:
			return True
		return False

	def get_args(self):
		return deepcopy(args)

	def validate(self):
		if self.keyargs:
			if not list(self.args) == self.keyargs:
				return False
		return True

class Register(Command):
	
	def __init__(self, **args):
		super().__init__(args)
		self.keyargs = ['username', 'passwd']
