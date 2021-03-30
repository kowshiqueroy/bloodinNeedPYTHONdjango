from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Donor(AbstractUser):
   full_name = models.CharField(max_length=100, null=False, blank= False, default="User")
   contact = models.CharField(max_length=100, null=False, blank= False, default="ContactNum")
   location = models.CharField(max_length=100, null=False, blank=False, default="Location")
   blood_group = models.CharField(max_length=10, null=False, blank= False, default="BG")
   is_donor = models.BooleanField(null=False, blank= False,default=False)



class Blog (models.Model):
   content= models.CharField(max_length=1000, null=False, blank= False)
   need= models.BooleanField(null=False, blank= False)
   date= models.DateTimeField(auto_now_add=True)
   location= models.CharField(max_length=200, default=" ")
   blog_blood_group = models.CharField(max_length=10, null=False, blank=False, default="BG")
   user= models.ForeignKey(Donor,null=False, blank=False, on_delete=models.CASCADE)



class DonorFind(models.Model):
   find= models.CharField(max_length=200, default="")