from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostForm, CommentForm, UserRegistrationForm, PostFilters, UserEditForm
from .models import Post, Comment, Notification
from django.contrib.auth.decorators import login_required


def post_list(request):
    posts = Post.objects.all()
    filter = PostFilters(request.GET, queryset=Post.objects.all())
    return render(request, 'post_list.html', {'posts': posts, 'filter': filter})


@login_required(login_url='/login/')
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.request = request
            post.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'post_create.html', {'form': form})


@login_required(login_url='/login/')
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    post.delete()
    return redirect('post_list')


@login_required(login_url='/login/')
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    if request.method == 'POST':
        form = PostForm(data=request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_list')
    else:
        form = PostForm(instance=post)
    return render(request, 'post_edit.html', {'form': form, 'post': post})


def post_retrive(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.request = request
            new_comment.save()
            return redirect(request.path)
    else:
        comment_form = CommentForm()
    return render(request,
                  'post_retrive.html',
                  {'post': post,
                   'comments': comments,
                   'comment_form': comment_form})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request, 'register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'register.html', {'user_form': user_form})


@login_required(login_url='/login/')
def user_edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)

        if user_form.is_valid():
            user_form.save()
            return render(request, 'user_edit.html',
                          {'user_form': user_form, 'user_update_result': 'Ваш профиль обновлён'})
    else:
        user_form = UserEditForm(instance=request.user)
    return render(request, 'user_edit.html', {'user_form': user_form})


def notifications(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'notifications.html', {'notifications': notifications})
