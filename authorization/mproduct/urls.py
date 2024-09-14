from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from mproduct.views import *

app_name = "mproduct"

urlpatterns = [
    path("",HomeView.as_view(),name='home'),
    path("login/",LoginView.as_view(template_name='mproduct/login.html'),name='login'),
    path("logout/",LogoutView.as_view(),name="logout"),
    path("register/",RegisterView.as_view(),name="register"),
    path("<str:company>/",DashboardView.as_view(),name='dashboard'),
    path("settings/",SettingsView.as_view(),name='settings'),
    path("create/Company/",CreateCompany.as_view(),name='create_Company'),
    path("create/plan/",CreatePlan.as_view(),name='create_plan'),
    # path("subscription/",SubscriptionView.as_view(),name='subscription'),
    # path("subscribers/",SubscribersView.as_view(),name='subscribers'),
    # path("subscription/status/<int:pk>/",SubscriptionStatusView.as_view(),name='status'),
    path("plans/",PlansView.as_view(),name='plans'),
    path("plans/<int:pk>/",CompanyPlansView.as_view(),name='Company_plans'),
    # path("purchase/",SubscribeView.as_view(),name='new_purchase'),
    path("search/",search_Companys,name='search_Companys'),
    path("<str:Company>/<str:BusinessUnit>/register/",EmployeeRegisterView.as_view(),name="employee_register"),
    path("<str:Company>/dashboard/",DashboardView.as_view(),name="dashboard"),
    path("invite/email/",InviteEmailView.as_view(),name='invite_email'),
]