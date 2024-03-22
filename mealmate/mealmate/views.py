from django.shortcuts import render
from rest_framework.views import APIView

class Home(APIView):
    def get(self, request):
        return render(request, 'mealmate/home.html')
