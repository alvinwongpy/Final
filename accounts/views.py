from genericpath import exists
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.db import models

#from contacts.models import Contact # To add later 

def register(request):
    if request.method == 'POST':
        # get form values
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        # check password
        if password == password2:
            # check username
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username exited !")
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, "User email is being used !")
                    return redirect('register')
                else:
                    # eveerything is fine by now
                    user = User.objects.create_user(
                        username=username,
                        password=password, email=email,
                        first_name=first_name,
                        last_name=last_name)
                    # goto login after register
                    # method 1
                    # auth.login(request, user)
                    # message.success(request, 'You ar now loggging in !')
                    # return redirect(''index)
                    # method 2
                    user.save()
                    messages.success(request, "You are now registered")
                    return redirect('login')
        else:
            messages.error(request, "Password do not match")
            return redirect('register')
    else:
        return render(request, 'accounts/register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        # if not match then return None
        if user is not None:
            auth.login(request, user)
            datafield = User._meta.get_fields()
            print(datafield)
            messages.success(request, 'Hi, You are logging in !')
            return redirect('menu')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')
    else:
        return render(request, 'accounts/login.html') 

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success( request, "you are now logging out !")
        return redirect('menu')
            

# def test(request):
#     #return render(request,'pages/menu.html')
#     return redirect('menu')
