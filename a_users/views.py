from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404, HttpResponse
from .models import Profile
from django.urls import reverse
from django.contrib import messages
from django.http import Http404
from django.contrib.auth import logout
from django.contrib.auth.models import User
from .forms import *
from django.db.models import Count
from a_posts.forms import ReplyCreateForm
# Create your views here.
#ham chuyen huong de xem profile ca nhan
# def profile_view(request):
#     profile=request.user.profile
#     return render(request, 'a_users/profile.html', {'profile': profile})

def profile_edit(request):
    '''Tham số instance được sử dụng để khởi tạo form với dữ liệu
      từ một instance cụ thể của model, thay vì tạo form trống.'''
    form=ProfileForm(instance=request.user.profile)
    
    if request.method=="POST":
        #doi voi cac tep, them 1 tham so bieu mau request.FILES
        #request.POST,request.FILES chua tất cả cá dữ liệu mà người dùng tải thông qua form
        #instance cho biết ProfileForm đang làm việc với một bản ghi hiện có,thay vì tạo mới 1 bản ghi.
        form=ProfileForm(request.POST, request.FILES , instance=request.user.profile)
        if form.is_valid():
            if form.cleaned_data['remove_image']:
                request.user.profile.image = None  # Gỡ ảnh khỏi bài đăng
            form.save()
            return redirect('profile')
    if request.path == reverse('profile-onboarding'):
        template='a_users/profile_onboarding.html'
    else:
        template='a_users/profile_edit.html'
    return render(request, template,{'form': form})
# ham khi an vao ten nguoi dung thi no se ra cac bai viet ma nguoi do da dang
def profile_view(request, username=None):
    if username:
        profile = get_object_or_404(User, username=username).profile
    else:
        try:
            profile = request.user.profile
        except:
            raise Http404()
        
    posts = profile.user.posts.all()
    if request.htmx:
        if 'top-posts' in request.GET:
            posts = profile.user.posts.annotate(num_likes=Count('likes')).filter(num_likes__gt=0).order_by('-num_likes')
        elif 'top-comments' in request.GET:
            comments = profile.user.comments.annotate(num_likes=Count('likes')).filter(num_likes__gt=0).order_by('-num_likes')
            replyform = ReplyCreateForm()
            return render(request, 'snippets/loop_profile_comments.html', { 'comments': comments, 'replyform': replyform })
        elif 'liked-posts' in request.GET:
            posts = profile.user.likeposts.order_by('-likeposts__created') 
        return render(request, 'snippets/loop_profile_posts.html', { 'posts': posts })
    
    context = {
        'profile' : profile,
        'posts': posts,
    }
    
    return render(request, 'a_users/profile.html', context)

    

def profile_delete_view(request):
    user=request.user
    if request.method=="POST":
        #Xóa ID người dùng đã xác thực khỏi yêu cầu và xóa dữ liệu phiên của họ.
        #dang xuat khoi trang web
        logout(request)
        user.delete()

        messages.success(request, 'Account deleted, what a pity')
        return redirect('login')

    return render(request, 'a_users/profile_delete.html')

