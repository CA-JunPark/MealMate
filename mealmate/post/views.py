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
        return render(request, 'post/postMoreInfo.html', context={'post':selectedPost, 'photo':photo, 'name':name})
    
    def post(self, request):
        """join"""
        id = request.data.get('id', None)
        user = request.user
        post_object = Post.objects.get(id=id)
        
        strCurrent_users = post_object.current_users
        
        if user.email == post_object.owner:
            return Response(status=500, data=dict(message='You are already a member'))
        if user.email in post_object.current_users:
            return Response(status=500, data=dict(message='You are already a member'))
        if (post_object.current_user_number == post_object.max_user_num):
            return Response(status=500, data=dict(message='Full'))

        # TODO Need algorithms to reject multiple join in close time

        post_object.current_users += " " + user.email
        
        post_object.save()
    
        return Response(status=200, data=dict(message="Joined"))
        