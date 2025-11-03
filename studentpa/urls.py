"""
URL configuration for studentpa project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from accommodations import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.landing_page, name='home'),

    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('register/role/', views.register_role_selection, name='register_role_selection'),
    path('register/student/', views.register_student, name='register_student'),
    path('register/landlord/', views.register_landlord, name='register_landlord'),

    # Accommodation URLs
    path('dashboard/profile/', views.landlord_profile_update, name='landlord_profile_update'),
    path('accommodations/', views.accommodation_list, name='accommodation_list'),
    path('accommodations/<int:pk>/', views.accommodation_detail, name='accommodation_detail'),
    path('dashboard/', views.landlord_dashboard, name='landlord_dashboard'),
    path('dashboard/accommodation/new/', views.accommodation_create, name='accommodation_create'),
    path('dashboard/accommodation/<int:pk>/edit/', views.accommodation_update, name='accommodation_update'),
    path('dashboard/accommodation/<int:pk>/delete/', views.accommodation_delete, name='accommodation_delete'),
    path('dashboard/accommodation/<int:pk>/preview/', views.accommodation_preview, name='accommodation_preview'),


     # Content pages
    path('terms/', views.terms_and_conditions, name='terms_and_conditions'),
    path('privacy/', views.privacy_policy, name='privacy_policy'),
    path('about/', views.about_us, name='about_us'),
    path('safety/', views.safety_guidelines, name='safety_guidelines'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)