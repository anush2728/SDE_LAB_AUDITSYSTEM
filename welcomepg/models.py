from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date


def create_json():
    data = list(Act.objects.values())
    new = {}
    for i in data:
        new[i['act_name']] = {'selected':False,'uploaded':False}
    #print(data)
    return new

def obser_json():
    data = list(Act.objects.values())
    new = {}
    for i in data:
        new[i['act_name']] = ""
    #print(data)
    return new 



class User(AbstractUser):        
    contact_number=models.BigIntegerField(null=True)
    related = models.IntegerField(null=True)
    class Role(models.TextChoices):
        ADMIN = 'Admin'
        AUDITOR = 'Auditor'
        SUBCONTRACTOR = 'Subcontractor'

    base_role = Role.ADMIN
    role = models.CharField(max_length=50,choices=Role.choices,null=True,default=Role.ADMIN) 

    def save(self,*arg,**kwargs):
        return super().save(*arg,**kwargs)

    def _str_(self):
        return f"{self.username}"


class AuditorManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.AUDITOR)

class Auditor(User):
    base_role = User.Role.AUDITOR
    auditor = AuditorManager() #Auditor.auditor.all()
    class Meta:
        proxy = True

    def welcome(self):
        return "Only for auditors"

class SubcontractorManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.SUBCONTRACTOR)

class Subcontractor(User):
    base_role = User.Role.SUBCONTRACTOR
    subcontractor = SubcontractorManager() #Auditor.auditor.all()
    class Meta:
        proxy = True

    def welcome(self):
        return "Only for subs"

class Act(models.Model):
    act_desc=models.TextField()
    act_name=models.CharField(max_length=30)
    act_shname=models.CharField(max_length=5)

    def __str__(self):
        return f"{self.act_shname}"

def selectedActs(audit_name,sub_name):
    val = Event.objects.all()
    x = []
    for i in val:
            print(i.audit,'-',i.sub,'\n',audit_name,'=',sub_name)
            if str(i.audit) == audit_name and str(i.sub) == sub_name:
                x = [j for j in i.acts if i.acts[j]['selected'] == True]
    return x

def uploadedActs(audit_name,sub_name):
    val = Event.objects.all()
    x = []
    for i in val:
            #print(type(str(i.audit)),type(audit_name))
            if str(i.audit) == audit_name and str(i.sub) == sub_name:
                x = [j for j in i.acts if i.acts[j]['uploaded'] == True]
    return x

class Event(models.Model):
    
    audit = models.ForeignKey(to=Auditor,on_delete=models.CASCADE,null=True,related_name='auditor')
    sub = models.ForeignKey(to=Subcontractor,on_delete=models.CASCADE,null=True,related_name='subcontractor')
    #description = models.TextField(blank=True,null=True)
    event_date = models.DateField('Event Date',max_length=30,null=True)
    event_time = models.TimeField('Event Time',max_length=30,null=True)
    acts = models.JSONField(default=create_json)
    observation = models.JSONField(default=obser_json)

    def __str__(self):
        return f"{self.audit} - {self.sub}"

class UploadFile(models.Model):
    f_name = models.CharField(max_length=255)
    #a_name = models.ForeignKey(to=Act,on_delete=models.CASCADE,null=True)
    f_files = models.FileField(upload_to="")
    e_id = models.ForeignKey(to=Event,on_delete=models.CASCADE,null=True)
    
    def __str__(self):
        return self.f_name