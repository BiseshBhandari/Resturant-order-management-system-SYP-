"""
URL configuration for foodies project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from orderApp import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.login_user, name='login'),
    path("logout/",views.logout_user, name="logout"),
    path('register/', views.register, name='register'),
    path("home/", views.home, name='home'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('view-cart/', views.view_cart, name='view_cart'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('clear-cart/', views.clear_cart, name='clear_cart'),
    path("adminn/", views.admin_dashboard, name='admins'),
    path('add_product/', views.add_product, name='add_product'),
    path('viewProduct/', views.view_product,name = 'view_product'),
    path('product_delete/<int:product_id>/', views.delete_product, name='delete_product'),
    path('feedback/', views.feedback_page, name='feedback'),
    path('feedbackform/', views.feedback_from, name='feedback_form'),
    path('view-feedback/', views.view_feedback, name='view_feedback'),

] + static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
