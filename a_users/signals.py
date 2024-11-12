#file này được viết ra để tự động tạo 1 trang profile khi nguiowf dùng đăng nhập vào trang web
from django.dispatch import receiver
from django.shortcuts import get_object_or_404
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import Profile

@receiver(post_save, sender=User)
#ham tu dong tao profile
def create_profile(sender, instance, created, **kwargs):
    #sender la nguoi gui, xac dinh models class dang duoc kich hoat
    # instance : 1 doi tuong cu the cua models class, doi tuong user da duoc tao
    #created: chco biet 1 doi tuong dang duoc tao, hay dang duoc edit.
    # **kwargs: 1 dictionary(key, value): hàm có thể chấp nhận bất kỳ số lượng giá trị nào dưới dạng dối số hoặc từ khóa. 
    user=instance
    #neu nguoi dung duoc tao moi
    if created:
        Profile.objects.create(
            user=user,
            email=user.email
        )
    #neu ma admin thay doi du lieu cua nguoi dung tu trang admin
    else:
        profile=get_object_or_404(Profile, user=user)
        profile.email=user.email
        profile.save()


# ham cap nhat lai email user khi chinh sua profile ca nhan.
@receiver(post_save, sender=Profile)
def update_user(sender, instance, created, **kwargs):
    profile=instance
    if created==False:
        user=get_object_or_404(User, id=profile.user.id)
        if user.email!=profile.email:
            user.email=profile.email
            user.save()
