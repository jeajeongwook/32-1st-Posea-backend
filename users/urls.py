from django.urls import path
from .views import CheckView, SignUpView, LogInView

urlpatterns = [
    path('/check', CheckView.as_view()),
    path('/signup', SignUpView.as_view()),
    path('/login', LogInView.as_view())
]