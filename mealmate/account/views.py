from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Account
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate, login, logout
from mealmate.settings import MEDIA_ROOT

class CreateAccount(APIView):
    def get(self, request):
        return render(request, 'account/createAccount.html')

    def post(self, request):
        username = request.data.get('name', None)
        email = request.data.get('email', None)
        password = request.data.get('password', None)
        confirmPW = request.data.get('confirmPW', None)
        gender = request.data.get('gender', None)
        country = request.data.get('country', None)
        print(country)
        language = request.data.get('language', None)
        year = request.data.get('year', None)
        year = int(year)
        major = request.data.get('major', None)
        minor = request.data.get('minor', None)
        bio = request.data.get('bio',None)
        
        if not username:
            return Response(status=500, data=dict(message='Cannot have blank username'))
        
        if not email:
            return Response(status=500, data=dict(message='Cannot have blank email'))
        
        if not password:
            return Response(status=500, data=dict(message='Cannot have blank password'))
        
        if password != confirmPW:
            return Response(status=500, data=dict(message='Password does not match'))
        
        if Account.objects.filter(email=email).exists():
            return Response(status=500, data=dict(message='This email already exists'))

        Account.objects.create(username=username, 
                               email=email, 
                               password = make_password(password),
                               gender=gender,
                               country=country,
                               language=language,
                               year=year,
                               major=major,
                               minor=minor,
                               bio=bio)
        
        return Response(status=200, data=dict(message="Registration Success"))

    
class Login(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        return render(request, 'account/login.html')

    def post(self, request):
        email = request.data.get('email', None)
        password = request.data.get('password', None)
        
        user = authenticate(email=email, password=password)
        
        if user is None:
            print("user not exists")
            return Response(status=500, data=dict(message='Account does not exist'))

        if check_password(password, user.password) is False:
            print("wrong pw")
            return Response(status=500, data=dict(message='Wrong Password'))

        request.session['loginCheck'] = True
        request.session['email'] = user.email
        
        login(request, user)
        
        return Response(status=200, data=dict(message='Login Success'))

class LogOut(APIView):
    def get(self, request):
        request.session.flush()
        logout(request)
        return render(request, "account/login.html")

class Profile(APIView):
    def get(self, request):
        userEmail = request.GET.get('userEmail')
        user = Account.objects.get(email=userEmail)
        return render(request, "account/profile.html", context={'user':user})
    
class OtherProfile(APIView):
    def get(self, request):
        userEmail = request.GET.get('userEmail')
        user = Account.objects.get(email=userEmail)
        otherEmail = request.GET.get('otherEmail')
        other = Account.objects.get(email=otherEmail)
        return render(request, "account/otherProfile.html", context={'user': user, 'other': other})
