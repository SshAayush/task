from urllib import response
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import redirect, render, get_object_or_404
from .forms import RegistrationForm
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            message = "User created successfully"
            return redirect('login')
        else:
            message = form.errors
    else:
        form = RegistrationForm()
    return render(request,'signup.html',{
        'form': form,
    })

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password1']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('profile')
        else:
            message = "Invalid username or password"
            return render(request, 'login.html',{
                'message': message,
            })

    return render(request, 'login.html')

def logout(request):
    auth_logout(request)
    return redirect('login')

@login_required
def profile(request):
    return render(request,'profile.html')

@login_required
def security(request):
    return render(request,'security.html')

@login_required
def viewUser(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("You are not allowed to access this page.")
    
    # Accessing the User model
    userDetails = User.objects.all()
    currentUser = User.objects.get(username=request.user)
    return render(request,'viewuser.html',{
        'userDetails': userDetails,
        'currentUser': currentUser,
    })

# function to delete a user by id
@login_required
def deleteUser(request, user_id):
    if request.user.is_superuser:
        if request.method == 'POST':
            user = get_object_or_404(User, id=user_id)
            user.delete()
            return redirect('viewuser')
        elif request.method == 'GET':
            return HttpResponseForbidden("You are not allowed to delete this user.")
    return redirect('viewuser')

@login_required
def editUser(request, user_id):
    if request.user.is_staff and request.user.is_superuser:
        user = get_object_or_404(User, id=user_id)
        if request.method == 'POST':
            return HttpResponse("Edit user POST request Invoked") #Incomplete
        else:
            form = RegistrationForm(instance=user)
        return render(request, 'edituser.html', {
            'form': form,
        })