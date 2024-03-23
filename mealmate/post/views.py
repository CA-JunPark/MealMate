from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Post
from account.models import Account

class CreatePost(APIView):
    def get(self, request):
        user = request.user
        if user is None:
            return render(request, 'mealmate/login.html')
        return render(request, 'post/createPost.html', context={'user': user})

    def post(self, request):
        owner = request.data.get('owner', None)
        where = request.data.get('where', None)
        when = request.data.get('when', None)
        max_user_num = int(request.data.get('max_user_num', None))
        note = request.data.get('note', None)

        if not owner or not where or not when or not max_user_num:
            return Response(status=500, data=dict(message='Cannot have blank'))
        
        Post.objects.create(owner=owner, where=where, when=when, current_users=owner,max_user_num=max_user_num, Note=note)
        
        return Response(status=200, data=dict(message="Posted"))
                        
class PostMoreInfo(APIView):
    def get(self, request):
        postID = request.GET.get('id')
        selectedPost = Post.objects.get(id=postID)
        owner = Account.objects.get(email=selectedPost.owner)
        name = owner.username
        photo = owner.photo
        current_users = selectedPost.current_users.split(" ")
        for i in range(len(current_users)):
            current_users[i] = Account.objects.get(email=current_users[i]).username
        return render(request, 'post/postMoreInfo.html', context={'post':selectedPost, 'photo':photo, 'name':name, 'current_users': current_users})
    
    def post(self, request):
        """join"""
        id = request.data.get('id', None)
        user = request.user
        post_object = Post.objects.get(id=id)
        
        if user.email == post_object.owner:
            return Response(status=500, data=dict(message='You are already a member'))
        if user.email in post_object.current_users:
            return Response(status=500, data=dict(message='You are already a member'))
        if (post_object.current_user_number == post_object.max_user_num):
            return Response(status=500, data=dict(message='Full'))

        # TODO Need algorithms to reject multiple join in close time

        # add current_user
        post_object.current_users += " " + user.email
        post_object.save()
    
        return Response(status=200, data=dict(message="Joined"))

class MyMeals(APIView):
    def get(self, request):
        
        user = request.user
        
        posts = Post.objects.all().order_by('owner')
        
        myPosts = []
        
        for post in posts:
            if user.email in post.current_users:
                myPosts.append(dict(id=post.id,
                                  owner=post.owner,
                                  owner_name=user.username,
                                  photo=user.photo,
                                  where=post.where,
                                  Note=post.Note,
                                  current_user_number=post.current_user_number,
                                  current_users=post.current_users,
                                  max_user_num=post.max_user_num,
                                  when=post.when))
        
        return render(request, 'post/myMeals.html', context={"posts":myPosts})