from django.contrib import admin
from .models import SystemInfos,PrivateKey,Action

admin.site.register(SystemInfos)
admin.site.register(PrivateKey)
admin.site.register(Action)