from inspect import classify_class_attrs
import re
from wsgiref.validate import validator
from rest_framework import serializers
from .models import Student

#validators

def name_validator(name):
    if len(name) <=2:
       raise serializers.ValidationError('Name is too short.')
            
    regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
     
    if (regex.search(name) != None):
        raise serializers.ValidationError('Special characters not allowed.')
    
def city_validator(city):
    if city.lower() == 'mumbai':
       raise serializers.ValidationError('Mumbai city not allowed.')


class StudentSerializers(serializers.Serializer):
    name = serializers.CharField(max_length=255,validators = [name_validator])
    roll = serializers.IntegerField()
    city = serializers.CharField(max_length=255,validators = [city_validator])
    
    def create(self, validate_data):
        return Student.objects.create(**validate_data)
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name',instance.name)
        instance.roll = validated_data.get('roll',instance.roll)
        instance.city = validated_data.get('city',instance.city)
        instance.save()
        return instance
    
    #field level validation
    def validate_roll(self,value):
        if(value>=200):
            raise serializers.ValidationError('Seat full')
        return value
    
    #object level validation
    # def validate(self, data):
    #     name = data.get('name')
    #     city = data.get('city')
    #     map = {}
    #     if len(name) <=2:
    #         map['name_error'] = 'Name is too short.'
            
    #     regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
     
    #     if (regex.search(name) != None):
    #         map['name_error_1'] = 'Special characters not allowed.'
        
    #     if city.lower() == 'mumbai':
    #        map['city_errror']='Mumbai city not allowed.'
        
    #     if(len(map)>0):
    #         raise serializers.ValidationError(map)
        
    #     return data
            