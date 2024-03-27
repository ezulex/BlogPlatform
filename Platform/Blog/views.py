from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostForm, CommentForm, UserRegistrationForm, PostFilters, UserEditForm
from .models import Post, Comment
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
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')

@login_required(login_url='/login/')
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return redirect('post_list')


def post_retrive(request, pk):
    post = get_object_or_404(Post, pk=pk)

    comments = post.comments.all

    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.request = request
            new_comment.save()
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
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            return render(request, 'register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'register.html', {'user_form': user_form})


@login_required
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
