from django.shortcuts import render
from rest_framework.views import APIView
from post.models import Post
from account.models import Account
import datetime

class Home(APIView):
    def get(self, request):
        user = request.user
        if user is None:
            return render(request, 'mealmate/login.html')
        
        sortVal = request.GET.get('sortVal')
        searchBy = request.GET.get('searchBy')
        searchVal = request.GET.get('searchVal')
        
        print(sortVal, searchBy, searchVal)
        
        user_objects = Account.objects.get(email=user.email)
        if searchVal is None: 
            posts_objects = Post.objects.all()
        else:
            if searchBy == "owner":
                posts_objects = Post.objects.get(ownerName=searchVal)
            # TODO so on...
        
        posts = []
        
        for post in posts_objects:
            # if current time is before post.when
            if post.when > datetime.datetime.now().time():
                owner_object = Account.objects.get(email=post.owner)
                posts.append(dict(id = post.id, 
                                owner=post.owner, 
                                owner_name=owner_object.username,
                                photo=owner_object.photo, 
                                where=post.where,
                                Note=post.Note,
                                current_user_number=post.current_user_number,
                                current_users=post.current_users,
                                max_user_num=post.max_user_num,
                                when=post.when))
            else: # delete posts that are over
                post.delete()
        
        # sort 
        if sortVal is not None:
            posts = sorted(posts, key = lambda item: item[sortVal], reverse=True)
        else:
            posts = sorted(posts, key=lambda item: item["when"], reverse=False)
        return render(request, 'mealmate/home.html', context={'posts': posts, 'user': user_objects})