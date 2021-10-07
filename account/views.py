from django.shortcuts import render,redirect,get_list_or_404, get_object_or_404
from django.contrib.auth.models import User,auth
from django.http import HttpResponse
from django.contrib import messages
# from mrbot.models import Exam
from time import sleep
from django.core.mail import send_mail,BadHeaderError
from student.models import Student
from quiz.models import Pin
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
# from placementbot.settings import EMAIL_HOST_USER,EMAIL_HOST_PASSWORD
# from mrbot.models import pin
# Create your views here.

def logout(request):
    sleep(5)
    auth.logout(request)
    return render(request,'thanks.html')

def login(request):

    if request.user.is_authenticated:
        return redirect('field-choice')
    if request.method == "POST":

        username = request.POST['email']
        password = request.POST['psw']
        pin=request.POST['pin']
        user=auth.authenticate(username=username,password=password)
        if user is not None:
                pin_obj=Pin.objects.first()
                exam_pin=pin_obj.pin
                if exam_pin==pin:
                    auth.login(request,user)
                    request.session["exam_started"]=False
                    return redirect('field-choice')
                else:
                     messages.info(request,'Invalid placement pin')
                     return render(request,'login.html',{'color':'red'})
        else:
            messages.info(request,'Invalid cradentials')
            return render(request,'login.html',{'color':'red'})
    else:
        return render(request, 'login.html')

def register(request):
    if request.method=="POST":
        first_name=request.POST['fname']
        last_name = request.POST['lname']
        email = request.POST['email']
        mobile = request.POST['mobile']
        username = request.POST['email']
        password1 = request.POST['psw']
        password2 = request.POST['psw-repeat']

        if password1==password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,'Username taken')
                return render(request,'login.html',{'color':'red'})
            elif User.objects.filter(email=email).exists():
                messages.info(request,'Email already taken')
                return render(request,'login.html',{'color':'red'})
            else:
                user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                                email=email, password=password1)

                user.save()
                student=Student()
                student.user=user
                student.mobile=mobile
                student.email=email
                student.save()
                messages.info(request, 'Registration successful. Now you can login.')
                return render(request,'login.html',{'color':'green'})

        else:
            messages.info(request,'Password not match')
            return render(request,'login.html',{'color':'red'})
    else:
        return render(request,'login.html')

class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'password_reset.html'
    email_template_name = 'password_reset_email.html'
    subject_template_name = 'password_reset_subject'
    success_message ="We've mailed reset password link to your registered email id"
    success_url = reverse_lazy('login')