from django.shortcuts import render, get_object_or_404,redirect
from .models import *
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .forms import *
from django.contrib import messages

@login_required
def chat_view(request, chatroom_name='public-chat'):
    chat_group=get_object_or_404(ChatGroup,group_name=chatroom_name )
    chat_messages=chat_group.chat_messages.all()[:30]
    form = ChatmessageCreateForm()
    other_user=None
    if chat_group.is_private:
        if request.user not in chat_group.members.all():
            raise Http404()
        for member in chat_group.members.all():
            if request.user != member:
                other_user=member
                break

    # kiem tra xem noi nhom co ten nhom(groupchat_name): day la group ma mk tu tao ra
    if chat_group.groupchat_name:
        if request.user not in chat_group.members.all():
            # chat_group.members.add(request.user)
            # Nếu chưa là thành viên, kiểm tra nếu đã có yêu cầu tham gia hay chưa
            join_request, created = JoinRequest.objects.get_or_create(user=request.user, chat_group=chat_group)
            if join_request not in chat_group.join_requests.all():
                chat_group.join_requests.add(join_request)
            if created:
                # Nếu yêu cầu mới được tạo, hiển thị thông báo xác nhận
                message = "Yêu cầu tham gia của bạn đã được gửi và đang chờ admin duyệt."
            else:
                # Nếu yêu cầu đã tồn tại, hiển thị thông báo chờ duyệt
                message = "Yêu cầu tham gia của bạn đang được xử lý."

            # Chuyển hướng hoặc hiển thị thông báo
            return render(request, 'partials/join_request_pending.html', {'message': message, 'chat_group': chat_group})


    if request.htmx:
        form=ChatmessageCreateForm(request.POST)
        if form.is_valid:
            message=form.save(commit=False)
            message.author=request.user
            message.group=chat_group
            message.save()
            context={
                'message': message,
                'user': request.user,
            }
            return render(request,'partials/chat_message_p.html', context)
    
    context={
        'chat_messages': chat_messages,
        'form': form,
        'other_user': other_user,
        'chatroom_name': chatroom_name,
        'chat_group':chat_group,
    }
        
    return render(request, 'a_rtchat/chat.html', context)


#ham nhan hoac tao phong tro chuyen 
@login_required
def get_or_create_chatroom(request, username=None):
    
    if not username:
        return redirect('chathome')  # Nếu không có username, chuyển hướng về trang chủ trò chuyện
    
    if request.user.username == username:
        return redirect('chathome')

    other_user=get_object_or_404(User, username=username)

    # loc tat ca cac phong tro chuyen private ma nguoi dung nay la thanh vien.
    my_chatrooms=request.user.chat_groups.filter(is_private=True)

    if my_chatrooms.exists():
        for chatroom in my_chatrooms:
            if other_user in chatroom.members.all():
                chatroom=chatroom
                break
            else:
                chatroom=ChatGroup.objects.create(is_private=True)
                chatroom.members.add(request.user, other_user)

    else:
        chatroom=ChatGroup.objects.create(is_private=True)
        chatroom.members.add(request.user, other_user)
    return redirect('chatroom', chatroom.group_name)

@login_required
def create_groupchat(request):
    form = NewGroupForm()
    
    if request.method == 'POST':
        form = NewGroupForm(request.POST)
        if form.is_valid():
            new_groupchat = form.save(commit=False)
            new_groupchat.admin = request.user
            new_groupchat.save()
            new_groupchat.members.add(request.user)
            return redirect('chatroom', new_groupchat.group_name)
    
    context = {
        'form': form
    }
    return render(request, 'partials/create_groupchat.html', context)

