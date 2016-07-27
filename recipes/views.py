from django.shortcuts import render
from django.http import HttpResponse # DELETE LATER

def home(request):
	return HttpResponse("Testing")

def recipes(request):
	return HttpResponse("Recipes")

def test(request):
	return HttpResponse("test")

