from django.db import models

class Pin(models.Model):
    pin=models.CharField(max_length=10)

    def __str__(self):
        return self.pin
class Field(models.Model):
   field_name = models.CharField(max_length=50)
   question_number = models.PositiveIntegerField()
   profile_pic= models.ImageField(upload_to='field_logo/',null=True,blank=True)
   total_marks = models.PositiveIntegerField()
   duration=models.IntegerField(default=20,null=True,blank=True)
   def __str__(self):
        return self.field_name

class Question(models.Model):
    field=models.ForeignKey(Field,on_delete=models.CASCADE)
    marks=models.PositiveIntegerField()
    question=models.CharField(max_length=600)
    option1=models.CharField(max_length=200)
    option2=models.CharField(max_length=200)
    option3=models.CharField(max_length=200)
    option4=models.CharField(max_length=200)
    cat=(('Option1','Option1'),('Option2','Option2'),('Option3','Option3'),('Option4','Option4'))
    answer=models.CharField(max_length=200,choices=cat)

    def __str__(self):
        return self.question

# class Result(models.Model):
#     student = models.ForeignKey(Student,on_delete=models.CASCADE)
#     email=models.EmailField(max_length = 254)
#     exam = models.ForeignKey(Field,on_delete=models.CASCADE)
#     marks = models.PositiveIntegerField()
#     date = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.email