from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from .models import Trip, User_Trip
from ..login.models import User

# Create your views here.
def index(request):
	user_trips = User_Trip.objects.filter(attendee_id=request.session['id'])
	other_trips = Trip.objects.exclude(owner_id=request.session['id'])
	for trip in user_trips:
		other_trips = other_trips.exclude(id=trip.trip.id)

	context = {
		'other_trips': other_trips,
		'user_trips': user_trips
	}

	return render(request, 'travels/index.html', context)


def show_add(request):
	return render(request, 'travels/add.html')


def show_trip(request, id):
	trip = Trip.objects.get(id=id)
	context = {
		'trip_attendees': User_Trip.objects.filter(trip=trip),
		'trip' : trip
	}
	print trip.destination
	print context['trip_attendees']
	return render(request, 'travels/trip.html', context)


def create(request, id):
	response = Trip.objects.validate(id, **request.POST)
	if not response[0]:
		print response[0]
		for message in response[1]:
			messages.error(request, message)
		return redirect(reverse('travel:show_add'))
	else:
		print response[1]
		messages.success(request, response[1])
	return redirect(reverse('travel:index'))

def join(request, id):
	User_Trip.objects.create(attendee=User.objects.get(id=request.session['id']), trip=Trip.objects.get(id=id))
	return redirect(reverse('travel:index'))
