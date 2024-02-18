from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from post.models import Post, Comment
from post.forms import PostForm

from core.models import SubmitChallenge
from core.forms import SubmitChallengeForm

from trend.decorators import admin_only

@admin_only
def index(request):
    posts = Post.objects.all().order_by('-created_at')
    context = {
        'posts': posts,
    }
    return render(request, 'post/index.html', context)


@admin_only
def detail(request, id):
    post = get_object_or_404(Post, pk=id)
    if Comment.objects.filter(post=post).exists():
        comments = post.comments.all()
    else:
        comments = False
    context = {
        'post': post,
        'comments': comments
    }
    return render(request, 'post/post_detail.html', context)


@admin_only
def update(request, id):
    post = get_object_or_404(Post, pk=id)
    if request.POST:
        post_form = PostForm(request.POST, instance=post)
        if post.submit_challenge:
            submit_challenge_form = SubmitChallengeForm(request.POST, request.FILES, instance=post.submit_challenge)
            if post_form.is_valid() and submit_challenge_form.is_valid():
                post_form.save()
                submit_challenge_form.save()
                messages.success(request, f"post aggiornato con successo!")
                return redirect('post:index')
        else:
            if post_form.is_valid():
                post_form.save()
                messages.success(request, f"post aggiornato con successo!")
                return redirect('post:index')
    else:
        post_form = PostForm(instance=post)
        if post.submit_challenge:
            submit_challenge_form = SubmitChallengeForm(instance=post.submit_challenge)
        else:
            submit_challenge_form = False

    context = {
        'post': post,
        'post_form': post_form,
        'submit_challenge_form': submit_challenge_form
    }
    
    return render(request, 'post/edit_post.html', context)


@admin_only
def delete(request,id):
    post = get_object_or_404(Post, pk=id)
    if request.method == 'POST':
        post.delete()
        messages.success(request, f"post eliminato con successo!")
        return redirect('post:index')
    context = {
        'post': post
    }
    return render(request, 'post/delete_post.html', context)
