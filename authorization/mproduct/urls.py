from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from mproduct.views import *

app_name = "mproduct"

urlpatterns = [
    path("login/",LoginView.as_view(template_name='mproduct/login.html'),name='login'),
    path("logout/",LogoutView.as_view(),name="logout"),
    path("register/",RegisterView.as_view(),name="register"),
    path("settings/",SettingsView.as_view(),name='settings'),
    path("create/brand/",CreateBrand.as_view(),name='create_brand'),
    path("create/plan/",CreatePlan.as_view(),name='create_plan'),
    path("",HomeView.as_view(),name='home'),
    path("plans/",PlansView.as_view(),name='plans'),
    path("planss/",PurchaseView.as_view(),name='purchase'),
    path("purchase/",SubscribeView.as_view(),name='new_purchase'),
    path("search/",search_brands,name='search_brands')
]