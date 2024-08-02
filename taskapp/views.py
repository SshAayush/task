from urllib import response
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import redirect, render, get_object_or_404
from .forms import RegistrationForm,ProfilePictureForm
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib import messages
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
    # used to access current user
    user=request.user
    userDetail = User.objects.get(username=request.user)
    try:
        # access the additional details of the user from models
        additionalUserDetail = UserProfile.objects.get(user=request.user)
        
        status = "Admin" if user.is_superuser else "Staff" if user.is_staff else "User"
    except UserProfile.DoesNotExist:
        additionalUserDetail = None
    
    # to update the user details
    if request.method == 'POST':
        if 'profile_picture' in request.FILES:
            form = ProfilePictureForm(request.POST, request.FILES, instance=request.user.userprofile)
            if form.is_valid():
                form.save()
                messages.success(request, 'Profile picture updated successfully')
            else:
                messages.error(request, 'Failed to upload image')
                
        username = request.POST.get('username', '').strip()
        # check whether the username is filled or not
        if username:
            # username = request.POST['username']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            company_name = request.POST['company_name']
            location = request.POST['location']
            email = request.POST['email']
            birthdate = request.POST['birthdate']
            phone = request.POST['phone']
            
            #to update the user details
            user = User.objects.get(username=request.user)
            # user.username = username
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.save()
            
            #to update the additional details of the user
            try:
                additionalUserDetail = UserProfile.objects.get(user=request.user)
                additionalUserDetail.company_name = company_name
                additionalUserDetail.location = location
                additionalUserDetail.birthdate = birthdate
                additionalUserDetail.phone = phone
                additionalUserDetail.save()
            except UserProfile.DoesNotExist:
                UserProfile.objects.create(user=request.user, company_name=company_name, location=location, birthdate=birthdate, phone=phone)
        return redirect('profile')
                
    form = ProfilePictureForm(instance=request.user.userprofile)
         
    return render(request,'profile.html',{
        'userDetail': userDetail,
        'additionalDetail':additionalUserDetail,
        'status':status,
        'form':form,
    })

# to change the password by user
@login_required
def security(request):
    return render(request,'security.html')

#to list all the users in the system
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