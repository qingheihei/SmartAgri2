from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework.views import APIView
from rest_framework.authentication import BaseAuthentication,BasicAuthentication
from rest_framework.versioning import QueryParameterVersioning,URLPathVersioning
from rest_framework import serializers
import json
from api import models
from api.utils.permission import AdminPermission


# Create your views here.


def md5(user):
    import hashlib
    import time
    ctime = str(time.time())
    m = hashlib.md5(bytes(user,encoding='utf-8'))
    m.update(bytes(ctime, encoding='utf-8'))
    return m.hexdigest()

class AuthView(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self,request,*args,**kwargs):
        ret = {
            'code': '1000',
            'msg': 'None'
        }
        try:
            user = request._request.POST.get('user_name')
            pwd = request._request.POST.get('password')
            obj = models.UserInfo.objects.filter(user_name=user,password=pwd).first()
            if not obj:
                ret['code'] = 1001
                ret['msg'] = "user error"
            token = md5(user)
            models.UserToken.objects.update_or_create(user=obj,defaults={'token':token})
            ret['token'] = token
        except Exception as e:
            ret['code'] = 1002
            ret['msg'] = 'eee'
        return JsonResponse(ret)

class HouseSerializer(serializers.Serializer):
    house_id = serializers.IntegerField()
    house_name = serializers.CharField()

@method_decorator(csrf_exempt, name='dispatch')
class HouseView(APIView):
    def get(self,request,*args,**kwargs):
        # 方式1
        # houses = models.House.objects.all().values_list('house_name')
        # houses = list(houses)
        # ret = json.dumps(houses, ensure_ascii=False)

        house = models.House.objects.all().first()
        ser = HouseSerializer(instance=house, many=False)
        ret = json.dumps(ser.data, ensure_ascii=False)
        return HttpResponse(ret)

    def post(self,request,*args,**kwargs):
        return HttpResponse('POST OK')
    def put(self,request,*args,**kwargs):
        return HttpResponse('PUT OK')
    def delete(self,request,*args,**kwargs):
        return HttpResponse('DELETE OK')

class ThingView(APIView):
    def get(self,request,*args,**kwargs):
        #print(request.version)
        ret = {
            'code': '1000',
            'msg': 'OK'
        }
        return HttpResponse(json.dumps(ret),status=201)

class MachineView(APIView):
    pass
class MachineTypeView(APIView):
    pass

from rest_framework.parsers import JSONParser,FormParser
class SensorView(APIView):
    #parser_classes = [JSONParser,FormParser,]
    def post(self,request,*args,**kwargs):
        #print(request.data)
        return HttpResponse('POST OK')
    
class SensorValueView(APIView):
    pass

class SensorTypeView(APIView):
    pass