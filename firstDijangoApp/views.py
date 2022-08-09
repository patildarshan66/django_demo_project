from asyncio import streams
from functools import partial
import re
from django.views import View
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework.renderers import JSONRenderer
import io
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt

from django.utils.decorators import method_decorator

from firstDijangoApp.models import Student
from firstDijangoApp.serializers import StudentSerializers
# Create your views here.

### function based view 
def student_detail(request,id): 
    stu = Student.objects.get(id=id)
    serializer = StudentSerializers(stu)
    json_data = JSONRenderer().render(serializer.data)
    # json_data = JsonResponse(serializer.data)
    return HttpResponse(json_data,content_type = 'application/json')

def students_list(request):
    stu = Student.objects.all()
    serializer = StudentSerializers(stu,many=True)
    # json_data = JSONRenderer().render(serializer.data)
    return JsonResponse(serializer.data,safe = False)
    # return HttpResponse(json_data,content_type = 'application/json')

@csrf_exempt
def add_student(request):
    if request.method == 'POST':
        json_data = request.body;
        stream = io.BytesIO(json_data)
        pythonData = JSONParser().parse(stream)
        serializer = StudentSerializers(data = pythonData)
        if serializer.is_valid():
            serializer.save()
            res = {'msg':'Student added successfully.'}
            return JsonResponse(res)
        
        return JsonResponse(serializer.errors) 
    msg = {'msg':'This is POST method.'}  
    return JsonResponse(msg)

### class based view 
@method_decorator(csrf_exempt,name='dispatch')
class StudentAPI(View):
    def get(self,request,*args, **kwargs):
        json_data = request.body;
        if json_data != b'':
            stream = io.BytesIO(json_data)
            pythonData = JSONParser().parse(stream)
            id = pythonData.get('id',None)
            if id != None:
                stu = Student.objects.get(id=id)
                seralizer = StudentSerializers(stu)
                return JsonResponse(seralizer.data)
            
        stu = Student.objects.all()
        seralizer = StudentSerializers(stu,many = True)
        return JsonResponse(seralizer.data,safe=False)

    def post(self,request,*args,**kwargs):
        json_data = request.body;
        stream = io.BytesIO(json_data)
        pythonData = JSONParser().parse(stream)
        serializer = StudentSerializers(data = pythonData)
        if serializer.is_valid():
            serializer.save()
            res = {'msg':'Student added successfully.'}
            return JsonResponse(res)
        
        return JsonResponse(serializer.errors)
    
    def put(self,request,*args,**kwargs):
        json_data = request.body;
        stream = io.BytesIO(json_data)
        pythonData = JSONParser().parse(stream)
        id = pythonData.get('id')
        stu = Student.objects.get(id=id)
        serializer = StudentSerializers(stu,data=pythonData)
        if serializer.is_valid():
            serializer.save()
            res = {'msg':'Student updated successfully.'}
            return JsonResponse(res)
        return JsonResponse(serializer.errors)
    
    def patch(self,request,*args,**kwargs):
        json_data = request.body;
        stream = io.BytesIO(json_data)
        pythonData = JSONParser().parse(stream)
        id = pythonData.get('id')
        stu = Student.objects.get(id=id)
        serializer = StudentSerializers(stu,data=pythonData,partial =True)
        if serializer.is_valid():
            serializer.save()
            res = {'msg':'Student updated successfully.'}
            return JsonResponse(res)
        return JsonResponse(serializer.errors)
    
    def delete(self,request,*args,**kwargs):
        json_data = request.body;
        stream = io.BytesIO(json_data)
        pythonData = JSONParser().parse(stream)
        id = pythonData.get('id')
        stu = Student.objects.get(id=id)
        stu.delete()
        res = {'msg':'Student deleted successfully.'}
        return JsonResponse(res)
        
        
        
        
        
    