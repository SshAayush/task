from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import redirect, render, get_object_or_404
from .forms import RegistrationForm,ProfilePictureForm, UserProfileForm, UserUpdateForm, CustomPasswordChangeForm
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout, update_session_auth_hash
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
            messages.success(request, 'User created successfully')
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
                for field, errors in form.errors.items():
                    for error in errors:
                        if isinstance(error, str):
                            messages.error(request, f"{field.capitalize()}: {error}")
                        else:
                            messages.error(request, f"{field.capitalize()}: Invalid data")

                
        username = request.POST.get('username', '').strip()
        # check whether the username is filled or not
        if username:
            user_form = UserUpdateForm(request.POST, instance=user)
            profile_form = UserProfileForm(request.POST, instance=additionalUserDetail)

            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                messages.success(request, 'Profile updated successfully')
                return redirect('profile')
            else:
                # send form errors and add them to messages
                for form in [user_form, profile_form]:
                    for field, errors in form.errors.items():
                        for error in errors:
                            if isinstance(error, str):
                                messages.error(request, f"{field.capitalize()}: {error}")
                            else:
                                messages.error(request, f"{field.capitalize()}: Invalid data")
    
        # user_form = UserUpdateForm(instance=user)
        # profile_form = UserProfileForm(instance=additionalUserDetail)
            
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
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # To keep the user logged in after password change
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{form.fields[field].label}: {error}")
    else:
        form = CustomPasswordChangeForm(request.user)
    
    return render(request, 'security.html', {'form': form})

#to list all the users in the system
@login_required
def viewUser(request):
    if not request.user.is_staff and not request.user.is_superuser:
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
    currentUser = User.objects.get(username=request.user)
    if request.user.is_superuser or currentUser.id == user_id: #only superuser can delete other users and user can delete himself
        if request.method == 'POST':
            user = get_object_or_404(User, id=user_id)
            user.delete()
            if currentUser.id == user_id: #return to login page if the user deletes himself
                return redirect('logout')
            return redirect('viewuser')
        elif request.method == 'GET':
            return HttpResponseForbidden("You are not allowed to delete this user.")
    return redirect('viewuser')

# used to redirect to user edit page with respective user details
@login_required
def viewUserEdit(request,user_id):
    if request.user.is_staff or request.user.is_superuser:
        user = User.objects.get(id=user_id)
        try:
        # access the additional details of the user from models
            additionalUserDetail = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            additionalUserDetail = None 
        return render(request, 'edituser.html',{
            'userDetail': user,
            'additionalDetail': additionalUserDetail,
        })
    return redirect('profile')

@login_required
def editUser(request, user_id):
    if request.user.is_staff or request.user.is_superuser:
        user = get_object_or_404(User, id=user_id)
        try:
            additionalUserDetail = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            additionalUserDetail = None

        if request.method == 'POST':
            user_form = UserUpdateForm(request.POST, instance=user)
            profile_form = UserProfileForm(request.POST, request.FILES, instance=additionalUserDetail)
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                messages.success(request, 'User details updated successfully.')
                return redirect('viewuseredit', user_id=user_id)
            else:
                for field, errors in user_form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")
                for field, errors in profile_form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")
        else:
            user_form = UserUpdateForm(instance=user)
            profile_form = UserProfileForm(instance=additionalUserDetail)

        return render(request, 'edituser.html', {
            'userDetail': user,
            'additionalDetail': additionalUserDetail,
        })
    return redirect('viewuseredit', user_id=user_id)