from django.urls import path,include
from .views import *

urlpatterns = [

    path('', IndexView.as_view(),name='index'),
    path('detail/<int:pk>/<slug:slug>', PostDetail.as_view(),name='detail'),
    path('post-update/<int:pk>/<slug:slug>', UpdatePostView.as_view(), name='post_update'),
    path('category/<int:pk>/<slug:slug>', CategoryDetail.as_view(),name='category_detail'),
    path('tag/<slug:slug>', TagDetail.as_view(), name='tag_detail'),
    path('post-create/', CreatePostView.as_view(), name='create_post'),
    path('post-delete/<int:pk>/<slug:slug>', DeletePostView.as_view(), name='post_delete'),
    path('search/', SearchView.as_view(), name='search'),

]
