class Person:
	def __init__(self, age=25, gender=None,
                 height=1.7, weight=65):
		self._age = age
		self._gender = gender
		self._height = height
		self._weight = weight
		self._friends = []
		self._relatives = []
		if self._gender is None:
			print("Gender hasn’t been provided")

	def add_friend(self, friend):
		self._friends.append(friend)

	def add_relative(self, relative):
		self._relatives.append(relative)

	def get_friend_info(self, friend):
		if friend in self._friends:
			print(f"age: {friend._age}")
			print(f"gender: {friend._gender}")
			print(f"height: {friend._height}")
			print(f"weight: {friend._weight}")
		else:
			print("this is not a friend")

	def get_relative_info(self, relative):
		if relative in self._relatives:
			print(f"age: {relative._age}")
			print(f"gender: {relative._gender}")
			print(f"height: {relative._height}")
			print(f"weight: {relative._weight}")
		else:
			print("this is not a relative")


class Employee(Person):
	def __init__(self, age=25, gender=None, height=1.7,
                 weight=65, firm=None):
		super().__init__(age, gender, height, weight)
		self._firm = firm
		self._post = None

	def add_post(self, post):
		self._post = post

	def get_post(self):
		if self._post is not None:
			print(f"this employee’s post is {self._post}")
		else:
			print("this employee doesn’t have a post yet")


class Student(Person):
	def __init__(self, age=25, gender=None, height=1.7,
                 weight=65, school=None):
		super().__init__(age, gender, height, weight)
		self._school = school
		self._grades = {}

	def set_grades(self, semester, grade):
		self._grades[semester] = grade

	def get_grades(self, semester):
		if semester not in self._grades.keys():
			print(f"grade for {semester} semester \
                    has not been provided")
		else:
			print(f"{semester} grade: \
                    {self._grades[semester]}")


jane = Student(age=15,gender="f",height=1.6,
               weight=50,school="Freedonia High")
john = Employee(age=34,gender="m",height=1.75,
                weight=71,firm="Freedo Realty")

jane.add_relative(john)
print("info of relative john:")
jane.get_relative_info(john)
