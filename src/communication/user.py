
class User(): 
	def __init__(self, name, password):
		self.name = name
		self.password = password
		self.uid = None
		self.connection = None
		self.contacts = []  
		self.rooms = []

	def password_matchs(self, password):
		return self.password == password

	def login(self, uid, connection):
		self.uid = uid
		self.connection = connection

	def logout(self):
		self.uid = None
		self.connection = None

	def logged(self):
		return self.connection != None

	def receive_message(self, message):
		self.connection.send_client(message)

	def add_contact(self, contact):
		self.contacts.append(contact);		

	def remove_contact(self, contact):
		self.contacts.remove(contact)

	def get_contacts(self):
		return self.contacts

	def enter_room(self, room):
		self.rooms.append(room)

	def exit_room(self, room):
		self.rooms.remove(room)

	def get_rooms(self):
		return rooms
