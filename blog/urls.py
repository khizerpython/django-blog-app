from django.urls import path
from .views import PostListView , PostDetailView , PostCreateView, PostUpdateView, PostDeleteView ,UserPostListView,TagMixin,TagIndexedView, AdminApproval
from . import views
urlpatterns = [
    path('', PostListView.as_view() , name='blog-home' ),
    path('post/new/', PostCreateView.as_view() , name='post-create' ),
    path('post/new/admin-approval', AdminApproval.as_view() , name='admin-approval' ),
    path('<slug:slug>', TagIndexedView.as_view() , name='tagged' ),
    path('user/<str:username>', UserPostListView.as_view() , name='user-posts' ),

    path('post/<slug:slug>/', PostDetailView.as_view() , name='post-detail' ),

    path('post/<int:pk>/update/', PostUpdateView.as_view() , name='post-update' ),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name='blog-about' ),
    path('contact/', views.contact, name='blog-contact' ),
    path('search/', views.search, name='blog-search' ),
    path('contributors/', views.contributors, name='post-contributors' ),
    #path('search/', PostSearch.as_view(), name='post-search' ),
]