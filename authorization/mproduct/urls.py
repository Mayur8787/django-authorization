from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from mproduct.views import *

app_name = "mproduct"

urlpatterns = [
    path("",HomeView.as_view(),name='home'),
    path("login/",LoginView.as_view(template_name='mproduct/login.html'),name='login'),
    path("logout/",LogoutView.as_view(),name="logout"),
    path("register/",RegisterView.as_view(),name="register"),
    path("settings/",SettingsView.as_view(),name='settings'),
    path("create/brand/",CreateBrand.as_view(),name='create_brand'),
    path("create/plan/",CreatePlan.as_view(),name='create_plan'),
    path("subscription/",SubscriptionView.as_view(),name='subscription'),
    path("subscribers/",SubscribersView.as_view(),name='subscribers'),
    path("subscription/status/<int:pk>/",SubscriptionStatusView.as_view(),name='status'),
    path("plans/",PlansView.as_view(),name='plans'),
    path("plans/<int:pk>/",BrandPlansView.as_view(),name='brand_plans'),
    path("purchase/",SubscribeView.as_view(),name='new_purchase'),
    path("search/",search_brands,name='search_brands')
]