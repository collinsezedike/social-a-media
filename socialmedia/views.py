from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import Profile, Chat, Message

from random import randrange

# Create your views here.
@login_required(login_url="signin")
def index(request):
    current_user = auth.get_user(request)
    user_profile = Profile.objects.get(user=current_user)
    chats = Chat.objects.filter(user=current_user).all()
    context = {
        "user_profile": user_profile,
        "chats": chats
    }
    return render(request, "index.html", context=context)


def signup(request):
    if request.method == "POST":
        username = request.POST["username"].lower()
        email = request.POST["email"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]
        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.info(request, "Username taken")
                return redirect("signup")
            else:
                if User.objects.filter(email=email).exists():
                    messages.info(request, "An account with that email already exists. Sign in instead")
                    return redirect("signin")
                else:
                    new_user = User.objects.create_user(username=username, email=email, password=password)
                    new_user.save()
                    new_profile = Profile.objects.create(user=new_user)
                    new_profile.save()
                    auth.login(request, new_user)
                    return redirect("settings")
        else:
            messages.info(request, "Passwords do not match")
            return redirect("signup")
    else:
        return render(request, "signup.html")


def signin(request):
    if request.method == "POST":
        username = request.POST["username"].lower()
        password = request.POST["password"]
        
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect("index")
        else:
            messages.info(request, "Invalid username or password")
            return redirect("signin")
    else:
        return render(request, "signin.html")


@login_required(login_url="signin")
def logout(request):
    auth.logout(request)
    return redirect("signin")


@login_required(login_url="signin")
def settings(request):
    user = auth.get_user(request) # or request.user
    user_profile = Profile.objects.get(user=user)
    if request.method == "POST":
        bio = request.POST["bio"]
        location = request.POST["location"]
        profile_image = request.FILES.get("profile_image")
        if profile_image is not None:
            user_profile.profile_img = profile_image
        user_profile.bio = bio
        user_profile.location = location
        user_profile.save()
        return redirect("index")
    else:
        context = {
            "user_profile": user_profile,
        }
        return render(request, "settings.html", context=context)
    

# @login_required(login_url="signin")
def profile(request, username):
    # This is necessary for the navbar links
    current_user = auth.get_user(request) 
    if User.objects.filter(username=current_user.username).exists():
        user = User.objects.get(username=current_user.username)
        user_profile = Profile.objects.get(user=user)
    else:
        user_profile = None
        
    if User.objects.filter(username=username.lower()).exists():
        requested_user = User.objects.get(username=username.lower())
        requested_user_profile = Profile.objects.get(user=requested_user)
    else:
        requested_user_profile = None
        
    context = {
        "username": username,
        "requested_user_profile": requested_user_profile,
        "user_profile" : user_profile
    }
    return render(request, "profile.html", context=context)


def search(request):
    search_term = request.GET["search_term"].lower()
    all_users = User.objects.all().filter(is_staff=False) # it should not get admin users else, it throws a sort of key error
    matching_user_profiles = [Profile.objects.get(user=user) for user in all_users if search_term in user.username]

    # This is necessary for the navbar links
    current_user = auth.get_user(request) 
    if User.objects.filter(username=current_user.username).exists():
        user = User.objects.get(username=current_user.username)
        user_profile = Profile.objects.get(user=user)
    else:
        user_profile = None
        
    context = {
        "user_profile" : user_profile,
        "matching_user_profiles": matching_user_profiles, 
        "search_term": search_term  
    }
    return render(request, "search.html", context=context)


@login_required(login_url="signin")
def chat(request, recipient):   
    if User.objects.filter(username=recipient):
        current_user = auth.get_user(request)
        if current_user.username == recipient:
            context = {
                "current_user": current_user.username,
                "recipient": recipient,
                "invalid_recipient": True
            }
        else:    
            if Chat.objects.filter(user=current_user, recipient_username=recipient).exists():
                chat_with_recipient = Chat.objects.get(user=current_user, recipient_username=recipient)
                my_messages = Message.objects.filter(conversation_id=chat_with_recipient.conversation_id).all()
                context = {
                    "recipient": recipient,
                    "messages": my_messages
                }
            else:
                context = {
                    "recipient": recipient,
                    "messages": None
                }
    else:
        context = {
            "recipient": recipient,
            "invalid_recipient": True
        }
    return render(request, "chat.html", context=context)


def send_message(request):
    current_user = auth.get_user(request)
    recipient = request.POST["recipient"]
    message = request.POST["message"]
    
    # check if there is a chat object for this conversation
     
    if Chat.objects.filter(user=current_user, recipient_username=recipient).exists():
        chat_object = Chat.objects.get(user=current_user, recipient_username=recipient)
        new_message = Message.objects.create(sender=current_user.username, recipient=recipient, message=message, conversation_id=chat_object.conversation_id)
        new_message.save()
    else:
        recipient_user_obj = User.objects.get(username=recipient)
        recipient_profile_obj = Profile.objects.get(user=recipient_user_obj)
        new_chat_obj_for_current_user = Chat.objects.create(
            user=current_user, 
            recipient_username=recipient_user_obj.username,
            recipient_profile_img=recipient_profile_obj.profile_img.url,
            conversation_id=randrange(100000, 10000000)
            )
        new_chat_obj_for_current_user.save()
        
        current_user_profile_obj = Profile.objects.get(user=current_user)
        new_chat_obj_for_recipient = Chat.objects.create(
            user=recipient_user_obj, 
            recipient_username=current_user.username,
            recipient_profile_img=current_user_profile_obj.profile_img.url,
            conversation_id=new_chat_obj_for_current_user.conversation_id
            )
        new_chat_obj_for_recipient.save()
        
        new_message = Message.objects.create(
            sender=current_user.username, 
            recipient=recipient, 
            message=message, 
            conversation_id=new_chat_obj_for_current_user.conversation_id
            )
        new_message.save()
    return redirect("chat", recipient=recipient)

    