from django.urls import path
from . import views
urlpatterns = [
    path('', views.blog_list, name='blog_list'),
    path('<int:blog_pk>', views.blog_detail, name='blog_detail'),
    path('type/<int:blog_type_pk>', views.blog_type_list, name='blog_type_list'),
    path('search/', views.search, name='search'),
    path('date/<int:year>/<int:month>', views.blog_dates_list, name='blog_dates_list'),
]