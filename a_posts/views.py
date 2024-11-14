from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from .models import *
from.forms import *
from django.db.models import Count
from bs4 import BeautifulSoup
import requests
from django.contrib import messages
#render: Hàm để kết xuất (render) một template và trả về phản hồi HTTP.
#redirect: Hàm chuyển hướng đến một URL khác sau khi hoàn thành một hành động (thường dùng sau khi lưu dữ liệu).
# Create your views here.
'''Ham rennder Trả về một HttpResponse có nội dung chứa đầy kết quả của việc 
gọi django.template.loader.render_to_string() với các đối số được truyền.'''
#Http la giao thuc truyen tai sieu van ban(siue van ban o day la html)
#cac ham duoi day tra ve cac the html tuong ung.
def index(request):
    return render(request, "index.html")
#Hàm view để hiển thị tất cả các bài đăng (Post) từ cơ sở dữ liệu.
'''phần tag=None trong hàm đặt giá trị mặc định cho tham số tag là None. Điều này có nghĩa là 
    nếu không có giá trị nào được truyền vào cho tag khi gọi hàm login(),
    thì tag sẽ tự động nhận giá trị None.'''
def login(request, tag=None):
    #hien thi tat ca cac bai post co cung category la tag
    if tag:
        posts=Post.objects.filter(tags__slug=tag)
        tag=get_object_or_404(Tag, slug=tag)
    else :
        #lay tat ca cac bai post tu csdl
        posts= Post.objects.all()

    # categories=Tag.objects.all()
    context={
        'posts': posts,
        # 'categories': categories,
        'tag':tag
    }
    return render(request, 'aposts/home.html',context)

#tao 1 bai Post
#PostCreateForm: Là một lớp form dựa trên model Post, dùng để tạo một bài đăng mới.
#Meta: Cung cấp thông tin cấu hình cho PostCreateForm.

#gui bai post luu vao csdl de hien thi bai post len trang chu
#Xử lý việc tạo bài đăng mới
@login_required
def post_create_view(request):
    #Tạo một instance của PostCreateForm.
    #PostCreateForm(): Form trống, dùng để hiển thị cho người dùng nhập liệu.
    form = PostCreateForm()
    #Kiểm tra nếu người dùng gửi form bằng phương thức POST.
    if request.method=='POST':
        #PostCreateForm(request.POST): Form chứa dữ liệu người dùng gửi, dùng để kiểm tra và xử lý khi form được submit.
        #Khi gọi PostCreateForm(request.POST), form đã được gửi
        #request.POST trong Django chứa dữ liệu mà người dùng gửi qua phương thức 
        # HTTP POST khi họ điền và gửi một form trên trang web. 
        form=PostCreateForm(request.POST, request.FILES)
        if form.is_valid():
            #chua luu vao csdl commit=False, phai them 1 vài dk nưa
            post=form.save(commit=False)
            post.author=request.user
            #luu vao csdl
            post.save()
            form.save_m2m()
            return redirect('login')
    return render(request, 'aposts/post_create.html', {'form': form})
#ham xoa 1 bai post
#yeu cau dang nhap moi co the truy cap den
@login_required
def post_delete_view(request, pk):
    post=get_object_or_404(Post, id=pk, author=request.user)
    if(request.method=="POST"):
        post.delete()
        #sau khi xoa thi hien thi 1 thong bao thanh cong
        messages.success(request, 'Post deleted')
        return redirect('login')
    
    return render(request, 'aposts/post_delete.html', {'post': post})
#ham chinh sua 1 bai post
@login_required
def post_edit_view(request, pk):
    post=get_object_or_404(Post, id=pk, author=request.user)
    form=PostEditForm(instance=post)
   
    if request.method=="POST":
        '''GET request: Khi người dùng truy cập trang chỉnh sửa, form sẽ được hiển thị với dữ liệu hiện tại của bài đăng (post).
          Dữ liệu của post được truyền vào PostEditForm qua instance=post.
        POST request: Khi người dùng gửi form với các chỉnh sửa, Django sẽ kiểm tra tính hợp lệ 
        của form (form.is_valid()). Nếu hợp lệ, form.save() sẽ cập nhật bài đăng hiện tại.'''
        form=PostEditForm(request.POST,request.FILES, instance=post)
        if form.is_valid():
            # Kiểm tra nếu người dùng chọn xóa ảnh
            if form.cleaned_data['remove_image']:
                post.file = None  # Gỡ ảnh khỏi bài đăng
            form.save()
            messages.success(request, "Post updated")
            return redirect('login')
        
     #nhung thu ma chung ta muon gui di
    context={
        'post':post,
        'form': form,
    }

    #gui yeu cau den trang post_edit kem theo du lieu cu cua bai post(context)
    return render(request, 'aposts/post_edit.html', context)
#post=get_object_or_404(Post, id=pk) tra ve bai post, neu khong thi tra ve trang 404
def comment_edit_view(request, pk):
    comment=get_object_or_404(Comment, id=pk)
    form=CommentEditForm(instance=comment)
    if request.method=='POST':
        form=CommentEditForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Comment updated')
            return redirect('post', comment.parent_post.id)
    
    context={
        'comment': comment,
        'form' : form,
    }
    
    return render(request, 'aposts/comment_edit.html', context)


