from django.shortcuts import render,redirect
from django.contrib.auth.models import auth
from . models import User
from django.contrib import messages
from . utils import email_sender, generate_otp
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

# Create your views here.
def home(request):
    return render(request,'home.html')

def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if len(password) >= 8:
            if password == password2:
                if User.objects.filter(email=email).exists():
                    messages.info(request,'This email already exists')
                    return redirect('register')
                else:
                    user = User.objects.create(first_name=first_name,last_name=last_name,email=email,password=password)

                    email_sender(user.email)

                    user.save()
                    
                    return redirect('verify_otp',user_id=user.id)
                
            else:
                messages.info(request,'Password doesn\'t match')
                return render(request,'register.html')
        else:
            messages.info(request,'Password should contain atleast 8 characters')
            return render(request,'register.html')
    return render(request,'register.html')

def verify_otp(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        if request.method == 'POST':
            email_otp = request.POST['email_otp']

            #checking if the email otp is the same as that in the DB
            if email_otp==user.email_otp:
                if user.is_email_verified == True:
                    messages.info(request, 'The OTP is already used')
                    return redirect('verify_otp',user_id=user.id)
                
                #checking otp expiry time
                elif  timezone.now() > user.otp_expiry_time:   
                    messages.warning(request, 'The OTP has Expired')
                    return redirect('verify_otp',user_id=user.id)   
                            
                # checking if the otp has already used
                user.is_email_verified = True
                user.save()
                return redirect('login')
            messages.info(request, 'The OTP is Invalid')
            return redirect('verify_otp',user_id=user.id)
        return render(request,'otp.html')
    except ObjectDoesNotExist:
        messages.warning(request,'User Does not exist')
        return redirect("register")

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(username=email,password=password)

        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request,'Invalid crediantials')
            return redirect('login')
    return render(request,'login.html')