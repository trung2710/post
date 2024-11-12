from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views
urlpatterns = [
    path('profile', views.profile_view, name='profile'),
    path('profile/edit',views.profile_edit ,name="profile-edit"),
    path('profile/<username>/', views.profile_view, name='userprofile'),
    path('profile/delete', views.profile_delete_view, name='profile-delete'),
    path('profile/onboarding', views.profile_edit, name='profile-onboarding'),
    
]