def reply_edit_view(request, pk):
    reply=get_object_or_404(Reply,id=pk)
    form=ReplyEditForm(instance=reply)

    if request.method=="POST":
        form=ReplyEditForm(request.POST, instance=reply)
        if form.is_valid():
            form.save()
            messages(request, 'Reply updated')
            return redirect('post', reply.parent_comment.parent_post.id)
    context={
        'reply' : reply,
        'form': form
    } 
    return render(request, 'aposts/reply_edit.html', context)

#ham de xem 1 bai viet
def post_page_view(request, pk):
    post=get_object_or_404(Post, id=pk)
    #form de lay du lieu tu cmt cua user
    commentform=CommentCreateForm()
    # if request.method=="POST":
    #     form=CommentCreateForm(request.POST)
    #     if form.is_valid():
    #         comment=form.save(commit=False)
    #         comment.author=request.user
    #         comment.parent_post=post
    #         comment.save()
    replyform=ReplyCreateForm()
    #kiểm tra xem một yêu cầu HTTP có phải là một yêu cầu từ HTMX hay không. 
    if request.htmx:
        #neu ma tim thay top trong url
        if 'top' in request.GET:
            #dang kiem tra xem thuoc tinh like cua comment co rỗng không.
            #comments=post.comments.filter(likes__isnull=False).distinct()
            #sap xep cac cmt theo thu tu so likes giam dan va cac cmt nay phai co so likes lon hon 0.
            comments=post.comments.annotate(num_likes=Count('likes')).filter(num_likes__gt=0).order_by('-num_likes')
        else:
            comments=post.comments.all()
        return render(request, 'snippets/loop_postpage_comments.html', {'comments': comments, 'replyform': replyform})


    context={
        'post': post,
        'commentform': commentform,
        'replyform' : replyform,
    }
    return render(request, 'aposts/post_page.html', context)

@login_required
def comment_send(request, pk):
    post=get_object_or_404(Post, id=pk)

    replyform=ReplyCreateForm()
    if request.method =="POST":
        form=CommentCreateForm(request.POST)
        if form.is_valid():
            comment=form.save(commit=False)
            comment.author=request.user 
            comment.parent_post=post
            comment.save()
    
    context={
        'comment': comment, 
        'post': post,
        'replyform': replyform,
    }
    return render(request, 'snippets/add_comment.html', context)
    # return redirect('post', comment.parent_post.id)
    # return render(request, 'aposts/comment.html', {'comment': comment})


@login_required     
def comment_delete_view(request, pk):
    comment=get_object_or_404(Comment, id=pk)

    if request.method=="POST":
        comment.delete()
        messages.success(request, 'Comment deleted')
        return redirect('post', comment.parent_post.id)
    
    return render(request, 'aposts/comment_delete.html', {'comment': comment})


#phan thao tac voi reply
@login_required
def reply_send(request, pk):
    comment=get_object_or_404(Comment, id=pk)

    replyform=ReplyCreateForm()
    if request.method=="POST":
        form=ReplyCreateForm(request.POST)
        if form.is_valid():
            reply=form.save(commit=False)
            reply.author=request.user
            reply.parent_comment=comment
            reply.save()

    context={
        'comment': comment,     
        'reply': reply,
        'replyform': replyform,
    }
    return render(request, 'snippets/add_reply.html',context)

@login_required
def reply_delete_view(request,pk):
    reply=get_object_or_404(Reply, id=pk)
    if request.method=="POST":
        reply.delete()
        messages.success(request, 'Comment deleted')
        return redirect('post', reply.parent_comment.parent_post.id)
    
    return render(request, 'aposts/reply_delete.html', {'reply': reply})


#ap dung python decorators
def like_toggle(model):
    def inner_func(func):
        def wrapper(request, *args, **kwargs):
            post=get_object_or_404(model,id=kwargs.get('pk'))
            #kiem tra xem nguoi ike da ton tai trong danh sach like cua bai post hay chua
            # tra ve True la da ton tai, False neu nguoc lai.
            user_exist=post.likes.filter(username=request.user.username).exists()

            if post.author!=request.user:
                if user_exist:
                    post.likes.remove(request.user)
                else:
                    post.likes.add(request.user)
                    
            return func(request, post)
        return wrapper
    return inner_func

@login_required
@like_toggle(Post)
def like_post(request, post):
    return render(request, 'snippets/likes.html', {'post': post})

@login_required
@like_toggle(Comment)
def like_comment(request, comment):
    return render(request, 'snippets/likes_comment.html', {'comment': comment})

@login_required
@like_toggle(Reply)
def like_reply(request, reply):
    return render(request, 'snippets/likes_reply.html', {'reply': reply})

#ham tim kiem user
@login_required
def search_view(request):
    if request.method=="GET":
        username=request.GET.get('query','')
        if username:
            try:
                user=get_object_or_404(User, username=username)
            except:
                raise Http404()   
        posts=user.posts.all()
        profile=user.profile
        return render(request, 'a_users/profile.html', {'profile':profile, 'posts': posts})
    return redirect('login')