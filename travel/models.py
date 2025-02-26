from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


# Custom User Model
class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('teacher', 'O‘qituvchi'),
        ('student', 'Talaba'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    phone = models.CharField(max_length=20, unique=True)
    profile_image = models.ImageField(upload_to='users/', null=True, blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'full_name']

    def __str__(self):
        return self.username


# Trip Model
class Trip(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    date = models.DateField()
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    @property
    def is_active(self):
        return self.date >= timezone.now().date()

    def __str__(self):
        return f"{self.name} - {self.location} ({'Active' if self.is_active else 'Inactive'})"


# Trip Images
class TripImage(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='trip_images/')


# Attendance Model (Users who registered for a trip)
class Attendance(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='attendees')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    registered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.full_name} registered for {self.trip.name}"


# Impression Model (User Posts after Trip)
class Impression(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='impressions')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='impressions/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# Comments on Impression
class Comment(models.Model):
    impression = models.ForeignKey(Impression, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.full_name} commented on {self.impression.title}"


# Replies to Comments
class Reply(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.full_name} replied to {self.comment.user.full_name}"
