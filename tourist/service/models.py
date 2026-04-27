from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Contact(models.Model):
    username=models.CharField(max_length=10)
    email=models.CharField(max_length=20)
    add=models.TextField()


    # Emergency Details
    ename = models.CharField(max_length=30)
    relation = models.CharField(max_length=30)  
    emergencynumber = models.CharField(max_length=10)

    def __str__(self):
        return self.dname

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    
class Feed(models.Model):
    name=models.CharField(max_length=10)
    email=models.CharField(max_length=20)
    msg=models.TextField()
# Create your models here.

class Tourist(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    identity_id = models.CharField(max_length=256)
    tourist_number = models.CharField(max_length=10)
    guardian_number = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

class EmergencyLog(models.Model):
    tourist = models.ForeignKey(Tourist, on_delete=models.CASCADE)
    location = models.CharField(max_length=255)
    issue = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


class SafetyLog(models.Model):

    tourist = models.ForeignKey(Tourist, on_delete=models.CASCADE)
    location = models.CharField(max_length=255)
    status = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)