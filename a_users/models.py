from django.db import models
from django.contrib.auth.models import User
from django.templatetags.static import static
# Create your models here.
class Profile(models.Model):
    # ket noi profile voi nguoi dung
    #on_delete=models.CASCADE : co nghia la khi nguoi dung bi xoa khoi csdl
    # thi profile cua nguoi nay cx se bi xoa.
    '''Trong Django, khi bạn tạo một trường OneToOneField với một model khác (trong trường hợp này là model User),
      Django sẽ tự động cung cấp cho model được tham chiếu một thuộc tính ngược để truy cập đến bản ghi của model mà 
      nó được liên kết.'''
    '''Điều này tạo ra một mối quan hệ một-một giữa User và Profile, 
    có nghĩa là mỗi người dùng User chỉ có một hồ sơ Profile tương ứng và ngược lại.'''
    #on_delete=models.CASCADE   khi nguoi dang bi xoa thi post cx bi xoa.
    ''' khi bạn tạo một OneToOneField từ Profile đến User, Django sẽ tự động cung cấp
      một thuộc tính ngược profile cho model User để truy cập Profile.'''
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    image=models.ImageField(upload_to='avatars/', null=True, blank=True)
    realname=models.CharField(max_length=50, null=True, blank=True)
    '''unique=True sẽ đảm bảo mỗi giá trị email là duy nhất trong bảng. Hai người dùng không thể có cùng một địa chỉ email.
    null=True cho phép trường này có giá trị NULL (không bắt buộc phải có giá trị). Lưu ý rằng trong cơ sở dữ liệu, 
    các giá trị NULL không được coi là trùng lặp.'''
    email=models.EmailField(unique=True, null=True)
    location=models.CharField(max_length=20, null=True, blank=True)
    #tieu su trang profile
    bio=models.TextField(null=True, blank=True)
    created=models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.user)

    @property
    #ham hoat dong giong nhu 1 thuoc tinh
    def avatar(self):
        try:
            avatar=self.image.url
        except:
            avatar=static('app/images/avatar_default.svg')
        return avatar

    @property
    def name(self):
      if self.realname:
          name=self.realname
      else:
        name=self.user.username
      return name
