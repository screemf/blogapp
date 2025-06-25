from django.urls import path
from . import views
from .views import PostDetailView, PostListView, post_detail, delete_comment, toggle_verified

urlpatterns = [
    path('home/', views.index, name='home'),
    path('contacts', views.contacts, name='contacts'),
   # path('author_create/', views.author_create, name='author_create'),
    path('authors/', views.authors, name='authors'),
    path('author/<int:author_id>/', views.author, name='author'),
    path('author_form/', views.author_create_form, name='author_create_form'),
    path('author_update_form/<int:author_id>/', views.author_update_form, name='author_update_form'),
    path('contact/', views.contact, name='contact'),
    #path('post/<int:pk>/', views.PostDetailView.as_view(), name='post'),
    #path('posts/', views.PostListView.as_view(), name='posts'),
    path('post/new', views.PostCreateView.as_view(), name='post_form'),
    #path('post/new', views.create_post, name='post_form'),
    path('posts/', views.post_list, name='posts'),
    path('post/<int:pk>/edit', views.PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete', views.PostDeleteView.as_view(), name='post_delete'),
    path('post/<int:pk>/', post_detail, name='post'),
    #path('', views.index, name='index'),
    path('like-post/<int:post_id>/', views.like_post, name='like_post'),
    path('like-comment/<int:comment_id>/', views.like_comment, name='like_comment'),
    path('delete-comment/<int:comment_id>/', delete_comment, name='delete_comment'),
    path('toggle-verified/<int:author_id>/', toggle_verified, name='toggle_verified'),
]