from django.urls import path
from .views import *

urlpatterns = [
    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('organizations', ListOrganizationsView.as_view()),
    path('todos', ListToDosView.as_view()),
]