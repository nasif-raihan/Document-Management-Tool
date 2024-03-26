from django.contrib import messages
from django.shortcuts import render
from django.views import View

from ..forms import RegistrationForm


class RegistrationView(View):
    @staticmethod
    def get(request):
        form = RegistrationForm()
        return render(request, "app/registration.html", {"form": form})

    @staticmethod
    def post(request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            messages.success(
                request, message="Congratulations! User is registered successfully."
            )
            form.save()
        return render(request, "app/registration.html", {"form": form})
