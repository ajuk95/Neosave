from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse, HttpResponse

from Users.models import User
from Users.serializers import UserSerializer
import requests
import json

# Create your views here.


@csrf_exempt
def post_user(request):
    if request.method == 'POST':
        '''
        user_data = {
            "Name": "abhishek",
            "Email": "abhi@gmail.com",
            "AddressPostcode": "560063",
            "StateName": ""
        }
        '''
        user_data = JSONParser().parse(request)
        pin = user_data['AddressPostcode']
        url = "https://api.postalpincode.in/pincode/" + str(pin)
        try:
            response = requests.get(url)
            res = json.loads(response.content)
            res = res[0]['PostOffice'][0]['State']
            user_data["StateName"] = res
        except:
            return JsonResponse("Postcode invalid, Failed to Add", safe=False)

        name = user_data.get("Name")
        if name == "" or name is None:
            return JsonResponse("Name is unfilled, Failed to Add", safe=False)

        user_serializer = UserSerializer(data=user_data)
        try:
            if user_serializer.is_valid():
                user_serializer.save()
                return JsonResponse("Added Successfully", safe=False)
        except ValidationError:
            return JsonResponse("Email already exists, Failed to Add", safe=False)
        else:
            return JsonResponse("Email invalid, Failed to Add", safe=False)
    return JsonResponse("invalid http method", safe=False)


def get_user(request, id):
    if request.method == 'GET':
        try:
            user = User.objects.get(Id=id)
            user_serializer = UserSerializer(user)
            return JsonResponse(user_serializer.data, safe=False)
        except:
            return JsonResponse("User_id not found", safe=False)
    return JsonResponse("invalid http method", safe=False)


@csrf_exempt
def get_all_users(request):
    if request.method == 'GET':
        users = User.objects.all()
        users_serializer = UserSerializer(users, many=True)
        return JsonResponse(users_serializer.data, safe=False)
    elif request.method == 'PUT':
        user_data = JSONParser().parse(request)
        user = User.objects.get(Email=user_data['Email'])
        user_serializer = UserSerializer(user, data=user_data)
        if user_serializer.is_valid():
            user_serializer.save()
            return JsonResponse("User Updated Successfully", safe=False)
        return JsonResponse("Failed to Update", safe=False)
    elif request.method == 'DELETE':
        try:
            user = User.objects.all()[0]
            user.delete()
            return JsonResponse("User Deleted Successfully", safe=False)
        except:
            return JsonResponse("All Users are deleted", safe=False)
