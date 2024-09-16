from django.shortcuts import render, redirect
from order.models import Order
from shop.models import *
from .models import *
from django.contrib.auth.decorators import login_required
from carts.views import *
from carts.models import *
from .forms import SignUpForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserForm, ProfileForm

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

# class CustomLogoutView(LogoutView):
#     template_name = 'registration/logged_out.html'
def Logout(request):
    logout(request)
    return redirect('home')   

class CustomPasswordResetView(PasswordResetView):
    template_name = 'registration/password_reset_form.html'
    success_url = reverse_lazy('password_reset_done')
    email_template_name = 'registration/password_reset_email.html'

class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.success_url)



@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

def home(request):
    featured_products = Product.objects.all()[:5]
    return render(request, 'base.html', {'featured_products' : featured_products})

@login_required(login_url="login")
def dashboard(request):
    user = request.user
    
    # Profile Information
    profile_info = {
        'name': f'{user.first_name} {user.last_name}',
        'email': user.email,
        
        #'phone': user.phone,
       # 'location': user.location,
        #'birth_date': user.birth_date
        #'contact': user.profile.contact if hasattr(user, 'profile') else '',
        #'address': user.profile.address if hasattr(user, 'profile') else '',
    }
    
    # Order History
    orders = Order.objects.filter(user=user, is_ordered=True)
    

    
    context = {
        'profile_info': profile_info,
        'orders': orders,
        
    }
    
    return render(request, "dashboard.html", context)


@login_required
def contact_us(request):
    
    return render(request, 'contact_us.html')


def about_us(request):
    return render(request, 'about_us.html')

def privay_and_policy(request):
    return render(request, 'privacy_and_policy.html')

def terms_of_conditions(request):
    return render(request, 'terms_of_conditions.html')
def faq(request):
    return render(request, 'faq.html')

def return_policy(request):
    return render(request, 'return_policy.html')

# def call_us(request):
#     return render(request,'call_us.html')