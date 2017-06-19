from django.db import models

# Create your models here.
class Words(models.Model):
    word = models.CharField(max_length=600)
    
    def __str__(self):
        return "{0}".format(self.word)

class FBMessage(models.Model):
    sender = models.CharField(max_length = 30, default = "logbot")
    recipient = models.CharField(max_length = 30, default = "logbot")
    message = models.CharField(max_length = 30)
    time_set = models.DateTimeField('time sent')

class Person(models.Model):
    first_name = models.CharField(max_length = 30)
    last_name = models.CharField(max_length = 40)
    fbid = models.CharField(max_length = 100)
    def __str__(self):
        return "first_name:{0} last_name:{1} {2}".format(self.first_name, self.last_name, self.fbid)

class Question(models.Model):
    question = models.CharField(max_length = 200)
    person = models.ForeignKey(Person,on_delete=models.CASCADE)
    def __str__(self):
        return "question:{0} person:{1}".format(self.question, self.person)

class Answer(models.Model):
    question = models.ForeignKey(Question,on_delete=models.CASCADE)
    answer = models.IntegerField()
    def __str__(self):
        return"question:{0} answer:{1}".format(self.question, self.answer)
