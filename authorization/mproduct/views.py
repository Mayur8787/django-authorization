from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from mproduct.forms import UserRegisterForm
from django.contrib.auth.models import User
from django.views.generic import CreateView, TemplateView, ListView, UpdateView, View
from mproduct.models import Plans, Company, BusinessUnit, Employee, Requests, Subscriber
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET
from django.http import HttpRequest, HttpResponse, JsonResponse, Http404
import datetime
# Create your views here.

class RegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = "mproduct/register.html"
    success_url = reverse_lazy("mproduct:login")

class HomeView(TemplateView):
    template_name = 'mproduct/home.html'

    def get_context_data(self, **kwargs: reverse_lazy):
        context = super().get_context_data(**kwargs)
        context['is_authenticated'] = self.request.user.is_authenticated
        context['is_authorized'] = False
        # context['is_authorized'] = Subscribers.objects.filter(name=self.request.user,subscription_status=True).exists() if context['is_authenticated'] else False
        context['is_Company'] = Company.objects.filter(owner=self.request.user).exists() if context['is_authorized'] else False
        context['title'] = 'Home'
        print("---------->",context)
        return context


class DashboardView(LoginRequiredMixin,TemplateView):
    login_url = 'mproduct:login'
    template_name = 'mproduct/dashboard.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Dashboard'
        context['user'] = self.request.user
        context['company'] = Subscriber.objects.filter(user=self.request.user).first()
        context['is_authorized'] = True
        context['is_authenticated'] = self.request.user.is_authenticated
        # context['is_authorized'] = Subscribers.objects.filter(name=self.request.user,subscription_status=True).exists() if context['is_authenticated'] else False
        context['is_Company'] = Company.objects.filter(owner=self.request.user).exists() if context['is_authorized'] else False
        print("->>>>>>>",context)
        return context


class InviteEmailView(LoginRequiredMixin,TemplateView):
    login_url = 'mproduct:login'
    template_name = 'mproduct/invite_email.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Dashboard'
        context['user'] = self.request.user
        context['company'] = Subscriber.objects.filter(user=self.request.user).first()
        context['is_authorized'] = True
        context['is_authenticated'] = self.request.user.is_authenticated
        # context['is_authorized'] = Subscribers.objects.filter(name=self.request.user,subscription_status=True).exists() if context['is_authenticated'] else False
        context['is_Company'] = Company.objects.filter(owner=self.request.user).exists() if context['is_authorized'] else False
        print("->>>>>>>",context)
        return context


class PlansView(LoginRequiredMixin,ListView):
    model = Plans
    template_name = 'mproduct/plans.html'
    context_object_name = 'plans'
    login_url = 'mproduct:login'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(Company=get_object_or_404(Company,name='mproduct'))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_authenticated'] = self.request.user.is_authenticated
        context['title'] = 'Plans'
        return context

class CompanyPlansView(LoginRequiredMixin,ListView):
    model = Plans
    template_name = 'mproduct/plans.html'
    context_object_name = 'plans'
    login_url = 'mproduct:login'

    def get_queryset(self):
        Company = Company.objects.get(pk=self.kwargs.get('pk'))
        queryset = super().get_queryset()
        return queryset.filter(Company=Company)

# class SubscribeView(LoginRequiredMixin,View):
#     login_url = 'mproduct:login'

#     def post(self,request,*args,**kwargs):
#         plan_id = request.POST.get('plan_id')
#         plan = get_object_or_404(Plans, id=plan_id)
#         name = request.user
#         date = timezone.now().date()
#         status = True
#         Subscribers.objects.create(name=name,plan=plan,purchased_on=date,subscription_status=status)
#         return redirect('mproduct:home')

class CreateCompany(LoginRequiredMixin,CreateView):
    login_url = 'mproduct:login'
    model = Company
    template_name = 'mproduct/settings.html'
    fields = ['name']
    success_url = reverse_lazy('mproduct:settings')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class CreatePlan(LoginRequiredMixin,CreateView):
    login_url = 'mproduct:login'
    model = Plans
    template_name = 'mproduct/settings.html'
    fields = ['name','description','price','duration']
    success_url = reverse_lazy('mproduct:settings')

    def form_valid(self, form):
        Company = Company.objects.get(owner=self.request.user)
        print("------------->Company",Company)
        form.instance.Company = Company
        return super().form_valid(form)


