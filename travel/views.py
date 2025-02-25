from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import Trip, Impression, Comment
from .forms import UserLoginForm, TripForm, ImpressionForm, CommentForm


# User Login View
def user_login(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('trip_list')
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})


# User Logout View
def user_logout(request):
    logout(request)
    return redirect('login')


# Trip List View
@login_required
def trip_list(request):
    trips = Trip.objects.filter(created_by=request.user)
    return render(request, 'trip_list.html', {'trips': trips})


# Trip Create View
@login_required
def trip_create(request):
    if request.method == "POST":
        form = TripForm(request.POST)
        if form.is_valid():
            trip = form.save(commit=False)
            trip.created_by = request.user
            trip.save()
            return redirect('trip_list')
    else:
        form = TripForm()
    return render(request, 'trip_form.html', {'form': form})


# Impression Create View
@login_required
def impression_create(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id)
    if request.method == "POST":
        form = ImpressionForm(request.POST, request.FILES)
        if form.is_valid():
            impression = form.save(commit=False)
            impression.user = request.user
            impression.trip = trip
            impression.save()
            return redirect('trip_list')
    else:
        form = ImpressionForm()
    return render(request, 'impression_form.html', {'form': form})


# Comment Create View
@login_required
def comment_create(request, impression_id):
    impression = get_object_or_404(Impression, id=impression_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.impression = impression
            comment.save()
            return redirect('trip_list')
    else:
        form = CommentForm()
    return render(request, 'comment_form.html', {'form': form})
