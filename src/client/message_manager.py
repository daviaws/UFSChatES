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

	def add_pending(self, to, msg, date):
		self.pending_messages[to] = {'msg' : msg, 'date' : date}

	def remove_pending(self, to):
		del self.pending_messages[to]