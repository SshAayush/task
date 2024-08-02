from django.urls import include, path
from . import views


urlpatterns = [
    path('', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout, name='logout'),
    path('security/', views.security, name='security'),
    path('viewuser/', views.viewUser, name='viewuser'),
    path('deleteuser/<int:user_id>', views.deleteUser, name='deleteuser'),
    path('edituser/<int:user_id>', views.editUser, name='edituser'),
]