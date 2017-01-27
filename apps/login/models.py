from __future__ import unicode_literals
import re
import bcrypt
from django.db import models

NAME_REGEX = re.compile(r'^[a-zA-Z]{3,}$')
PASSWORD_REGEX = re.compile(r'^[a-zA-Z.#!?$+=*]{8,255}')

# Create your models here.
class UserManager(models.Manager):
	"""docstring for UserManager."""
	def login(self, **kwargs):
		errors = []
		username = str(kwargs['username'][0])
		password = str(kwargs['password'][0])
		incorrect = False

		if not NAME_REGEX.match(username):
			incorrect = True
			errors.append('Please insert a valid username.')
		if not PASSWORD_REGEX.match(password):
			incorrect = True
			errors.append('Please insert a valid password.')

		if incorrect:
			return (False, errors)

		try:
			user = User.objects.get(username=username)
		except Exception as e:
			errors.append("I'm sorry, the entered username does not exist.")
			return (False, errors)

		if user.password != bcrypt.hashpw(password, user.password.encode()):
			errors.append('I\'m sorry, the password you entered was wrong.')
			return (False, errors)

		return (True, 'Successful Login', {'id': user.id, 'name' : user.name})




	def register(self, **kwargs):
		errors = []
		username = str(kwargs['username'][0])
		name = str(kwargs['name'][0])
		password = str(kwargs['password'][0])
		confirm = str(kwargs['confirmation'][0])
		incorrect = False

		# Name check
		if not NAME_REGEX.match(name):
			incorrect = True
			errors.append("Please enter a name with only characters and is at least 3 characters long.")


		# Username Check
		if not NAME_REGEX.match(username):
			incorrect = True
			errors.append("Please enter a username with only characters and is at least 3 characters long.")

		# Password Checks
		if not PASSWORD_REGEX.match(password):
			incorrect = True
			errors.append("Please enter a password with 8 or more characters and with valid characters\n [Valid characters are: '.' '#' '!' '?' '+' '=' '*'] ")
		elif not password == confirm:
			incorrect = True
			errors.append("Passwords do not match, try again")

		# Check to see if flag was tripped at all
		if incorrect:
			return (False, errors)

		hashed = bcrypt.hashpw(password, bcrypt.gensalt(14))

		try:
			user = User.objects.create(name=name, password=hashed, username=username)
		except Exception as e:
			errors.append("I'm sorry, there is already a user with that username.")
			return (False, errors)

		return (True, 'Successfully registered!', {'id' : user.id, 'name' : name})


class User(models.Model):
	"""docstring for User."""
	name = models.CharField(max_length=90)
	password = models.CharField(max_length=255)
	username = models.CharField(max_length=50, unique=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = UserManager()
