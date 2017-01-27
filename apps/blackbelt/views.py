from django.shortcuts import redirect
from django.urls import reverse

# Create your views here.
def entry(request):
	return redirect(reverse('login:index'))
