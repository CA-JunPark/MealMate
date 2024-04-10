from django.shortcuts import render
from rest_framework.views import APIView
from post.models import Post
from account.models import Account
from datetime import datetime
from django.core.cache import cache
from django.http import JsonResponse
from django.db.models import Q

class Home(APIView):
    def get(self, request):
        user = request.user
        if user is None:
            return render(request, 'mealmate/login.html')
        
        sortVal = request.GET.get('sortVal')
        searchBy = request.GET.get('searchBy')
        searchVal = request.GET.get('searchVal')
        isUp = request.GET.get('isUp')
        if isUp == 'true':
            isUp = True
        else:
            isUp = False
        
        user_objects = Account.objects.get(email=user.email)
        
        posts_objects = Post.objects.all()
        
        posts = []
        
        for post in posts_objects:
            # if current time is before post.when
            if datetime.strptime(post.when[:-3].replace(" ", "").replace("-", "").replace(":", ""), "%Y%m%d%H%M") > datetime.now():
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
        
       
        return render(request, 'mealmate/home.html', context={'posts': posts, 'user': user_objects})


def searchPost(request):
    print("SEARCH2")
    sortVal = request.GET.get('sortVal')
    searchBy = request.GET.get('searchBy')
    searchVal = request.GET.get('searchVal')
    isUp = request.GET.get('isUp')
    
    if isUp == 'true':
        isUp = True
    else:
        isUp = False

    posts_objects = {}
    print(searchBy)
    if searchBy is None:
        searchBy = "ownerName"
    print(searchVal)
    if searchVal == "":
        posts_objects = Post.objects.all()
    else:
        if searchBy == "ownerName":
            posts_objects = Post.objects.filter(Q(ownerName__icontains=searchVal))
        elif searchBy == "where":
            posts_objects = Post.objects.filter(
                Q(where__icontains=searchVal))
        elif searchBy == "when":
            posts_objects = Post.objects.filter(
                Q(when__icontains=searchVal))
        elif searchBy == "current_user_number":
            posts_objects = Post.objects.filter(
                Q(current_user_number__icontains=searchVal))
        elif searchBy == "max_user_num":
            posts_objects = Post.objects.filter(
                Q(max_user_num__icontains=searchVal))

    posts = []

    for post in posts_objects:
        # if current time is before post.when
        if datetime.strptime(post.when[:-3].replace(" ", "").replace("-", "").replace(":", ""), "%Y%m%d%H%M") > datetime.now():
            owner_object = Account.objects.get(email=post.owner)
            posts.append(dict(id=post.id,
                                owner=post.owner,
                                owner_name=owner_object.username,
                                photo=owner_object.photo,
                                where=post.where,
                                Note=post.Note,
                                current_user_number=post.current_user_number,
                                current_users=post.current_users,
                                max_user_num=post.max_user_num,
                                when=post.when))
        else:  # delete posts that are over
            post.delete()
    # sort
    if sortVal is None:
        sortVal = 'when'

    if isUp is None:
        isUp = False

    posts = sorted(posts, key=lambda item: item[sortVal], reverse=isUp)
    
    return JsonResponse(posts, safe = False)
