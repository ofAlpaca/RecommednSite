"""RecommendSite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf import settings
from django.views.static import serve
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
import article.views as article_view
import ckeditor_uploader.views as ck_view
import article.regbackend as reg_view

urlpatterns = [
    re_path(r'^$',
        article_view.home_page,
        name='index'),

    re_path(r'^accounts/register/',
        reg_view.MyRegistrationView.as_view(), 
        name='registration_register'),

    re_path(r'^accounts/profile/',
        article_view.profile,
        name='profile'),

    path('accounts/<int:pk>/',
        article_view.status,
        name='status'),

    re_path(r'^accounts/',
        include('registration.backends.simple.urls')),

    path('article/<int:pk>/edit/', 
        article_view.post_edit_article,
        name='post_edit_article'),

    path('article/<int:pk>/', 
        article_view.post_article,
        name='post_article'),

    path('article/<int:pk>/remove', 
        article_view.delete_own_article,
        name='delete_own_article'),

    path('article/new/', 
        article_view.post_new_article,
        name='post_new_article'),

    re_path(r'^ckeditor/', 
        include('ckeditor_uploader.urls')),

    re_path(r'^comments/delete_own/(?P<id>.*)/$',
        article_view.delete_own_comment,
        name='delete_own_comment'),

    re_path(r'^comments/',
        include('django_comments.urls')),

    re_path(r'^login/',
        auth_views.login,
        name='login'),

    re_path(r'^admin/',
        admin.site.urls,
        name='admin'),

    re_path(r'^upload/', 
        login_required(ck_view.upload),
        name='ckeditor_upload'),

    re_path(r'^browse/',
        never_cache(login_required(ck_view.browse)),
        name='ckeditor_browse'),

    path('ajax-follow/<int:pk>/',
        article_view.ajax_follow,
        name='ajax-follow'),

    path('ajax-like/<int:pk>/',
        article_view.ajax_like,
        name='ajax-like'),

    path('search/',
        article_view.search,
        name='article_search'),
]

if settings.DEBUG:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT
        }),
    ]
