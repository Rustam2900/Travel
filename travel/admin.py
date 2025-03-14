from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from travel.models import CustomUser, Trip, TripImage, Attendance, Impression, Comment, Reply, BirthdayGreeting


# Custom User Admin
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'full_name', 'email', 'role', 'phone', 'is_active', 'is_staff')
    search_fields = ('username', 'full_name', 'email', 'phone')
    list_filter = ('role', 'is_active', 'is_staff')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('full_name', 'email', 'role', 'age', 'phone', 'profile_image')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )


# Trip Admin
@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'location', 'date', 'created_by')
    search_fields = ('id', 'name', 'location', 'created_by__username')
    list_filter = ('date',)


@admin.register(BirthdayGreeting)
class BirthdayGreetingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'sender', 'message', 'image', 'created_at')
    search_fields = ('id', 'message', 'created_at')
    list_filter = ('created_at',)


# Trip Image Admin
@admin.register(TripImage)
class TripImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'trip', 'image')


# Attendance Admin
@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'trip', 'user', 'registered_at')
    search_fields = ('trip__name', 'user__username')


# Impression Admin
@admin.register(Impression)
class ImpressionAdmin(admin.ModelAdmin):
    list_display = ('id', 'trip', 'user', 'title', 'created_at')
    search_fields = ('trip__name', 'user__username', 'title')
    list_filter = ('created_at',)


# Comment Admin
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'impression', 'user', 'text', 'created_at', 'likes')
    search_fields = ('impression__title', 'user__username', 'text')


# Reply Admin
@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ('id', 'comment', 'user', 'text', 'created_at')
    search_fields = ('comment__text', 'user__username', 'text')
