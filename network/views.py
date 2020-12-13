import datetime
import json

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import UserSerializer, PostSerializer
from django.views.decorators.csrf import csrf_protect, csrf_exempt

from .models import User, user_rel, post 


def index(request):
    data = {'posts':post.objects.all().order_by('-id')[0:5]}
    return render(request, "network/index.html", data)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("discover"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
    else:
        return render(request, "network/register.html")

@csrf_protect
def discover(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            user = request.user.username
            date = datetime.datetime.now()
            image_url = request.POST['image_url']
            body = request.POST['body']
            like_count = None
            dislike_count = None
            new_post = post.objects.create(user=user, date=date, image_url=image_url, body=body, like_count=like_count, dislike_count=dislike_count)
            new_post.save()
            return HttpResponseRedirect(reverse('discover'))
        else:
            try:
                myUsrel = user_rel.objects.get(user=request.user.username)
            except user_rel.DoesNotExist:
                newRelation = user_rel.objects.create(user=request.user.username)
            finally:
                return render(request, "network/post_feed.html")
    else:
        HttpResponseRedirect(reverse('index'))

def profile(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            return HttpResponse('Http method not valid.')
        else:
            context = {
                'user': request.user.username,
                'following': user_rel.objects.get(user=request.user.username).follows_json
                }
            return render(request, "network/profile.html", context)
    else:
        return HttpResponseRedirect(reverse('index'))

def user_profile(request, username):
    if request.user.is_authenticated:
        if request.method == 'PUT':
            data = json.loads(request.body)
            try:
                followerObj = user_rel.objects.get(user=data['follower'])
                followersArr = followerObj.follows_json.split(',')
                if data['user'] in followersArr:
                    followersArr.remove(data['user'])
                    followersArr = list(filter(None, followersArr))
                    followersStr = ','.join(followersArr)
                    followerObj.follows_json = followersStr
                    followerObj.save()
                    responseJson = {'user':followerObj.user,'Status':'ok','NewRelation':False,'Event':'unfollow', 'following': followerObj.follows_json.split(',')}
                    return JsonResponse(responseJson, safe=False)
                else:
                    newFollowers = followersArr + [data['user']]
                    followersStr = ','.join(newFollowers)
                    followerObj.follows_json = followersStr
                    followerObj.save()
                    responseJson = {'user':followerObj.user, 'Status':'ok', 'NewRelation':False, 'Event':'follow','following':followerObj.follows_json.split(',')}
                    return JsonResponse(responseJson, safe=False)
            except user_rel.DoesNotExist:
               newRelation = user_rel.objects.create(user=data['follower'], follows_json=data['user'])
               newRelation.save()
               confirmationJson = {'user':followerObj.user,'Status':'ok','NewRelation':True,'Event':'follow'}
               return JsonResponse(confirmationJson, safe=False)
################# /*FOLLOWERS SECTION SCRAPED DUE TIME SHORAGE AND ENGINEERING FINALS*/ ###################
#            finally:
#               try:
#                    followingObj = user_rel.objects.get(user=data['follower'])
#                    followsArr = followingObj.follows_json.split(',')
#                    responseJson = {'user':followingObj.user}
#                    return JsonResponse(responseJson, safe=False)
#                except user_rel.DoesNotExist:
#                    newRelation = user_rel.objects.create(user=data['follower'], follows_json=data['user'])
#                    confirmationJson = {'Status':'ok'}
#                    return JsonResponse(confirmationJson, safe=False)
        else:
            user_exist = User.objects.filter(username=username).first()
            try:
                initial_followers = user_rel.objects.filter(user=username).first()
            except user_rel.DoesNotExist:
                newRelation = user_rel.objects.create(user=username)
            finally:
                if user_exist is not None:
                    if username == request.user.username:
                        return HttpResponseRedirect(reverse("profile"))
                    else:
                        context = {
                            'user': username,
                            'exist': user_exist,
                            'following': user_rel.objects.filter(user=username).first().follows_json,
                            'followers': user_rel.objects.get(user=request.user.username).follows_json
                            }
                        return render(request, "network/profile.html", context)
                else:
                    return HttpResponseRedirect(reverse("profile"))
    else:
        return HttpResponseRedirect(reverse("index"))


def api(request):
    if request.method == "POST":
        try:
            usrdata = json.loads(request.body)
            dataUsers = []
            try:
                for usrdata in usrdata:
                    dataUsers.append(usrdata)
            finally:
                post_data = post.objects.all().filter(user__in=dataUsers).order_by('-id')
                data = []
                for post_data in post_data:
                    json_obj = {
                        'id': post_data.id,
                        'user': post_data.user,
                        'date': post_data.date,
                        'image_url': post_data.image_url,
                        'body': post_data.body,
                        'like_count': post_data.like_count,
                        'dislike_count': post_data.dislike_count,
                        }
                    data.append(json_obj)
        finally:
            return JsonResponse(data, safe=False)
    else:
        post_data = post.objects.all().order_by('-id')
        data = []
        for post_data in post_data:
            json_obj = {
                'id': post_data.id,
                'user': post_data.user,
                'date': post_data.date,
                'image_url': post_data.image_url,
                'body': post_data.body,
                'like_count': post_data.like_count,
                'dislike_count': post_data.dislike_count,
            }
            data.append(json_obj)
        return JsonResponse(data, safe=False)

def api_usr(request, username):
    if request.method == "POST":
        return "none"
    else:
        post_data = post.objects.filter(user=username).order_by('-id')
        data = []
        for post_data in post_data:
            json_obj = {
                'id': post_data.id,
                'user': post_data.user,
                'date': post_data.date,
                'image_url': post_data.image_url,
                'body': post_data.body,
                'like_count': post_data.like_count
                }
            data.append(json_obj)
        return JsonResponse(data, safe=False)

@csrf_exempt
def interaction(request, post_id):
    post_data = post.objects.get(id=post_id)
    json_obj = {
        'id': post_data.id,
        'user': post_data.user,
        'date': post_data.date,
        'image_url': post_data.image_url,
        'body': post_data.body,
        'like_count': post_data.like_count,
        'dislike_count': post_data.dislike_count,
        }
    if post_data is not None:
        if request.method == "PUT":
            data = json.loads(request.body)
            user = data['user']
            if post_data.like_count is None:
                post_data.like_count = user
                post_data.save()
                return JsonResponse(post_data.user, safe=False)
            else: 
                likes_arr = post_data.like_count.split(',')
                dislikes = post_data.dislike_count
                if data['like'] is True:
                    if user in likes_arr:
                        likes_arr.remove(user)
                        likes_arr = list(filter(None, likes_arr))
                        save_as_str = ','.join(likes_arr)
                        post_data.like_count = save_as_str
                        post_data.save()
                        return JsonResponse(save_as_str, safe=False)
                    else:
                        append_like = likes_arr + [user]
                        save_as_str = ','.join(append_like)
                        post_data.like_count = save_as_str
                        post_data.save()
                        return JsonResponse(save_as_str, safe=False)
                else:
                    return HttpResponse("An error has occurred.")
            return HttpResponse(status=204)
        else:
            return JsonResponse(json_obj, safe=False)
    else:
        return HttpResponse('Post does not exist, try other one.')

def edit_post(request, post_id):
    if request.user.is_authenticated:
        post_data = post.objects.get(id=post_id)
        if post_data.user == request.user.username:
            if request.method == 'GET':
                post_context = {
                    'post': post_data,
                    'user': request.user.username
                }
                return render(request, 'network/edit_post.html', post_context)
            elif request.method == 'POST':
                image_url = request.POST['image_url']
                body = request.POST['post_body']
                post_data.image_url = image_url
                post_data.body = body
                post_data.save()
                return HttpResponseRedirect('/profile#'+str(post_data.id))
            else:
                return HttpResponse('Not valid HTTP method.')
        else:
            return HttpResponse('This is not your post, therefore you cannot edit it.')
    else:
        return HttpResponse(reverse('index'))       
