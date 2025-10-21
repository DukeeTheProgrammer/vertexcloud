from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, FileResponse
from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from .tools import get_ext, session_key_generator, Hasher
from .models import File
import requests
import random

@csrf_exempt
def api_health(request):
    http_response = False
    models = False
    issues = 0
    try:
        response = requests.get("https://www.googlge.com/")
        if response.status_code==200:
            http_response = True
        else:
            http_response=False
            issues+=1
        files = File.objects.all()
        if files:
            models =True
        else:
            models = False
            issues+=1
    except Exception as e:
        http_response=False
        models=False
    if http_response and models:
        return JsonResponse({"status":True, "request method":"POST" if request.method=="POST" else "GET","message":f"Api is Running Correctly! Api is having {issues} Issue(s)","runtime":"Active", "producer":"DukeeTheProgrammer"})
    else:
        return JsonResponse({"status":True, "request method":"POST" if request.method=="post" else "GET", "message":f"API is having {issues} issue(s)", "runtime":"Active", "producer":"DukeeTheProgrammer"})

#auth ---

@csrf_exempt
def create_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        #check if the credentials exists in the database..
        password_hasher_instance = Hasher()
        hashed_password = password_hasher_instance.hash(password)["hashed_password"]
        print(hashed_password)

        if User.objects.filter(username=username).exists():
            return JsonResponse({"status":False, "message":"Username already Exists"})
        elif User.objects.filter(email=email).exists():
            return JsonResponse({"status":False, "message":"Email Already Exists"})
        else:
            User.objects.create_user(
                    username=username,
                    email=email,
                    password=password
                    )
            request.session["current_user"] = username
            generator = session_key_generator(username)

            detail = request.session["auth"] = {"user":username, "key":generator["generated_key"]}
            return JsonResponse({"status":True, "session":True, "session_name":"current_user", "message":f"New User {username} has been created successfully", "your session key":detail["key"]})
    return JsonResponse({"status":False, "message":"GET request method Not allowed on this Route"})


@csrf_exempt
def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        key = ""
        if user is not None:
            login(request, user)
            user_ = request.session["current_user"] = user.username
            if request.session["auth"]["user"]==user_:
                key="".join(request.session["auth"]["key"])
            generator = session_key_generator(username)
            detail = request.session["auth"] = {
                    "user":username,
                    "key":generator["generated_key"]
                    }

            print(key)
            return JsonResponse({"status":True, "session":True if "current_user" in request.session else False, "session_name":"current_user", "logged_in":True if user.username else False, "user":user.username, "session_key":detail["key"] if detail["user"] else "Forbidden"})
        else:
            return JsonResponse({"status":False, "message":"A severe Error Occured. Could not log you in. Try again", "current_user_status":True if user is not None else False})
    return JsonResponse({"status":False, "message":"GET request method not allowed on this route."})



@csrf_exempt
def add_file(request):
    if request.method == "POST":
        file = request.FILES.get("file")
        key = request.POST.get("key")
        if key != request.session["auth"]["key"]:
            return JsonResponse({"status":False, "message":f"Could not create file : -'{file.name}' - due to Invalid Key! #if you need a new key, use this endpoint '/token/' and register a new key or check if you have an existing one.", "producer":"DukeeTheProgrammer"})
        user = User.objects.filter(username=request.session["auth"]["user"]).first()
        if user is not None:
            filename = file.name
            type = file.content_type
            size = file.size
            print(f"File Recieved : {filename}")
            file = File.objects.create(user=user if user else None,file=file,type=type,size=size, name=filename)
            return JsonResponse({"status":True, "message":"File Created Successfully! and has been saved.", "file_type":type, "filename":filename, "file-type":type, "size":size})
        return JsonResponse({"status":False, "message":"File was not saved Successfully, an error Occured", "producer":"DukeeTheProgrammer","github_handle":"https://github.com/DukeeTheProgrammer/"})
    return JsonResponse({"status":False, "message":"GET method is not allowed on this Route"})


@csrf_exempt
def get_files(request):
    if request.method == "POST":
        session_key = request.POST.get("key")

        if session_key != request.session["auth"]["key"]:
            return JsonResponse({"status":False,"message":"Invalid Key entered For this user. You can use /token/ endpoint to create a new key"})
        username = request.session["auth"]["user"]
        print(username)
        user = User.objects.filter(username=username).first()
        if user is not None:
            files = File.objects.filter(user=user.id).all()
            if not files:
                return JsonResponse({"status":False,"message":"No file is available under this User", "authorization":"user-token" if request.session["auth"]["key"] else "Not authorized", })
            file_dict = {
                    file.name :{
                        "id":file.id,
                        "url":file.file.url,
                        "type":file.type,
                        "size":file.size,
                        "created_at":file.created_at
                        } for file in files
                    }

            return JsonResponse({"file":file_dict})
        return JsonResponse({"status":False, "message":"User credentail is not valid for this Operation"})
    return JsonResponse({"status":False, "message":"GET request is not allowed on this Route"})

