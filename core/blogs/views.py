from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from .models import Post


def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blogs/home.html', context)


class PostListView(ListView):
    model = Post
    # this is the default convention if you don't set the template_name
    # <app>/<model>_<viewtype>.html
    # blog/post_list.html
    template_name = 'blogs/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5


class UserPostListView(ListView):
    model = Post
    template_name = 'blogs/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post
    # this is the default convention if you don't set the template_name
    # <app>/<model>_<viewtype>.html


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    # this is the default convention if you don't set the template_name
    # <app>/<model>_<viewtype>.html
    # https://youtu.be/-s7e_Fy6NRU?list=PL-osiE80TeTtoQCKZ03TU5fNfx2UY6U4p&t=1304
    # explain why the default is not post_create.html but post_form.html

    def form_valid(self, form):
        # get the current login user and set that to the author of this post
        form.instance.author = self.request.user
        return super().form_valid(form)


# LoginRequiredMixin so that only login user can access this
# UserPassesTestMixin so that the owner of the post can only update its own post
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # so that the owner of the post can only update its own post
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
    return render(request, 'blogs/about.html', {
        'title': 'About',
    })
