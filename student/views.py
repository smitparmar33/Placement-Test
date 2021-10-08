from django.shortcuts import render,redirect,reverse
from . import models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from quiz import models as QMODEL
from quiz.models import Field
from django.contrib.auth.models import User
from django.core.mail import send_mail,BadHeaderError
from placementbot.settings import EMAIL_HOST_USER,EMAIL_HOST_PASSWORD
import datetime
from django.http import HttpResponse,JsonResponse


@login_required(login_url='login')
def field_choice(request):
    print("Inside choise")
    user_obj = User.objects.get(id=request.user.id)
    print(user_obj)
    try:
        student = models.Student.objects.get(user=user_obj)
        print("status.......",student.status)
    except:
        return HttpResponse("Something went wrong you cannot login. Please contact contact@yudiz.com")
    if student.status=="started":
        if request.session["exam_started"]:
            pk=request.session["field"]
            return redirect(f"/student/start-exam/{pk}")
        else:
            return HttpResponse("Your exam already started please try to login with same web browser")
    elif student.status=="submitted":
        return HttpResponse("You have already submitted your exam")
    else:
        field_name=QMODEL.Field.objects.all()
        return render(request,'fields.html',{'field_name':field_name})

@login_required(login_url='login')
# @user_passes_test(is_student)
def instruction(request,pk):

    field=QMODEL.Field.objects.get(id=pk)
    total_questions=QMODEL.Question.objects.all().filter(field=field).count()
    questions=QMODEL.Question.objects.all().filter(field=field)
    total_marks=0
    duration=field.duration
    for q in questions:
        total_marks=total_marks + q.marks
    
    return render(request,'instruction.html',{'field':field,'total_questions':total_questions,'total_marks':total_marks,'duration':duration})

def set_timer(request,pk):
    request.session["count"]=0
    x = datetime.datetime.now()
    now = x.strftime("%b %d, %Y %H:%M:%S")
    request.session['start_time']=str(now)
    print(pk)
    return redirect(f"/student/start-exam/{pk}")

@login_required(login_url='login')
# @user_passes_test(is_student)
def start_exam_view(request,pk):
    field=QMODEL.Field.objects.get(id=pk)
    questions=QMODEL.Question.objects.all().filter(field=field)
    user_obj = User.objects.get(id=request.user.id)
    name=user_obj.first_name.title()+" "+user_obj.last_name.title()

    student = models.Student.objects.get(user=user_obj)
    student.status="started"
    student.exam=field
    student.save()
    if request.method=='POST':
        pass
    duration=(602000*field.duration)/10
    request.session["field"]=pk
    request.session["exam_started"]=True
    response= render(request,'quiz.html',{'field':field,'questions':questions,'time':request.session['start_time'],'duration':duration,'name':name})
    response.set_cookie('field_id',field.id)
    return response

def suspicious(request):
    print("called")
    request.session["count"]+=1
    response={"count":request.session["count"]}
    return JsonResponse (response)


@login_required(login_url='login')
# @user_passes_test(is_student)
def calculate_marks_view(request):
    if request.COOKIES.get('field_id') is not None:
        field_id = request.COOKIES.get('field_id')
        field=QMODEL.Field.objects.get(id=field_id)
        total_marks=0
        questions=QMODEL.Question.objects.all().filter(field=field)
        for q in questions:
            total_marks=total_marks + q.marks
        obtained_marks=0
        
        for i in range(len(questions)):
            
            selected_ans = request.COOKIES.get(str(i+1))
            print("selected",selected_ans)
            actual_answer = questions[i].answer
            if selected_ans == actual_answer:
                obtained_marks = obtained_marks + questions[i].marks
        user_obj = User.objects.get(id=request.user.id)
        student = models.Student.objects.get(user=user_obj)
        # student = models.Student()
        # student.user=user_obj
        # student.mobile="7878585787"
        if request.session["count"] < 3:
            print(obtained_marks)
            student.marks=obtained_marks
            # student.email=user_obj.email
            student.exam=field
            student.student=student
            student.status="submitted"
            student.save()
            percetange=(float(obtained_marks)/float(total_marks))*100
            print(percetange)
            try:
                if percetange >=70:
                    send_mail(
                                        'Congratulations!',
                                        f'Congratulations {user_obj.first_name},\nYou are qualified for the next round.Your score is {obtained_marks} out of {total_marks}.\nSoon you will get update regarding your upcoming round.\n\nThank you and wish you good luck!',
                                        EMAIL_HOST_USER,
                                        [user_obj.email],
                                        fail_silently=False,
                                    )
                else:
                    send_mail(
                                        'Exam Result',
                                        f'Hello {user_obj.first_name},\nSorry you have not qualified for the next round. Your score is {obtained_marks} out of {total_marks}.\n\nThank you',
                                        EMAIL_HOST_USER,
                                        [user_obj.email],
                                        fail_silently=False,
                                    )
            except:
                pass
            request.session["count"]=0
            request.session.modified = True
            return redirect('/logout')
        else:
            print("inside suspicious",request.session["count"])
            student.marks=0
            # student.email=user_obj.email
            student.exam=field
            student.student=student
            student.status="submitted"
            student.suspicious=True
            student.save()
            request.session["count"]=0
            request.session.modified = True
            return redirect('/logout')



@login_required(login_url='login')
# @user_passes_test(is_student)
def view_result_view(request):
    fields=QMODEL.Field.objects.all()
    return render(request,'student/view_result.html',{'fields':fields})
    

# @login_required(login_url='login')
# # @user_passes_test(is_student)
# def check_marks_view(request,pk):
#     field=QMODEL.Field.objects.get(id=pk)
#     student = models.Student.objects.get(user_id=request.user.id)
#     results= QMODEL.Result.objects.all().filter(exam=field).filter(student=student)
#     return render(request,'student/check_marks.html',{'results':results})
