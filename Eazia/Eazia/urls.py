"""
URL configuration for Eazia project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import include, path
from django.conf import settings

from pages.views import home_view, about_view, login_view, loged_view, post_view, posting_view

urlpatterns = [
    path('/admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('about/', about_view, name="about"),
    path('login/', login_view, name="login"),
    path('users/sign_in/', loged_view, name="sign_in"),
    path('posts/', post_view, name="posts"),
    path('posting/', posting_view, name="create"),
]
