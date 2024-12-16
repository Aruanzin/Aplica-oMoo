from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('home/', views.home_view, name='home'),
    path('request_appointment/', views.request_appointment_view, name='request_appointment'),
    path('manage_appointments/', views.manage_appointments_view, name='manage_appointments'),
    path('accept_appointment/<int:appointment_id>/', views.accept_appointment_view, name='accept_appointment'),
    path('reject_appointment/<int:appointment_id>/', views.reject_appointment_view, name='reject_appointment'),
    path('view_appointments/', views.view_appointments, name='view_appointments'),
    path('get_available_times/', views.get_available_times, name='get_available_times'),
    path('manage_schedule/', views.manage_schedule_view, name='manage_schedule'),
    path('toggle_schedule/<int:schedule_id>/', views.toggle_schedule_view, name='toggle_schedule'),
    path('configure/', views.configure_user_view, name='configure_user'),
    path('reset-password/', views.reset_password_view, name='reset_password'),
]