class SettingsView(LoginRequiredMixin,TemplateView):
    login_url = 'mproduct:login'
    template_name = 'mproduct/settings.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_authenticated'] = self.request.user.is_authenticated
        context['profile'] = get_object_or_404(User,username=self.request.user)
        # context['is_authorized'] = Subscribers.objects.filter(name=self.request.user,subscription_status=True).exists()
        context['title'] = 'Settings'
        if context['is_authorized']:
            context['is_Company'] = Company.objects.filter(owner=self.request.user).exists()
        else:
            context['is_Company'] = False
        if context['is_Company']:
            context['Company'] = Company.objects.get(owner=self.request.user)
            if Plans.objects.filter(Company=context['Company']).count() < 3:
                context['create_plans'] = True
            else:
                context['create_plans'] = False
            context['plans'] = Plans.objects.filter(Company=context['Company'])
        else:
            context['Company'] = False
        context['requests'] = Requests.objects.filter(receiver=self.request.user)
        print("------------->",context)
        return context


# class SubscriptionView(LoginRequiredMixin,ListView):
#     model = Subscribers
#     template_name = 'mproduct/subscription.html'
#     context_object_name = 'subscriptions'
#     login_url = 'mproduct:login'

#     def get_queryset(self) -> QuerySet[reverse_lazy]:
#         queryset = super().get_queryset()
#         return queryset.filter(name=self.request.user)
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['is_authenticated'] = self.request.user.is_authenticated
#         context['is_authorized'] = Subscribers.objects.filter(name=self.request.user,subscription_status=True).exists()
#         context['is_Company'] = Company.objects.filter(owner=self.request.user).exists()
#         context['title'] = 'Subscriptions'
#         return context

# class SubscribersView(LoginRequiredMixin,ListView):
#     model = Subscribers
#     template_name = 'mproduct/subscribers.html'
#     context_object_name = 'subscribers'
#     login_url = 'mproduct:login'

#     def get_queryset(self) -> QuerySet[reverse_lazy]:
#         queryset = super().get_queryset()
#         if Company.objects.filter(owner=self.request.user).exists():
#             Company = Company.objects.get(owner=self.request.user)
#             return queryset.filter(plan__Company=Company)
#         return queryset.none()
    
#     def get_context_data(self, **kwargs: reverse_lazy) :
#         context = super().get_context_data(**kwargs)
#         context['is_authenticated'] = self.request.user.is_authenticated
#         context['is_authorized'] = Subscribers.objects.filter(name=self.request.user,subscription_status=True).exists()
#         context['is_Company'] = Company.objects.filter(owner=self.request.user).exists()
#         context['title'] = 'Subscribers'
#         return context

# class SubscriptionStatusView(LoginRequiredMixin,UpdateView):
#     login_url = 'mproduct:login'
#     model = Subscribers
#     fields = []
#     success_url = reverse_lazy('mproduct:subscribers')

#     def form_valid(self, form):
#         subscriber = form.instance
#         end_date = subscriber.purchased_on + timezone.timedelta(days=subscriber.plan.duration)
#         if end_date > timezone.now().date():
#             subscriber.subscription_status = not subscriber.subscription_status
#         subscriber.save()
#         return super().form_valid(form)

@require_GET
def search_Companys(request):
    query = request.GET.get('data','')
    if query:
        Companys = Company.objects.filter(name__icontains=query)
        results = list(Companys.values())
    else:
        results = []
    return JsonResponse(results,safe=False)


class EmployeeRegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = 'mproduct/employee_register.html'
    success_url = reverse_lazy('mproduct:login')

    def dispatch(self, request: HttpRequest, *args, **kwargs):
        Company = self.kwargs.get('Company')
        BusinessUnit = self.kwargs.get('BusinessUnit')
        self.Company = get_object_or_404(Company,name=Company)

        try:
            self.BusinessUnit = BusinessUnit.objects.get(name=BusinessUnit,Company=self.Company)
        except BusinessUnit.DoesNotExist:
            raise Http404("BusinessUnit Not found")

        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        user = form.save()
        employee = Employee.objects.create(employee=user,BusinessUnit=self.BusinessUnit,is_approved=False)
        sender = user
        created = timezone.now().date()
        status = False
        if self.BusinessUnit.head:
            receiver = self.BusinessUnit.head
        else:
            receiver = employee.BusinessUnit.Company.owner
        request = Requests.objects.create(sender=sender,receiver=receiver,created=created,status=status)
        return super().form_valid(form)