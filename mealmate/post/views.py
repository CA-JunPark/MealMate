from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Post
from account.models import Account
from datetime import datetime
from django.contrib.messages import error

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
        when = when.replace(":","")
        date = request.data.get('date', None)
        date = date.replace("-","")
        when = date+when
        max_user_num = int(request.data.get('max_user_num', None))
        note = request.data.get('note', None)

        if not owner or not where or not when or not max_user_num:
            return Response(status=500, data=dict(message='Cannot have blank'))
        
        time = datetime.strptime(when, "%Y%m%d%H%M")
        if time < datetime.now():
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
            t1 = datetime.strptime(mp.when[:-3].replace(" ", "").replace("-", "").replace(":", ""), "%Y%m%d%H%M")
            if time.date() == t1.date():
                t1_s = t1.hour * 3600 + t1.minute * 60 + t1.second
                if abs(t1_s - t2_s) < 1800:
                    return Response(status=500, data=dict(message='You are in the another meal that is close to this'))
        Post.objects.create(owner=owner, ownerName=ownerName, where=where, when=time, current_users=owner,max_user_num=max_user_num, Note=note)
        
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
                                                                  'postID': postID,
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

        all_posts = Post.objects.all()
        myPosts = []
        for p in all_posts:
            if user.email in p.current_users:
                myPosts.append(p)
        # compare each time then reject if within 30min
        time = datetime.strptime(
            post_object.when[:-3].replace(" ", "").replace("-", "").replace(":", ""), "%Y%m%d%H%M")
        t2_s = time.hour * 3600 + time.minute * 60 + time.second
        for mp in myPosts:
            t1 = datetime.strptime(
                mp.when[:-3].replace(" ", "").replace("-", "").replace(":", ""), "%Y%m%d%H%M")
            if time.date() == t1.date():
                t1_s = t1.hour * 3600 + t1.minute * 60 + t1.second
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
            if datetime.strptime(post.when[:-3].replace(" ", "").replace("-", "").replace(":", ""), "%Y%m%d%H%M") > datetime.now():
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

class EditPost(APIView):
    def get(self, request):
        user = request.user
        id = request.GET.get('id')
        post = Post.objects.get(id=id)
        
        where = post.where
        when = post.when
        date = when[:10]
        when = when[11:]
        
        max = post.max_user_num
        note = post.Note

        return render(request, 'post/editPost.html', context={"id": id, "owner": post.owner, "where": where, "when": when, "date": date, "max": max, "note": note})

    def post(self, request):
        user = request.user
        id = request.data.get('id', None)
        owner = request.data.get('owner', None)
        where = request.data.get('where', None)
        when = request.data.get('when', None)
        when = when.replace(":", "")
        if (len(when) > 4):
            when = when[:4]
        date = request.data.get('date', None)
        date = date.replace("-", "")
        when = date+when
        note = request.data.get('note', None)
        max_user_num = int(request.data.get('max_user_num', None))
        
        if owner != user.email:
            return Response(status=500, data=dict(message="You are not the owner of this post"))
        
        time = datetime.strptime(when, "%Y%m%d%H%M")
        
        all_posts = Post.objects.exclude(id=id)
        myPosts = []
        for p in all_posts:
            if user.email in p.current_users:
                myPosts.append(p)
        # compare each time then reject if within 30min
        t2_s = time.hour * 3600 + time.minute * 60 + time.second
        for mp in myPosts:
            t1 = datetime.strptime(
                mp.when[:-3].replace(" ", "").replace("-", "").replace(":", ""), "%Y%m%d%H%M")
            if time.date() == t1.date():
                t1_s = t1.hour * 3600 + t1.minute * 60 + t1.second
                if abs(t1_s - t2_s) < 1800:
                    return Response(status=500, data=dict(message='You are in the another meal that is close to this'))
        
        post = Post.objects.get(id=id)
        
        post.where = where
        post.when = time
        post.Note = note
        post.max_user_num = max_user_num
        
        post.save()
        
        return Response(status=200, data=dict(message="Edited"))
