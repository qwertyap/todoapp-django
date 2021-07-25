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
                            request.POST['username'], password=request.POST['password1'])
                        user.save()
                        login(request, user)
                        return redirect('profile')
                    except:
                        pass
                    # except IntegrityError:
                    #     return render(request, 'todo/signupuser.html', {'form': UserCreationForm(), 'error': 'That username has already been taken. Please choose a new username'})
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
            form.save()
            return redirect('currenttodos')
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
        return redirect('currenttodos')


@login_required
def member(request):
    # return render(request, 'todo/member.html')
    # todos = Todo.objects.all()
    l = []
    check_list=[]
    todos = Todo.objects.order_by("-datecompleted")
    for i in todos:
        if i.user not in check_list:
            # print(i.user)
            check_list.append(i.user)
            l.append(i)

    
    return render(request, 'todo/member.html', {'todos': l})


@login_required
def profile(request):
    # form = TodoForm(request.POST)
    # newtodo = form.save(commit=False)
    # newtodo.user = request.user
    # newtodo.save()
    # return redirect('currenttodos')
    # if request.method == 'GET':
    #     return render(request, 'todo/profile.html', {'form': ImageForm()})
    if request.method == "POST":
        form = ImageForm(request.POST, request.FILES)
        newform = form.save(commit=False)
        if form.is_valid():
            newform.user=request.user
            newform.save()
    form = ImageForm()
    images = Image.objects.filter(user=request.user)
    # print(list(images))
    img=""
    for i in images:
        img=i
    return render(request, 'todo/profile.html', {'images': img, 'form': form})
