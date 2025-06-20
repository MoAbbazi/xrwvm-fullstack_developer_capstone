import json
import logging
from datetime import datetime

from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

from .models import CarMake, CarModel
from .populate import initiate  # ✅ import populate script if available

logger = logging.getLogger(__name__)

# --- Authentication Views ---

@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('userName')
        password = data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({"userName": username, "status": "Authenticated"}, status=200)
        else:
            return JsonResponse({"error": "Invalid credentials"}, status=401)
    return JsonResponse({"error": "Only POST allowed"}, status=405)

@csrf_exempt
def logout_request(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({"status": "Logged out"}, status=200)
    return JsonResponse({"error": "Only POST allowed"}, status=405)

@csrf_exempt
def registration(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('userName')
        password = data.get('password')
        first = data.get('firstName')
        last = data.get('lastName')
        email = data.get('email')
        if User.objects.filter(username=username).exists():
            return JsonResponse({"userName": username, "error": "Already Registered"}, status=409)
        user = User.objects.create_user(username=username, password=password,
                                        first_name=first, last_name=last, email=email)
        login(request, user)
        return JsonResponse({"userName": username, "status": "Authenticated"}, status=201)
    return JsonResponse({"error": "Only POST allowed"}, status=405)

# --- Dealership / Reviews Views (placeholders) ---

def get_dealerships(request):
    return JsonResponse({"message": "get_dealerships - Not implemented yet"}, status=501)

def get_dealer_reviews(request, dealer_id):
    return JsonResponse({"message": f"get_dealer_reviews({dealer_id}) - Not implemented yet"}, status=501)

def get_dealer_details(request, dealer_id):
    return JsonResponse({"message": f"get_dealer_details({dealer_id}) - Not implemented yet"}, status=501)

@csrf_exempt
def add_review(request):
    if request.method == 'POST':
        return JsonResponse({"message": "add_review - Not implemented yet"}, status=501)
    return JsonResponse({"error": "Only POST allowed"}, status=405)

# --- Car Models Endpoint ---

def get_cars(request):
    count = CarMake.objects.count()
    logger.info(f"CarMake count: {count}")
    if count == 0:
        try:
            initiate()
        except Exception as e:
            logger.warning(f"initiate() failed: {e}")
    car_models = CarModel.objects.select_related('car_make')
    cars = []
    for car_model in car_models:
        cars.append({
            "CarModel": car_model.name,
            "CarMake": car_model.car_make.name,
            "Year": car_model.year,
            "Type": car_model.type
        })
    return JsonResponse({"CarModels": cars})
