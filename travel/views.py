from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.utils.timezone import now, timedelta
from django.http import JsonResponse, HttpResponse
from datetime import date

from travel.models import Trip, Impression, Attendance, CustomUser, BirthdayGreeting
from travel.forms import UserLoginForm, TripForm, ImpressionForm, CommentForm, CustomUserForm, BirthdayGreetingForm


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


@login_required
def trip_list(request):
    trips = Trip.objects.all()
    return render(request, 'trip_list.html', {'trips': trips})


@login_required
def trip_detail(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id)
    attendees = Attendance.objects.filter(trip=trip).select_related('user')

    return render(request, 'trip_detail.html', {
        'trip': trip,
        'attendees': attendees
    })


@login_required
def profile_view(request):
    user = request.user
    trips = Trip.objects.filter(created_by=user)

    upcoming_trips = trips.filter(date__gte=timezone.now().date())
    past_trips = trips.filter(date__lt=timezone.now().date())

    context = {
        'user': user,
        'upcoming_trips': upcoming_trips,
        'past_trips': past_trips,
    }
    return render(request, 'profile.html', context)


@login_required
def profile_edit(request):
    user = request.user
    if request.method == 'POST':
        form = CustomUserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = CustomUserForm(instance=user)

    return render(request, 'profile_edit.html', {'form': form})


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


@login_required
def create_trip(request):
    if request.method == "POST":
        form = TripForm(request.POST)
        if form.is_valid():
            trip = form.save(commit=False)
            trip.created_by = request.user
            trip.save()
            return redirect('trip_attendance', trip_id=trip.id)
    else:
        form = TripForm()
        form.fields['date'].widget.attrs['min'] = (now() + timedelta(days=1)).date()

    return render(request, 'create_trip.html', {'form': form})


def user_search(request):
    query = request.GET.get('query', '').strip()
    if not query:
        users = CustomUser.objects.all()[:10]
    else:
        users = CustomUser.objects.filter(username__icontains=query)[:10]

    return JsonResponse({"users": list(users.values("id", "username", "full_name"))})


@login_required
def trip_attendance(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id)
    users = CustomUser.objects.all()

    if request.method == "POST":
        selected_user_ids = request.POST.getlist('users')
        for user_id in selected_user_ids:
            user = CustomUser.objects.get(id=user_id)
            Attendance.objects.get_or_create(trip=trip, user=user)
        return redirect('profile')

    return render(request, 'trip_attendance.html', {'users': users, 'trip': trip})


def past_trips(request):
    trips = Trip.objects.filter(date__lt=date.today())
    return render(request, 'past_trips.html', {'trips': trips})


def birthday_greeting_view(request):
    if request.method == "POST":
        form = BirthdayGreetingForm(request.POST, request.FILES)
        if form.is_valid():
            greeting = form.save(commit=False)  # Avval commit qilmaymiz
            if request.user.is_authenticated:  # Foydalanuvchi tizimga kirganmi?
                greeting.sender = request.user  # `sender` maydoniga foydalanuvchini qo‘shamiz
            else:
                return HttpResponse("Siz tizimga kirmagansiz!", status=403)
            greeting.save()
            return redirect("trip_list")  # Muvaffaqiyatli saqlangandan keyin yo‘naltirish
    else:
        form = BirthdayGreetingForm()

    return render(request, "send_greeting.html", {"form": form})


def birthday_greetings_list(request):
    greetings = BirthdayGreeting.objects.all().order_by('-created_at')  # Eng oxirgi tabriklar yuqorida bo'ladi
    return render(request, 'greetings_list.html', {'greetings': greetings})


def birthday_greeting_detail(request, greeting_id):
    greeting = get_object_or_404(BirthdayGreeting, id=greeting_id)
    return render(request, 'greeting_detail.html', {'greeting': greeting})
