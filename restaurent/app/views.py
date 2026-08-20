from django.shortcuts import redirect, render
from .models import *
import qrcode
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import send_mail,EmailMessage
import django.template.loader
# Create your views here.
def index(request):
    category=Category.objects.all()
    cateid=request.GET.get('category')
    #print(cateid)
    #print(type(cateid))
    if cateid == 'all':
        momo=Momo.objects.filter(is_available=True)

    elif cateid:
        momo=Momo.objects.filter(is_available=True,category=cateid)    
    else:
        momo=Momo.objects.filter(is_available=True)

    if request.method =="POST":
        name=request.POST.get("name")
        phone=request.POST.get("phone")
        email=request.POST.get("email")
        message=request.POST.get("message")
        Form.objects.create(name=name,phone=phone,email=email,message=message)

        subject="Thank you for submmiting your mail"
        message=django.template.loader.render_to_string('auth/email_format.html',{'name':name})
        from_email="simarandev2021@gmail.com"
        recipient_list=[email,"simarandev2021@gmail.com"]

        ab=EmailMessage(subject=subject,body=message,from_email=from_email,to=recipient_list)
      
        ab.send(fail_silently=False)
    

        send_mail(subject,message=message,from_email=from_email,recipient_list=recipient_list,fail_silently=False)
        

        response=redirect('index')
        response.set_cookie('name',name,max_age=3600)
        return response

    context={
         'category':category,
         "momo":momo
    }
    return render(request,'momo_app/index.html',context)


def about(request):
    return render(request,'momo_app/about.html')

def contact(request):
    return render(request,'momo_app/contact.html')
@login_required(login_url='login_part')
def menu(request):
    category=Category.objects.all()
    qr=qrcode.make("http://127.0.0.1:8000/menu/")
    qr.save("app/static/images/qr.png")

    context={
        'category':category
    }
    return render(request,'momo_app/menu.html',context)

def services(request):
    return render(request,'momo_app/services.html')

def testimonial(request):
    review=Review.objects.all()
    if request.method =='POST':
        name=request.POST['name']
        order=request.POST.get('order')
        rating=request.POST.get('rating')
        message=request.POST['message']
        Review.objects.create(name=name,rating=rating,order=order,message=message)

    context={

        'review':review
        }
    return render(request,'momo_app/testimonial.html',context)  

'''
============================================================================
============================================================================
                          AUTH
=============================================================================
=============================================================================                          
'''
def login_part(request):
    name=request.COOKIES.get('name')
    if request.method == "POST":
         username=request.POST.get("username")
         password=request.POST.get("password")
         remember_me=request.POST.get("remember_me")

         if not User.objects.filter(username=username).exists():
              messages.error(request,"username is not register yet")
              return redirect("login_in")

         user =authenticate(username=username,password=password)

         if user is not None:
              login(request,user)
              if remember_me:
                   request.session.set_expiry(360000)
              else:
                   request.session.set_expiry(0)     
              next=request.POST.get('next',"")
              return redirect(next if next else 'index')

         else:
              messages.error(request,'Invalid Password')
              return redirect("register")

    next=request.GET.get('next',"")
          
    return render(request,'auth/login.html',{'next':next,'name':name})


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password1 = request.POST.get("password1")

        if password==password1:
                if User.objects.filter(username=username).exists():
                     messages.error(request,"username is already exists")

                if User.objects.filter(email=email).exists():
                     messages.error (request,"email is already exists") 
                     return redirect("register")

                # if not re.search(r"[A-Z]",password):
                #      messages.error(request,"passsword must contain atleast one uppercase")
                #      return redirect("register")

                # if not re.search(r"\d",password):
                #      messages.error(request,"password must contain at least one digit")
                #      return redirect("register")

                

                try:
                    user=User(first_name=firstname,username=username)
                    validate_password(password)
                    User.objects.create_user(first_name=firstname,username=username,last_name=lastname,email=email,password=password)
                    messages.success(request,"your account is succefully register")
                    return redirect('register') 
                except ValidationError as e:
                    for i in e.messages:
                        messages.error(request,i)
                
                        return redirect("register") 
                                
        else:
                
                messages.error(request,"password and confirm password is incorrect !!")
                return redirect('register')
    return render(request, "auth/register.html")

def log_out(request):
     logout(request)
     return redirect('login_part')

@login_required(login_url="login_part")
def password_change(request):
    form=PasswordChangeForm(user=request.user)
    if request.method == 'POST':
     form=PasswordChangeForm(user=request.user,data=request.POST)
     if form.is_valid():
         form.save()
         return redirect("login_part")
    return render(request,"auth/password_change.html",{'form':form})

 

