from django.shortcuts import render, HttpResponse, redirect
from home.models import Contact
from django.contrib import messages
from Blog.models import Blogs
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def home(request):
    return render(request,'home/home.html')

def contact(request, method=['POST','GET']):
    if request.method=='POST':
        name = request.POST['name']
        email = request.POST['email']
        desc  = request.POST['phone']
        phone = request.POST['desc']
        if len(name)>2 and len(email)>2 and len(phone)>9:
            messages.success(request, 'Message sent!')
            contact = Contact(name=name, email=email, phone=phone, desc=desc)
            contact.save()
        else:
            messages.warning(request, 'Pls fill the form properly')
    return render(request,'home/contact.html')

def about(request):
    return render(request,'home/about.html')

def search(request):
    query = request.GET['query']
    if len(query)> 50:
        allPost = Blogs.objects.none()
    else:
        allPostTitle = Blogs.objects.filter(title__icontains=query)
        allPostContent = Blogs.objects.filter(content__icontains=query)
        allPost = allPostTitle.union(allPostContent)

    if allPost.count() == 0:
        messages.warning(request, 'Pls enter some valid query')
    contex = {'allPost':allPost}
    return render(request, 'home/search.html',contex)

#auth api

def SignUpP(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        if pass1 != pass2:
            messages.danger(request,"password dosent match")
            return redirect('home')
        myuser = User.objects.create_user(username, email, pass1)
        myuser.save()
        messages.success(request,"Acount created")
        return redirect('home')
    else:
        return HttpResponse("Not Allowed")

def loginP (request):
    if request.method == 'POST':
        username = request.POST['loginusername']
        pass1 = request.POST['loginpass1']
        
        user = authenticate(username=username, password=pass1)
        
        if user is not None:
            login(request, user)
            messages.success(request, "logged in")
            return redirect('home')
        else:
            messages.danger(request, "Invalid user")
            return redirect('home')

    
def logoutP (request):
    logout(request)
    messages.success(request, "logged out")
    return redirect('home')