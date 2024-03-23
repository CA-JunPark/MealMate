from django.shortcuts import render
from rest_framework.views import APIView
from post.models import Post
from account.models import Account

class Home(APIView):
    def get(self, request):
        user = request.user
        if user is None:
            return render(request, 'mealmate/login.html')
        
        user_objects = Account.objects.get(email=user.email)
        posts_objects = Post.objects.all()
        
        posts = []
        for post in posts_objects:
            photo = Account.objects.get(email=post.owner).photo
            posts.append(dict(id = post.id, 
                              owner=post.owner, 
                              photo=photo, 
                              where=post.where,
                              Note=post.Note,
                              current_user_number=post.current_user_number,
                              current_users=post.current_users,
                              max_user_num=post.max_user_num,
                              when=post.when))
            
        return render(request, 'mealmate/home.html', context={'posts': posts, 'user': user_objects})