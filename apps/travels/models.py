from __future__ import unicode_literals
from datetime import datetime
import re
from django.db import models
from ..login.models import User

DESTINATION_REGEX = re.compile(r'^[a-zA-Z\'\". ]{5,}$')

# Create Model Managers
class TripManager(models.Manager):
	"""docstring for TripManager."""
	def validate(self, id, **kwargs):
		incorrect = False
		errors = []
		# Collect error free values from kwargs and validate
		destination = str(kwargs['destination'][0])
		description = str(kwargs['description'][0])

		print incorrect
		# Destination Null check
		if not DESTINATION_REGEX.match(destination):
			incorrect = True
			errors.append('Please enter a destination for your trip.')
		# Description Null check
		if description and len(description) < 10:
			incorrect = True
			errors.append("If you're going to enter a description, make sure that You enter one at least 10 characters long.")

		print incorrect, 'before tries'
		# Collect error prone values from kwargs and validate
		try:
			travel_to = datetime.strptime(str(kwargs['travel_to'][0]), '%d %B, %Y')
		except Exception as e:
			incorrect = True
			errors.append("Please enter a value for 'Travel To'")

		try:
			travel_from = datetime.strptime(str(kwargs['travel_from'][0]), '%d %B, %Y')
		except Exception as e:
			incorrect = True
			errors.append("Please enter a value for 'Travel From'")

		print incorrect, 'before tries'
		try:
			delta = travel_to - travel_from
			if delta.days < 0:
				incorrect = True
				errors.append("The 'Travel To' date must be further in the future than the travel from date.")
		except Exception as e:
			print e

		if incorrect:
			return (False, errors)

		try:
			user = User.objects.get(id=id)
		except Exception as e:
			errors.append("You somehow managed to get to this page without signing in. Go back home and sign in!")
			return (False, errors)

		trip = Trip.objects.create(destination=destination, description=description, owner=user, travel_from=travel_from, travel_to=travel_to)

		message = 'Created trip to '+ destination + '!'
		return (True, message)


# Create your models here.
class Trip(models.Model):
	"""docstring for Trip."""
	destination = models.CharField(max_length=45)
	description = models.TextField(max_length=1000)
	owner = models.ForeignKey(User)
	travel_from = models.DateTimeField()
	travel_to = models.DateTimeField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = TripManager()


class User_Trip(models.Model):
	"""docstring for User_Trip."""
	attendee = models.ForeignKey(User)
	trip = models.ForeignKey(Trip)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
