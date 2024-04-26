class Person:
	def __init__(self,age=25,gender=None,
                 height=1.7,weight=65):
		self._age = age
		self._gender = gender
		self._height = height
		self._weight = weight
		self._friends  = []
		if self._gender is None:
			print("Gender hasn’t been provided!")

	def add_friend(self, friend):
		self._friends.append(friend)

	def get_friend_info(self, friend):
		if friend in self._friends:
			print(f"age: {friend._age}")
			print(f"gender: {friend._gender}")
			print(f"height: {friend._height}")
			print(f"weight: {friend._weight}")
		else:
			print("this is not a friend")

jane = Person(age=30, gender="f", height=1.65, weight=58)
john = Person(age=24, gender="m", height=1.75, weight=71)
jack = Person(age=40, gender="m", height=1.8, weight=78)

jane.add_friend(john)
print("info of friend john:")
jane.get_friend_info(john)
print()
print("info of friend jack:")
jane.get_friend_info(jack)
