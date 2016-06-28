
class User(Object): 
	def __init__(self, name, connection):
		self.name = name
		self.connection = connection
		self.contacts = []  
		self.rooms = []

	def receive_message(self, message):
		self.connection.send_client(message)

	def add_contact(self, contact):
		self.contacts.append(contact);		

	def remove_contact(self, contact):
		self.contacts.remove(contact)

	def login(self, connection):
		self.connection = connection

	def logout(self):
		self.connection = None

	def logged(self):
		return self.connection != None

	def get_contacts(self):
		return self.contacts

	def enter_room(self, room):
		self.rooms.append(room)

	def get_rooms(self):
		return rooms

	def exit_room(self, room):
		self.rooms.remove(room)

