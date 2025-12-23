
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import PayeeRegistrationForm

def register(request):
    form = PayeeRegistrationForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(form.cleaned_data["password"])
        user.save()
        form.save_m2m()
        return redirect("login")
    return render(request, "accounts/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        id_number = request.POST["id_number"]
        phone = request.POST["phone"]
        password = request.POST["password"]

        user = authenticate(
            request,
            username=id_number,
            password=password,
            phone=phone
        )
        if user:
            login(request, user)
            return redirect("dashboard")

    return render(request, "accounts/login.html")
