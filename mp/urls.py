from django.urls import path
from . import views
from .views import  SignUpView
urlpatterns = [
    path('', views.home, name = 'home'),
    path('logout/', views.Logout, name = 'logout'),

    path('signup/', SignUpView.as_view(), name= 'signup'),
    path('dashboard/',views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('contact_us/',views.contact_us, name='contact_us'),
    path('about_us/', views.about_us, name= 'about_us'),
    path('privacy/', views.privay_and_policy, name='privacy_and_policy'),
    path('terms_of_conditions/', views.terms_of_conditions, name='terms_of_conditions'),
    path('faq/', views.faq, name= 'faq'),
    path('return_policy/', views.return_policy, name = 'return_policy'),
   # path('call_us/', views.call_us, name='call_us')

]