# ham chinh sua lai nhom chat: doi ten, xoa thanh vien, thuc hien chuc nang cua admin.
@login_required
def chatroom_edit_view(request, chatroom_name):
    chat_group=get_object_or_404(ChatGroup, group_name=chatroom_name)
    if request.user != chat_group.admin:
        raise Http404()
    form=ChatRoomEditForm(instance=chat_group)

    if request.method == "POST":
        form=ChatRoomEditForm(request.POST, instance=chat_group)
        if form.is_valid:
            form.save()

            #danh sach id cua cac thanh vien bi xoa khoi nhom chat
            remove_members=request.POST.getlist('remove_members')
            for member_id in remove_members:
                member=User.objects.get(id=member_id)
                chat_group.members.remove(member)

            return redirect('chatroom', chatroom_name)

    context={
        'form': form,
        'chat_group': chat_group,
    }
    return render(request, 'partials/chatroom_edit.html', context)

#ham xoa nhom chat
@login_required
def chatroom_delete_view(request, chatroom_name):
    chat_group=get_object_or_404(ChatGroup, group_name=chatroom_name)

    if request.user != chat_group.admin:
        raise Http404()
    
    if request.method == "POST":
        chat_group.delete()
        messages.success(request, 'Chatroom deleted')
        return redirect('login')
    
    return render(request, 'partials/chatroom_delete.html', {'chat_group':chat_group})

#admin them 1 nguoi dung vao trong nhom chat.
@login_required
def chatroom_add_view(request, chatroom_name):
    # Lấy nhóm chat theo `group_name`
    chat_group = get_object_or_404(ChatGroup, group_name=chatroom_name)

    # Kiểm tra quyền admin
    if request.user != chat_group.admin:
        raise Http404()
    
    form = UserAddGroupChatForm()
    if request.method == "POST":
        form = UserAddGroupChatForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            
            # Kiểm tra sự tồn tại của người dùng
            try:
                add_user = User.objects.get(username=username)
            except User.DoesNotExist:
                form.add_error('username', "Người dùng không tồn tại.")
            else:
                # Kiểm tra người dùng đã có trong nhóm chưa
                if add_user in chat_group.members.all():
                    form.add_error('username', "Người dùng đã là thành viên của nhóm.")
                else:
                    # Thêm người dùng vào nhóm
                    chat_group.members.add(add_user)
                    return redirect('chatroom', chat_group.group_name)
        
    # Trả về template nếu không phải phương thức POST hoặc nếu có lỗi trong form
    context = {
        'form': form,
        'chat_group': chat_group,
    }
    return render(request, 'partials/chatroom_add.html', context)


#khi 1 người dùng rời khỏi nhóm chat.
@login_required
def chatroom_leave_view(request, chatroom_name):
    chat_group=get_object_or_404(ChatGroup, group_name=chatroom_name)

    if request.user not in chat_group.members.all():
        raise Http404()

    if request.method == "POST":
        chat_group.members.remove(request.user)
        messages.success(request, 'You have left the chat')
        return redirect('login')
    
    return render(request, 'partials/chatroom_leave.html', {'chat_group':chat_group})



#admin duyet cac yeu cau tham gia nhom cua cac user.
@login_required
def review_join_requests(request, chatroom_name):
    chat_group = get_object_or_404(ChatGroup, group_name=chatroom_name)

    # Kiểm tra quyền admin
    if request.user != chat_group.admin:
        raise Http404("Bạn không có quyền quản lý nhóm này.")

    
    join_requests = chat_group.join_requests.filter(status="pending")

    context = {
        'join_requests': join_requests,
        'chat_group': chat_group,
    }
    return render(request, 'partials/review_join_requests.html', context)

@login_required
def handle_join_request(request, request_id, action):
    join_request = get_object_or_404(JoinRequest, request_name=request_id)

    # Kiểm tra quyền admin của nhóm chat
    if request.user != join_request.chat_group.admin:
        raise Http404()

    if request.method == "POST":
        if action == "accept":
            join_request.status = "accepted"
            join_request.chat_group.members.add(join_request.member)  # Thêm thành viên vào nhóm
        elif action == "reject":
            join_request.status = "rejected"
        
        join_request.save()  # Lưu trạng thái mới
        join_request.delete()  # Xóa yêu cầu sau khi xử lý

    
        join_request.save()
    return redirect('review_join_requests', chatroom_name=join_request.chat_group.group_name)