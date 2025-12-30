from django.urls import path
from .views import register, login_view, dashboard, logout_view, view_payee_info
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path("register/", register, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    #path("logout/", LogoutView.as_view(next_page="login"), name="logout"),
    path("dashboard/", dashboard, name="dashboard"),
    path("payee_info/", view_payee_info, name="payee_info"),
]
