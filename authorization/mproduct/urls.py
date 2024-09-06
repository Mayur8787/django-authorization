from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from mproduct.views import *

app_name = "mproduct"

urlpatterns = [
    path("login/",LoginView.as_view(template_name='mproduct/login.html'),name='login'),
    path("logout/",LogoutView.as_view(),name="logout"),
    path("register/",RegisterView.as_view(),name="register"),
    path("",LandingPageView.as_view(),name='home'),
    path("plans/",PurchaseView.as_view(),name='purchase'),
    path("search/",search_brands,name='search_brands')
]