@csrf_exempt
def my_key(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")


        user = authenticate(request, username=username, password=password)

        if user is not None:
            #check if previous key exists before deleting
            key = request.session.get("auth")
            if key is not None:
                return JsonResponse({"status":True, "message":"Your Existing Key is still available","key":key["key"]})
            new_key = session_key_generator(username)
            new = request.session["auth"] = {
                    "user":user.username,
                    "key":new_key
                    }
            return JsonResponse({"status":True, "message":"A new key has been created for you", "details":new})
        return JsonResponse({"status":False,"message":"Invalid username or password!"})
    return JsonResponse({"status":False,"message":"Only POST request is available on this route"})


@csrf_exempt
def get_file(request):
    if request.method=="POST":
        return JsonResponse({"status":False, "message":"POST is not allowed on this Route"})
    id = request.GET.get("id")
    token = request.GET.get("token")
    if not token or token !=request.session["auth"]["key"]:
        return JsonResponse({"status":False,"message":"Invalid Token or Did you forget to add your token to your parameters?"})
    try:
        user = User.objects.filter(username=request.session["auth"]["user"]).first()

        if user is not None:
            file = File.objects.filter(user=user.id, id=id).first()
            file_dict ={
                    file.name :{
                        "id":file.id,
                        "url":file.file.url,
                        "type":file.type,
                        "size":file.size,
                        "created_at":file.created_at
                        }
                    }
            return JsonResponse({"file":file_dict})
        return JsonResponse({"status":False, "message":"Invalid Token Key. you can visit '/token/' for a new token key or get your existing ones"})
    except Exception as e:
        return JsonResponse({"status":False, "message":f"{e}"})


@csrf_exempt
def delete_file(request):
    if request.method == "POST":
        return JsonResponse({"status":True, "message":"Resend The request User GET. post is currently not supported.", "authorization":"user-token" if request.session["auth"]["key"] == request.POST.get("key") else "No Authorization. Page content has been locked"})
    key = request.GET.get("key")
    id = request.GET.get("id")
    if not request.user.is_authenticated:
        return JsonResponse({"status":False, "message":"Route is locked due to No login credentials Found. Login to contnue"})

    if not key or key !=request.session["auth"]["key"]:
        return JsonResponse({"status":False, "message":"Invalid Token Key."})
    user = User.objects.filter(username=request.session["auth"]["user"]).first()
    if user is None:
        return JsonResponse({"status":False, "message":"Invalid Token key"})

    #return File properties if file id exists

    file = File(user=user, id=id)
    if file is not None:
        file.delete()
        return JsonResponse({"status":True, "message":f"File with id : '{id}' has been deleted", "authorization": "user-token" if request.session["auth"]["key"] == key else "No Authorization access"})
    return JsonResponse({"status":False, "message":"Could not delete file due to File not ex8sts or invalid id given"})


@csrf_exempt
def remove_session(request):
    key = request.POST.get("key") if request.method=="POST" else request.GET.get("key")
    if key != request.session["auth"]["key"]:
        return JsonResponse({"status":False, "message":"Invalid token Key"})
    if not key:
        return JsonResponse({"status":False, "message":"A token is required to access this Endpoint"})
    username=request.session["auth"]["user"]
    user = User.objects.filter(username=username).first()
    try:
        request.session.flush()
        logout(user)
        return JsonResponse({"status":True, "message":f"User : {user.username} sessions has been Flushed and Now logged out."})
    except Exception as e:
        return JsonResponse({"status":False, "message":f"{e}"})


@csrf_exempt
def delete_user(request):
    key = request.GET.get("key") if request.method=="GET" else request.POST.get("key")
    password = request.GET.get("password") if request.method =="GET" else request.POST.get("password")

    try:
        if not request.user.is_authenticated:
            return JsonResponse({"status":False, "message":"You are not authorized to access this route, you must first be logged in"})
        username = request.user.username
        if username:
            if key == request.session["auth"]["key"]:
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    try:
                        user.delete()
                        request.session.flush()
                        return JsonResponse({"status":True, "message":"User has been Deleted Successfully and all corresponding sessions has been flushed"})
                    except Exception as e:
                        return JsonResponse({"status":False, "message":f"{e}"})
                return JsonResponse({"status":False, "message":"Invalid User Credentials"})
            return JsonResponse({"status":False, "message":"Invalid Key Credential"})
        return JsonResponse({"status":False, "message":"User details is invalid"})
        
    except Exception as e:
        return JsonResponse({"status":False, "message":f"{e}"})


