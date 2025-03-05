from django.urls import path
from travel import views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('trips/', views.trip_list, name='trip_list'),
    path('create-trip/', views.create_trip, name='create_trip'),
    path('user-search/', views.user_search, name='user_search'),
    path('trip/<int:trip_id>/attendance/', views.trip_attendance, name='trip_attendance'),
    path('trips/<int:trip_id>/', views.trip_detail, name='trip_detail'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('trips/create/', views.trip_create, name='trip_create'),
    path('trips/<int:trip_id>/impressions/create/', views.impression_create, name='impression_create'),
    path('impressions/<int:impression_id>/comments/create/', views.comment_create, name='comment_create'),
]
