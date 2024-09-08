from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from mproduct.forms import UserRegisterForm
from django.contrib.auth.models import User
from django.views.generic import CreateView, TemplateView, ListView, DetailView, View
from mproduct.models import Plans, Brand, Subscribers
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET
from django.http import HttpResponse, JsonResponse
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
        context['title'] = 'Home'
        return context

class PlansView(LoginRequiredMixin,ListView):
    model = Plans
    template_name = 'mproduct/plans.html'
    context_object_name = 'plans'
    login_url = 'mproduct:login'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(brand=get_object_or_404(Brand,name='mproduct'))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_authenticated'] = self.request.user.is_authenticated
        return context

class SubscribeView(LoginRequiredMixin,View):
    login_url = 'mproduct:login'

    def post(self,request,*args,**kwargs):
        plan_id = request.POST.get('plan_id')
        plan = get_object_or_404(Plans, id=plan_id)
        name = request.user
        date = timezone.now().date()
        status = True
        Subscribers.objects.create(name=name,plan=plan,purchased_on=date,subscription_status=status)
        return redirect('mproduct:home')

class CreateBrand(LoginRequiredMixin,CreateView):
    login_url = 'mproduct:login'
    model = Brand
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
        brand = Brand.objects.get(owner=self.request.user)
        print("------------->brand",brand)
        form.instance.brand = brand
        return super().form_valid(form)


class SettingsView(LoginRequiredMixin,TemplateView):
    login_url = 'mproduct:login'
    template_name = 'mproduct/settings.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_authenticated'] = self.request.user.is_authenticated
        context['profile'] = get_object_or_404(User,username=self.request.user)
        context['is_authorized'] = False if not Subscribers.objects.filter(name=self.request.user).first() else True
        if context['is_authorized']:
            context['is_brand'] = False if not Brand.objects.filter(owner=self.request.user).first() else True
        else:
            context['is_brand'] = False
        if context['is_brand']:
            context['brand'] = Brand.objects.get(owner=self.request.user)
            if Plans.objects.filter(brand=context['brand']).count() < 3:
                context['create_plans'] = True
            else:
                context['create_plans'] = False
            context['plans'] = Plans.objects.filter(brand=context['brand'])
        else:
            context['brand'] = False
        print("------------->",context)
        return context


class PurchaseView(LoginRequiredMixin,ListView):
    model = Plans
    template_name = 'mproduct/purchase.html'
    context_object_name = 'plans'
    login_url = 'mproduct:login'


class SubscriptionView(LoginRequiredMixin,DetailView):
    template_name = 'mproduct/subscription.html'
    context_object_name = 'subscription'
    login_url = 'mproduct:login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subscribers']

@login_required(login_url='mproduct:login')
def purchase(request):
    context = {}
    context['is_authenticated'] = True
    if request.method == 'POST':
        plan_id = request.POST.get('plan_id')
        plan = get_object_or_404(Plans,id=plan_id)
        name = request.user
        date = timezone.now().date()
        status = True
        subscriber = Subscribers.objects.create(name=name,plan=plan,purchased_on=date,subscription_status=status)
        return redirect('mproduct:home')
    else:
        brand = Brand.objects.filter(name='mproduct')
        if brand:
            brand = brand[0]
            context['plans'] = Plans.objects.filter(brand=brand)
        else:
            context['plans'] = []
    return render(request=request,template_name='mproduct/purchase.html',context=context)

class LandingPageView(TemplateView):
    template_name = "mproduct/landing.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'base'
        context['is_authenticated'] = self.request.user.is_authenticated
        return context

@require_GET
def search_brands(request):
    query = request.GET.get('data','')
    if query:
        brands = Brand.objects.filter(name__icontains=query)
        results = list(brands.values())
    else:
        results = []
    # print('-------------------',results)
    
    return JsonResponse(results,safe=False)