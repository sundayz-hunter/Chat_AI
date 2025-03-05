from django.urls import path

from user.views import SignupView, CustomLoginView, logout_view

app_name = 'user'

urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", logout_view, name="logout"),
]