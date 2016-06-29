from datetime import datetime

from communication.communication_protocol import Message

class MessageManager():

	def __init__(self):
		self.pending_messages = {}

	def has_pending_msg(self, to):
		if to in self.pending_messages:
			return True
		else:
			return False

	def get_msg(self, to):
		if to in self.pending_messages:
			return self.pending_messages[to]
		else:
			return None

	def add_pending(self, fromuser, to, msg):
		date = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))	
		self.pending_messages[to] = {'msg' : msg, 'date' : date}
		return Message(to=to, fromuser=fromuser, window=fromuser, date=date, msg=msg)

	def remove_pending(self, to):
		del self.pending_messages[to]