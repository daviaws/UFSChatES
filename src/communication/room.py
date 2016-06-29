class Room(): 
	def __init__(self, admin_name, room_name):
		self.name = room_name
		self.users = []
		self.admin = admin_name

	def get_usernames(self):
		usernames = []
		for user in self.users:
			usernames.append(user.name)
		return usernames

	def add_user(self, user):
		self.users.append(user)

	def remove_user(self, user):
		self.users.remove(user)

	def broadcast_message(self, message):
		for user in self.users:
			if user.logged():
				user.connection.receive_message(message)

	def change_admin(self, new_admin):
		self.admin = new_admin.name
