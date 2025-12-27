from django.shortcuts import render, redirect

# Create your views here.

def index(request):
    #return render(request, "base.html")
    return redirect("login")
