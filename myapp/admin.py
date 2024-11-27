from django.contrib import admin
from . models import User


# Register your models here.
class userOrder(admin.ModelAdmin):
    list_display = ['id','first_name','last_name','email','email_otp',
                'is_email_verified','otp_created_time','otp_expiry_time']

admin.site.register(User, userOrder)

