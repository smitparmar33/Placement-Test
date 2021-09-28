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


#for showing signup/login button for student
# def studentclick_view(request):
#     if request.user.is_authenticated:
#         return HttpResponseRedirect('afterlogin')
#     return render(request,'student/studentclick.html')

# def student_signup_view(request):
#     userForm=forms.StudentUserForm()
#     studentForm=forms.StudentForm()
#     mydict={'userForm':userForm,'studentForm':studentForm}
#     if request.method=='POST':
#         userForm=forms.StudentUserForm(request.POST)
#         studentForm=forms.StudentForm(request.POST,request.FILES)
#         if userForm.is_valid() and studentForm.is_valid():
#             user=userForm.save()
#             user.set_password(user.password)
#             user.save()
#             student=studentForm.save(commit=False)
#             student.user=user
#             student.save()
#             my_student_group = Group.objects.get_or_create(name='STUDENT')
#             my_student_group[0].user_set.add(user)
#         return HttpResponseRedirect('studentlogin')
#     return render(request,'student/studentsignup.html',context=mydict)

# def is_student(user):
#     return user.groups.filter(name='STUDENT').exists()

# @login_required(login_url='login')
# # @user_passes_test(is_student)
# def student_dashboard_view(request):
#     dict={
    
#     'total_course':QMODEL.Field.objects.all().count(),
#     'total_question':QMODEL.Question.objects.all().count(),
#     }
#     return render(request,'student/student_dashboard.html',context=dict)

@login_required(login_url='login')
def field_choice(request):
    field_name=QMODEL.Field.objects.all()
    return render(request,'fields.html',{'field_name':field_name})

@login_required(login_url='login')
# @user_passes_test(is_student)
def instruction(request,pk):
    field=QMODEL.Field.objects.get(id=pk)
    total_questions=QMODEL.Question.objects.all().filter(field=field).count()
    questions=QMODEL.Question.objects.all().filter(field=field)
    total_marks=0
    for q in questions:
        total_marks=total_marks + q.marks
    
    return render(request,'instruction.html',{'field':field,'total_questions':total_questions,'total_marks':total_marks})

@login_required(login_url='login')
# @user_passes_test(is_student)
def start_exam_view(request,pk):
    field=QMODEL.Field.objects.get(id=pk)
    questions=QMODEL.Question.objects.all().filter(field=field)
    if request.method=='POST':
        pass
    response= render(request,'quiz.html',{'field':field,'questions':questions})
    response.set_cookie('field_id',field.id)
    return response


@login_required(login_url='login')
# @user_passes_test(is_student)
def calculate_marks_view(request):
    if request.COOKIES.get('field_id') is not None:
        field_id = request.COOKIES.get('field_id')
        field=QMODEL.Field.objects.get(id=field_id)
        
        total_marks=0
        questions=QMODEL.Question.objects.all().filter(field=field)
        for i in range(len(questions)):
            
            selected_ans = request.COOKIES.get(str(i+1))
            actual_answer = questions[i].answer
            if selected_ans == actual_answer:
                total_marks = total_marks + questions[i].marks
        print(request.user.id)
        user_obj = User.objects.get(id=request.user.id)
        student = models.Student()
        student.user=user_obj
        student.mobile="7878585787"
        student.marks=total_marks
        student.email=user_obj.email
        student.exam=field
        student.student=student
        student.save()

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

@login_required(login_url='login')
# @user_passes_test(is_student)
def student_marks_view(request):
    fields=QMODEL.Field.objects.all()
    return render(request,'student/student_marks.html',{'fields':fields})