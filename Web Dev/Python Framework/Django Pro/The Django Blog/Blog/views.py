from django.shortcuts import render,HttpResponse, redirect
from Blog.models import Blogs, BlogComment
from django.contrib import messages
# Create your views here.
def blog(request):
    allPost = Blogs.objects.all()
    contex = {'allPost':allPost}
    return render(request, 'BLog/blog.html',contex)

def post(request, slug):
    post = Blogs.objects.filter(slug=slug).first()
    comments = BlogComment.objects.filter(post = post)
    contex = {'post':post, 'comments':comments, 'user':request.user}
    return render(request, 'Blog/blogpost.html', contex)


def blogcomments(request):
    if request.method == 'POST':
        comment = request.POST.get('comment')
        user = request.user
        postsno = request.POST.get('postsno')
        post = Blogs.objects.get(sno = postsno)
        comment = BlogComment(comment=comment, user=user, post=post)
        comment.save()
        messages.success(request, "Comment posted ")

    return redirect(f"/blog/{post.slug}")