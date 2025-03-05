from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from user.forms import CustomSignupForm, CustomLoginForm

User = get_user_model()


class SignupView(CreateView):
    form_class = CustomSignupForm
    template_name = "user/signup.html"
    success_url = reverse_lazy("chat:chat_list")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.success_url)


class CustomLoginView(LoginView):
    authentication_form = CustomLoginForm
    template_name = "user/login.html"


def logout_view(request):
    logout(request)
    return redirect("user:login")
