from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('app/<int:id>/', views.app_detail, name='app_detail'),
    path('download/<int:id>/', views.download_app, name='download_app'),

    path('register/user/', views.register_user, name='register_user'),
    path('register/developer/', views.register_developer, name='register_developer'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('upload/', views.upload_app, name='upload'),
    path('app/<int:id>/delete/', views.delete_app, name='delete_app'),
    path('review/<int:id>/', views.add_review, name='add_review'),
]
