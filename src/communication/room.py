class Room(): 
	def __init__(self, admin_name, room_name):
		self.name = room_name
		self.users = []
		self.admin = admin_name

	def get_usernames(self):
		usernames = []
		for user in users:
			usernames.append(user.name)
		return usernames

	def add_user(self, user):
		self.users.append(user)

	def broadcast_message(self, message):
		for user in users:
			if user.logged():
				connection.receive_message(message)

	def change_admin(self, new_admin):
		admin = new_admin.name