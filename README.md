# Python - Django - Basic User Registration/Authentication with Blog
Python 3.11.0
pip 22.3 

In requirements.txt
```
pip freeze > requirements
pip install -r requirements.txt
```
asgiref==3.7.2
crispy-bootstrap4==2022.1
Django==4.2.5
django-crispy-forms==2.0
sqlparse==0.4.4
tzdata==2023.3


## Setup - Step 1

Go to desktop
```
cd desktop
```

Create project folder
desktop
```
mkdir projName01
```

Go in your project folder
desktop
```
cd projName01
```

Create environment named venv
desktop/projName01
```
python -m venv venv
```

Activate environment
desktop/projName01
```
venv\Scripts\activate.bat
```

Install django
(venv) desktop/projName01
```
python -m pip install Django
```

Start project
(venv) desktop/projName01
```
django-admin startproject core
```

cd in your project
(venv) desktop/projName01
```
cd core
```

IDE
- drag outer core folder in your IDE(visual studio code)
OR
(venv) desktop/projName01/core
```
code .
```

## Setup - Step 2

1. Create app users, blogs, and install crispy forms
```python
python manage.py startapp users
python manage.py startapp blogs
pip install django-crispy-forms
pip install crispy-bootstrap4
```

2. Static and Templates. [Bootstrap4 Starter Template](https://getbootstrap.com/docs/4.0/getting-started/introduction/#starter-template) 
```
> projName01
	> static
		> main.css
	> templates
		> base.html
	> users
		> templates
			> users
				> .html
	> blogs
		> templates
			> blogs
				> .html
```

3. settings.py
```python
import os

INSTALLED_APPS = [
    'blogs.apps.BlogsConfig',
    'users.apps.UsersConfig',
    "crispy_forms",
    "crispy_bootstrap4",

]

TEMPLATES = [
    {
        'DIRS': [
            BASE_DIR / 'templates',
        ],
    },
]


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "static_root"

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap4"
CRISPY_TEMPLATE_PACK = "bootstrap4"

# do this if you use from django.contrib.auth import views as auth_views to manage your login
# so that django will not redirect to profile "default" after logging in
LOGIN_REDIRECT_URL = 'blog-home'

# users get redirected here if trying to access page that needs authentication
LOGIN_URL = 'login'

# for resetting password
# watch link below for continue setup
# https://youtu.be/-tyBEsHSv7w?list=PL-osiE80TeTtoQCKZ03TU5fNfx2UY6U4p&t=729
# https://myaccount.google.com › apppasswords
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'emailUsername'
EMAIL_HOST_PASSWORD = 'passGeneratedByGoogleAppPasswords'
```

4. core/urls.py
```python
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from users import views as user_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', user_views.register, name='register'),

    # note that we don't have views.py for these
    # the built-in views for login and logout that Django gave us
    # will handle the forms and the logic for us
    # but it's not going to handle the templates, that's why we put it here
    # explains why iyang template naa sa users location rather than main folder
    # https://youtu.be/3aVqWaLjqS4?list=PL-osiE80TeTtoQCKZ03TU5fNfx2UY6U4p&t=257
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),

    path('profile/', user_views.profile, name='profile'),
    
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='users/password_reset.html'
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='users/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='users/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='users/password_reset_complete.html'
         ),
         name='password_reset_complete'),

    path('', include('blogs.urls')),
]
```

5. blogs/urls.py
```python
from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, UserPostListView
from . import views


urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('about/', views.about, name='blog-about'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
]
```

6. users/forms.py
```python
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', ]
```

7. blogs/models.py
```python
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    # https://youtu.be/-s7e_Fy6NRU?list=PL-osiE80TeTtoQCKZ03TU5fNfx2UY6U4p&t=1651
    # when we want the view to know where we want to redirect once we've created the post
    # use get_absolute_url, the way to tell django how to find the url
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
```

8. blogs/admin.py
```python
from django.contrib import admin
from .models import Post

admin.site.register(Post)
```

9. users/views.py
```python
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            # username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


# decorator to enforce only login users can go to this page
@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        # p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        # if u_form.is_valid() and p_form.is_valid():
        if u_form.is_valid():
            u_form.save()
            # p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        # p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        # 'p_form': p_form,
    }

    return render(request, 'users/profile.html', context)
```

10. blogs/views.py
```python
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
```

11. Migrations, Super user, Run server
```python
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

12. Dummy Data. Need atleast 2 users in database. 
projName\posts.json
```python
python manage.py shell
import json
from blogs.models import Post
with open('posts.json') as f:
	posts_json = json.load(f)

for post in posts_json:
	post = Post(title=post['title'], content=post['content'], author_id=post['user_id'])
	post.save()
```


