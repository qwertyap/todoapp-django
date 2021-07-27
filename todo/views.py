from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm, ImageForm
from .models import Todo, Image
from django.utils import timezone
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'todo/home.html')


def signupuser(request):
    if request.method == 'GET':
        return render(request, 'todo/signupuser.html', {'form': UserCreationForm()})
    else:

        #     # try:
        if request.POST['username'] == "":
            return render(request, 'todo/signupuser.html', {'form': UserCreationForm(), 'error': 'Please enter some username'})

        if request.POST['username'] is not None:
            try:
                if User.objects.get(username=request.POST['username']):
                    return render(request, 'todo/signupuser.html', {'form': UserCreationForm(), 'error': 'Username Already Exists'})
            except:
                if request.POST['password1'] == "" or request.POST['password2'] == "":
                    return render(request, 'todo/signupuser.html', {'form': UserCreationForm(), "username": request.POST['username'], "uservalid": "Username Available", 'error': 'You must enter some password'})
                elif (request.POST['password1'] == request.POST['password2']):
                    try:
                        user = User.objects.create_user(
                            request.POST['username'], password=request.POST['password1'], first_name=request.POST['first_name'], last_name=request.POST['last_name'])
                        user.save()
                        login(request, user)
                        return redirect('profile')
                    except:
                        return render(request, 'todo/signupuser.html', {'form': UserCreationForm(), 'error': 'Some Error occured try again please.'})
                else:
                    return render(request, 'todo/signupuser.html', {'form': UserCreationForm(), "username": request.POST['username'], "uservalid": "Username Available", 'error': 'Passwords did not match'})


def loginuser(request):
    if request.method == 'GET':
        return render(request, 'todo/loginuser.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todo/loginuser.html', {'form': AuthenticationForm(), 'error': 'Username and password did not match'})
        else:
            login(request, user)
            return redirect('profile')


@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


@login_required
def createtodo(request):
    if request.method == 'GET':
        return render(request, 'todo/createtodo.html', {'form': TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
           
            newtodo = form.save(commit=False)
            newtodo.datecompleted = timezone.now()
            newtodo.user = request.user
            newtodo.save()
            return redirect('member')
        except ValueError:
            return render(request, 'todo/createtodo.html', {'form': TodoForm(), 'error': 'Bad data passed in. Try again.'})


@login_required
def currenttodos(request):
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'todo/currenttodos.html', {'todos': todos})


@login_required
def completedtodos(request):
    todos = Todo.objects.filter(
        user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'todo/completedtodos.html', {'todos': todos})


@login_required
def viewtodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'GET':
        form = TodoForm(instance=todo)
        return render(request, 'todo/viewtodo.html', {'todo': todo, 'form': form})
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            # form.datecompleted = timezone.now()
            form.save()
            return redirect('member')
        except ValueError:
            return render(request, 'todo/viewtodo.html', {'todo': todo, 'form': form, 'error': 'Bad info'})


@login_required
def completetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.datecompleted = timezone.now()
        todo.save()
        return redirect('currenttodos')


@login_required
def deletetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('completedtodos')


@login_required
def member(request):
    # return render(request, 'todo/member.html')
    # todos = Todo.objects.all()
    # images = Image.objects.filter(user=request.user)
    
    todo = []
    check_list=[]
    todos = Todo.objects.order_by("-datecompleted")
    for i in todos:
        if i.user not in check_list:
            # print(i.user)
            check_list.append(i.user)
            todo.append(i)
    # print("yo",check_list)
    img=[]
    for i in check_list:
        # images = Image.objects.filter(user=i).order_by('-date')
        imgaes=""
        images = Image.objects.filter(user=i).order_by('-date')
        # print(images.values())
        if images:
            for i in images:
                img.append(i)
                break
        else:
            img.append(0)
        # print(img)
    
    # user1 = User.objects.all()
    # temp_userlist = []
    # userlist = []
    # for i in user1:
    #     if i.username in check_list:
    #         userlist.append(i)

        # print((user_name).user)
    
    img_todo = []
    for i in range(len(todo)):
        img_todo.append((todo[i], img[i]))
        # print((todo[i], img[i]))
    
        
    # images = Image.objects.filter(user=request.user)
    # print(images.values())
    # img = []
    # # imguser = []
    # for i in images:
    #     if 
    #     img.append(i)

    return render(request, 'todo/member.html', {'todos': todo, "images": img, "img_todo": img_todo})


@login_required
def profile(request):
    # user1 = User.objects.filter(user=request.user)
    # print((User.user))
    user1 = User.objects.all()
    currentuser="a"
    usernow = str(request.user)

    for i in user1:
        # print("1st")
        # print(type(i.username))
        # print(type(usernow))
        if i.username == usernow:
            currentuser = i
    print(currentuser.first_name)
    if request.method == "POST":
        form = ImageForm(request.POST, request.FILES)
        newform = form.save(commit=False)
        newform.user=request.user
        newform.save()
    form = ImageForm()
    images = Image.objects.filter(user=request.user)
    # print((images).values())
    img=""
    for i in images:
        img=i
    return render(request, 'todo/profile.html', {'images': img, 'form': form, "currentuser": currentuser})
