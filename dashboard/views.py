from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from user.models import User
from task.models import Task
from django.db.models import Q

def login_(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.role != 'user':
            login(request, user)
            return redirect('users')
        return redirect('login')
    return render(request, 'login.html')

@login_required(login_url='login')
def logout_(request):
    logout(request)
    return redirect("login")

@login_required(login_url='login')
def users(request):
    user = User.objects.filter(role='user')
    return render(request, 'user.html', {"users": user})

@login_required(login_url='login')
def create_user(request):
    admins = User.objects.filter(role='admin')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        assigned_to = request.POST.get('assigned_to')
        admin = User.objects.get(id=assigned_to)
        user = User(username=username, role="user", assigned_to=admin)
        user.set_password(password)
        user.save()
        return redirect('users')
    return render(request, 'create_user.html', {"admins": admins})

@login_required(login_url='login')
def delete_user(request, id):
    User.objects.get(id=id).delete()
    return redirect('users')

@login_required(login_url='login')
def admins(request):
    user = request.user
    if user.role != 'superadmin':
        return redirect('users')
    admins = User.objects.filter(role='admin')
    return render(request, 'admin.html', {"admins": admins})

@login_required(login_url='login')
def create_admin(request):
    user = request.user
    if user.role != 'superadmin':
        return redirect('users')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        admin = User(username=username, role="admin")
        admin.set_password(password)
        admin.save()
        return redirect('admins')
    return render(request, 'create_admin.html')

@login_required(login_url='login')
def delete_admin(request, id):
    user = request.user
    if user.role != 'superadmin':
        return redirect('users')
    User.objects.get(id=id).delete()
    return redirect('admins')

@login_required(login_url='login')
def tasks(request):
    user = request.user
    q = Q(status__in=['pending', 'progress'])
    if user.role == 'admin':
        q &= Q(created_by=user)
    tasks = Task.objects.filter(q)
    return render(request, 'task.html', {"tasks": tasks})

@login_required(login_url='login')
def create_task(request):
    admin = request.user
    admins = User.objects.filter(role='user')
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        assigned_to = request.POST.get('assigned_to')
        due_date = request.POST.get('due_date')
        user = User.objects.get(id=assigned_to)
        created_by = admin if admin.role == 'admin' else user.assigned_to
        task = Task.objects.create(title=title, description=description, due_date=due_date, assigned_to=user, created_by=created_by)
        task.save()
        return redirect('tasks')
    return render(request, 'create_task.html', {"admins": admins})

@login_required(login_url='login')
def delete_task(request, id):
    user = request.user
    if user.role != 'admin':
        return redirect('tasks')
    Task.objects.get(id=id).delete()
    return redirect('tasks')

@login_required(login_url='login')
def task_reports(request):
    user = request.user
    q = Q(status='completed')
    if user.role == 'admin':
        q &= Q(created_by=user)
    tasks = Task.objects.filter(q)
    return render(request, 'task_report.html', {"tasks": tasks})