from django.db import models
import uuid
from django.contrib.auth.models import User
#ModelForm và forms: Sử dụng Django Form để tạo form dựa trên model.
class Post(models.Model):
     #null: neu bang True thi django se luu cac gia tri rong(empty) la NULL trong database.Mac dinh la False
    #blank: neu True, truong duoc phep trong.Mac dinh la False
    title=models.CharField(max_length=500)
    #nguoi tao ra bai post
    # khi tac gia bi xoa thi bai post van ton tai
    #bang User tao 1 thuoc tinh co ten la posts.
    #related_name='posts' thiết lập mối quan hệ giữa User và Post.
    author=models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='posts')
    #nguoi tao ra hinh anh
    #artist= models.CharField(max_length=500, null=True, blank=True)
    #url=models.CharField(max_length=500, null=True, blank=True)
    image=models.ImageField(upload_to='imagepost/' ,null=True, blank=True)
    file=models.FileField(upload_to='filepost/' ,null=True, blank=True)
    video=models.FileField(upload_to='videopost/', null=True, blank=True)
    audio=models.FileField(upload_to='audiopost/', null=True, blank=True)
    #image=models.URLField(max_length=500)
    likes=models.ManyToManyField(User,related_name='likeposts', through='LikedPost' )
    body=models.TextField()
    tags=models.ManyToManyField('Tag', null=True, blank=True)

    created=models.DateTimeField(auto_now_add=True)
    id=models.CharField(max_length=100, default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return str(self.title)
    
    @property
    def ImageUrl(self):
        try:
            url=self.image.url
        except:
            url=''
        return url
    
    @property
    def FileUrl(self):
        try:
            url=self.file.url
        except:
            url=''
        return url
    #cac bai dang se duoc sap xep theo thu tu thoi gian
    class Meta:
        ordering= ['-created']

class LikedPost(models.Model):
    post=models.ForeignKey(Post, on_delete=models.CASCADE)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    created=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} : {self.post.title}'
    


class Tag(models.Model):
    name=models.CharField(max_length=20)
    image=models.FileField(upload_to='icons/',null=True, blank=True)
    '''models.SlugField: SlugField là một kiểu trường trong Django, giống như một chuỗi văn bản (CharField) 
    nhưng chỉ cho phép chứa các ký tự hợp lệ trong slug, bao gồm:
    Chữ cái (a-z),
    Số (0-9),
    Dấu gạch ngang (-) và gạch dưới (_).
    Trường slug thường dùng để tạo các URL thân thiện với người dùng và dễ SEO, ví dụ:
    Tiêu đề bài viết: "Hướng dẫn Django cơ bản"
    Slug: huong-dan-django-co-ban
    Với slug này, URL bài viết sẽ có dạng: https://example.com/huong-dan-django-co-ban/, thân thiện với người dùng và SEO hơn.
    '''
    slug=models.SlugField(max_length=20, unique=True)
    order=models.IntegerField(null=True)
    def __str__(self):
        return self.name
    
    @property
    def ImageUrl(self):
        try:
            url=self.image.url
        except:
            url=''
        return url
    #sap xep theo so thu tu
    class Meta:
        ordering=['order']


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='comments')
    parent_post=models.ForeignKey(Post, on_delete=models.CASCADE,null=True, related_name='comments')
    body=models.CharField(max_length=200)
    likes=models.ManyToManyField(User, related_name='likecomments', through='LikedComment')
    created=models.DateTimeField(auto_now_add=True)
    id=models.CharField(max_length=100, default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        try:
            return f'{self.author.username} : {self.body[:30]}'
        except:
            return f'no other : {self.body[:30]}'
        
    class Meta:
        ordering= ['-created']


class LikedComment(models.Model):
    comment=models.ForeignKey(Comment, on_delete=models.CASCADE)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    created=models.DateTimeField(auto_now_add=True) 


    def __str__(self):
        return f'{self.user.username} : {self.comment.body[:30]}'

       

class Reply(models.Model):
    author=models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='replies')
    parent_comment=models.ForeignKey(Comment, on_delete=models.CASCADE,null=True, related_name='replies')
    body=models.CharField(max_length=200)
    likes=models.ManyToManyField(User, related_name='likereplies', through="LikedReply")
    created=models.DateTimeField(auto_now_add=True)
    id=models.CharField(max_length=100, default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        try:
            return f'{self.author.username} : {self.body[:30]}'
        except:
            return f'no author : {self.body[:30]}'
        
    class Meta:
        ordering=['-created']
        

class LikedReply(models.Model):
    reply=models.ForeignKey(Reply, on_delete=models.CASCADE)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    created=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}:{self.reply.body[:30]}'