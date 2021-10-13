from django.db import models
from django.contrib.auth.models import User
from quiz.models import Field

class College(models.Model):
    college_name=models.CharField(max_length=60)

    def __str__(self):
        return self.college_name
class Student(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    mobile = models.CharField(max_length=20,null=False)
    email=models.EmailField(max_length = 254,null=True,blank=True)
    exam = models.ForeignKey(Field,on_delete=models.CASCADE,null=True,blank=True)
    marks = models.PositiveIntegerField(default=0)
    suspicious=models.BooleanField(default=False)
    date = models.DateTimeField(auto_now=True)
    status_choice = [
    ('pending', 'pending'),
    ('started', 'started'),
    ('submitted', 'submitted'),
    ]
    status=models.CharField(max_length=20,choices=status_choice,default='pending')
    college=models.ForeignKey(College,on_delete=models.CASCADE,default=None)

   
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_instance(self):
        return self
    def __str__(self):
        return self.user.first_name