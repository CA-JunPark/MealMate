from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Post
from account.models import Account
from datetime import datetime
from django.http import JsonResponse

class CreatePost(APIView):
    def get(self, request):
        user = request.user
        if user is None:
            return render(request, 'mealmate/login.html')
        return render(request, 'post/createPost.html', context={'user': user})

    def post(self, request):
        owner = request.data.get('owner', None)
        ownerName = Account.objects.get(email=owner).username
        where = request.data.get('where', None)
        when = request.data.get('when', None)
        max_user_num = int(request.data.get('max_user_num', None))
        note = request.data.get('note', None)

        if not owner or not where or not when or not max_user_num:
            return Response(status=500, data=dict(message='Cannot have blank'))
        
        time = datetime.strptime(when, "%H:%M").time()
        if time < datetime.now().time():
            return Response(status=500, data=dict(message='Please set time in the future'))
        
        # get all this user's meals
        user = request.user
        all_posts = Post.objects.all()
        myPosts = []
        for p in all_posts:
            if user.email in p.current_users:
                myPosts.append(p)
        # compare each time then reject if within 30min
        
        t2_s = time.hour * 3600 + time.minute * 60 + time.second
        for mp in myPosts:
            t1 = mp.when
            t1_s = t1.hour * 3600 + t1.minute * 60 + t1.second
        
            if abs(t1_s - t2_s) < 1800:
                return Response(status=500, data=dict(message='You are in the another meal that is close to this'))

        Post.objects.create(owner=owner, ownerName=ownerName, where=where, when=when, current_users=owner,max_user_num=max_user_num, Note=note)
        
        return Response(status=200, data=dict(message="Posted"))
                        
class PostMoreInfo(APIView):
    def get(self, request):
        postID = request.GET.get('id')
        selectedPost = Post.objects.get(id=postID)
        owner = Account.objects.get(email=selectedPost.owner)
        name = owner.username
        photo = owner.photo
        current_users = selectedPost.current_users.split(" ")
        ownerEmail = selectedPost.owner
        
        memberInfo = []

        for n in range(len(current_users)):
            memberObject = Account.objects.get(email=current_users[n])
            # convert email to its username
            current_users[n] = memberObject.username
            if n != 0: # Skip owner
                # get member photos
                memberInfo.append(
                    (current_users[n], memberObject.photo, memberObject.email))
                
        return render(request, 'post/postMoreInfo.html', context={'post': selectedPost, 
                                                                  'ownerPhoto': photo, 
                                                                  'ownerName': name, 
                                                                  'current_users': current_users, 
                                                                  'memberInfo': memberInfo, 
                                                                  'ownerEmail': ownerEmail})
    
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

        # get all this user's meals
        all_posts = Post.objects.all()
        myPosts = []
        for p in all_posts:
            if user.email in p.current_users:
                myPosts.append(p)
        # compare each time then reject if within 30min
        for mp in myPosts:
            t1 = mp.when
            t2 = post_object.when
            t1_s = t1.hour * 3600 + t1.minute * 60 + t1.second
            t2_s = t2.hour * 3600 + t2.minute * 60 + t2.second
            
            if abs(t1_s - t2_s) < 1800: 
                return Response(status=500, data=dict(message='You are in the another meal that is close to this'))

        if post_object.current_user_number == post_object.max_user_num:
            return Response(status=500, data=dict(message='This group is full'))
        
        # add current_user
        post_object.current_users += " " + user.email
        post_object.current_user_number += 1
        post_object.save()
    
        return Response(status=200, data=dict(message="Joined"))

    def patch(self, request):
        """Leave"""
        
        user = request.user
        
        userEmail = user.email
        
        currentPostID = request.data.get('id', None)

        post = Post.objects.get(id=currentPostID)
        
        if post.owner == user.email:
            return Response(status=500, data=dict(message="Owner of the post cannot leave the post"))
        
        memberEmails = post.current_users
        
        if (" " + userEmail) in memberEmails:
            memberEmails = memberEmails.replace(" " + userEmail, "")
            post.current_users = memberEmails
            post.current_user_number -= 1
            post.save()
            return Response(status=200, data=dict(message="Leaved"))
        else:
            return Response(status=500, data=dict(message="You are not the member of this post"))
    
class MyMeals(APIView):
    def get(self, request):
        
        user = request.user
        
        posts = Post.objects.all().order_by('owner')
        
        myPosts = []
        
        for post in posts:
            if post.when > datetime.now().time():
                if user.email in post.current_users:
                    ownerObject = Account.objects.get(email=post.owner)
                    myPosts.append(dict(id=post.id,
                                    owner=post.owner,
                                    owner_name=ownerObject.username,
                                    photo=ownerObject.photo,
                                    where=post.where,
                                    Note=post.Note,
                                    current_user_number=post.current_user_number,
                                    current_users=post.current_users,
                                    max_user_num=post.max_user_num,
                                    when=post.when))
            else:  # delete posts that are over
                post.delete()
        return render(request, 'post/myMeals.html', context={"posts":myPosts})
    