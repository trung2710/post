from django.forms import ModelForm
from django import forms
from .models import *
class PostCreateForm(ModelForm):
    class Meta:
        model=Post
        #fields: là các trường mà form sẽ xử lí(nếu cần tất cả các trường thì fields="__all__")
        fields=['title','image','file','video','audio','body', 'tags']
        #labels: Cung cấp nhãn hiển thị cho trường body (đặt tên là "Caption").
        labels={ 
            'body': 'Caption',
            'tags': 'category',
            
        }
        '''widgets: Sử dụng các widget tùy chỉnh để thêm thuộc tính CSS
          và cấu hình cho các trường nhập liệu (Textarea cho body và TextInput cho url).'''
        widgets={
            'title' : forms.TextInput(attrs={'row' :1, 'placeholder':'Add a title...', 'class':'front2 text-5m'}) ,
            'image': forms.FileInput(),
            'file': forms.FileInput(),
            'video':forms.FileInput(),
            'audio':forms.FileInput(),
            'body': forms.Textarea(attrs={'rows':3, 'placeholder':'Add a caption...', 'class':'front1 text-3xl'}), 
            'tags': forms.CheckboxSelectMultiple(),
        }

class PostEditForm(ModelForm):
    # đây là checkbox để người dùng có thể chọn để gỡ ảnh nếu ảnh đã tồn tại.
    remove_image = forms.BooleanField(required=False, label='Remove image', initial=False)
    class Meta:
        model=Post
        fields=['title','image','file','video','audio','body', 'tags']
        labels={
            'body':'Caption',
            'tags': 'catelory',
        }
        widgets={
            'title' : forms.TextInput(attrs={'row' :1, 'placeholder':'Add a title...', 'class':'front2 text-5m'}) ,
            'image': forms.FileInput(),
            'file': forms.FileInput(),
            'video':forms.FileInput(),
            'audio':forms.FileInput(),
            'body': forms.Textarea(attrs={'rows':3, 'placeholder':'Add a caption...', 'class':'front1 text-3xl'}),
            'tags': forms.CheckboxSelectMultiple(),
        }

class CommentCreateForm(ModelForm):
    class Meta:
        model=Comment
        #fields: là các trường mà form sẽ xử lí(nếu cần tất cả các trường thì fields="__all__")
        fields=['body']
        #labels: Cung cấp nhãn hiển thị cho trường body (đặt tên là "Caption").
        labels={ 
            'body': '',
        }
        '''widgets: Sử dụng các widget tùy chỉnh để thêm thuộc tính CSS
          và cấu hình cho các trường nhập liệu (Textarea cho body và TextInput cho url).'''
        widgets={
            'body': forms.Textarea(attrs={'rows':3, 'placeholder':'Add a comment...', 'class':'front1 text-3xl'}),
        }

class CommentEditForm(ModelForm):
    class Meta:
        model=Comment
        #fields: là các trường mà form sẽ xử lí(nếu cần tất cả các trường thì fields="__all__")
        fields=['body']
        #labels: Cung cấp nhãn hiển thị cho trường body (đặt tên là "Caption").
        labels={ 
            'body': '',
        }
        '''widgets: Sử dụng các widget tùy chỉnh để thêm thuộc tính CSS
          và cấu hình cho các trường nhập liệu (Textarea cho body và TextInput cho url).'''
        widgets={
            'body': forms.Textarea(attrs={'rows':3, 'placeholder':'Add a comment...', 'class':'front1 text-3xl'}),
        }


class ReplyCreateForm(ModelForm):
    class Meta:
        model=Reply
        #fields: là các trường mà form sẽ xử lí(nếu cần tất cả các trường thì fields="__all__")
        fields=['body']
        #labels: Cung cấp nhãn hiển thị cho trường body (đặt tên là "Caption").
        labels={ 
            'body': '',
        }
        '''widgets: Sử dụng các widget tùy chỉnh để thêm thuộc tính CSS
          và cấu hình cho các trường nhập liệu (Textarea cho body và TextInput cho url).'''
        widgets={
            'body': forms.Textarea(attrs={'rows':3, 'placeholder':'Add a reply...', 'class':'front1 text-3xl'}),
        }

class ReplyEditForm(ModelForm):
    class Meta:
        model=Reply
        #fields: là các trường mà form sẽ xử lí(nếu cần tất cả các trường thì fields="__all__")
        fields=['body']
        #labels: Cung cấp nhãn hiển thị cho trường body (đặt tên là "Caption").
        labels={ 
            'body': '',
        }
        '''widgets: Sử dụng các widget tùy chỉnh để thêm thuộc tính CSS
          và cấu hình cho các trường nhập liệu (Textarea cho body và TextInput cho url).'''
        widgets={
            'body': forms.Textarea(attrs={'rows':3, 'placeholder':'Add a reply...', 'class':'front1 text-3xl'}),
        }
        
class SearchUserForm(ModelForm):
    class Meta:
        model=User
        fields=['username']
            