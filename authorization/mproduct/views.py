from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from mproduct.forms import UserRegisterForm
from django.views.generic import CreateView, TemplateView, ListView
from mproduct.models import Plans
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET
from django.http import JsonResponse
# Create your views here.

class RegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = "mproduct/register.html"
    success_url = reverse_lazy("mproduct:home")

class PurchaseView(ListView,LoginRequiredMixin):
    model = Plans
    template_name = 'mproduct/plans.html'
    context_object_name = 'plans'
    login_url = 'mproduct:login'

    def get_queryset(self):
        return Plans.objects.filter(user=self.request.user)

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
        brands = Plans.objects.filter(brand__icontains=query)
        results = list(brands.values())
    else:
        results = []
    # print('-------------------',results)
    
    return JsonResponse(results,safe=False)