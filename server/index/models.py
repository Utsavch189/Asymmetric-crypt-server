from django.db import models
from datetime import date

class SystemInfos(models.Model):
    ip=models.CharField(max_length=40,null=True,blank=True)
    system_name=models.CharField(max_length=50,null=True,blank=True)
    roots=models.TextField(null=True,blank=True)
    items=models.TextField(null=True,blank=True)

    def __str__(self) -> str:
        return self.system_name

class PrivateKey(models.Model):
    system_name=models.CharField(max_length=50,null=True,blank=True)
    key=models.TextField(null=True,blank=True)
    path=models.CharField(max_length=200,null=True,blank=True)
    filename=models.CharField(max_length=50,null=True,blank=True)
    created_at=models.DateField(date.today())

    def __str__(self) -> str:
        return self.system_name

class Action(models.Model):
    path=models.CharField(max_length=200,null=True,blank=True)
    filename=models.CharField(max_length=50,null=True,blank=True)
    system_name=models.CharField(max_length=50,null=True,blank=True)
    action_name=models.CharField(max_length=50,null=True,blank=True)
    
    def __str__(self) -> str:
        return self.system_name
