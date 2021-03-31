from . import views
from django.urls import path
urlpatterns = [
    path('register/', views.register),
    path('token/', views.token),
    path('token/refresh_token', views.refresh_token),
    path('token/revoke_token', views.revoke_token),
]
