from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, request
from .models import Post
from django.contrib.auth.models import User
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from taggit.models import Tag
from .forms import PostForm
from django.db.models import Q
from django.template.defaultfilters import slugify
from django.shortcuts import redirect
from users.models import User,Profile
from django import forms
from pagedown.widgets import PagedownWidget
# Create your views here.

class TagMixin(object):
    model = 'Post'
    def get_context_data(self, **kwargs):
        context = super(TagMixin,self).get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        return context


class PostCreateView(TagMixin, LoginRequiredMixin, CreateView):
    #form_class = PostForm()
    #context_object_name = form_class
    #content = forms.CharField(widget=PagedownWidget)
    model = Post
    fields = ['title', 'content', 'image',]


    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return HttpResponseRedirect('admin-approval')



class AdminApproval(ListView):
    model = Post
    template_name = 'blog/admin-approval.html'


class PostListView(TagMixin,ListView):
    model = Post
    template_name = 'blog/home.html'
    queryset=Post.objects.filter(is_approved=True)
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 15
    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        context['top_rated']=Post.objects.filter(category='TR')[0:3]
        context['most_popular'] = Post.objects.filter(category='MV')[0:3]
        context['recently_added'] = Post.objects.filter(category='RA')[0:1]
        context['tags_slider']=Tag.objects.all()
        print(context)
        return context




#class PostSearch(TagMixin,ListView):
 #   model = Post
  #  paginate_by = 4
   # template_name = 'blog/base.html'
    #def get_queryset(self):
     #   query = self.request.GET.get('query')
      #  if query:
       #     posts = Post.objects.filter(title__icontains=query)
        #    print(posts)
         #   print(query)
        #return posts

class UserPostListView(TagMixin,ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 15

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user , is_approved=True).order_by('-date_posted')


class TagIndexedView(TagMixin, ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    paginate_by = 15

    def get_queryset(self):
        return Post.objects.filter(tags__slug=self.kwargs.get('slug'))


class PostDetailView(DetailView):
    model = Post








class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html')

def contact(request):
    return render(request, 'blog/contact.html')

def contributors(request):
    model = Profile
    profile= model.objects.all()
    context = {'profile' :profile}

    return render(request, 'blog/contributors.html', context)

def search(request):
    query = request.GET.get('query', '')   # so we always get a string

    qs = Post.objects.all()
    if len(query) > 0:
        qs = qs.filter(title__icontains=query)

    context = {
        'query': query,
        'posts': qs,
    }
    print('context', context)

    return render(request, 'blog/home.html', context)

