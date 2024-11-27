from django.urls import path
from  . views import(
    home,
    register,
    login,
    verify_otp,
)

urlpatterns = [
    path('',home,name='home'),
    path('register/',register,name='register'),
    path('verify_otp/<int:user_id>',verify_otp,name='verify_otp'),
    path('login/',login,name='login'),
]