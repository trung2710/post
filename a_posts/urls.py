
from django.urls import path, include
from a_posts import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    #path('', views.index),
    path('', views.login, name='login'),
    path('create', views.post_create_view, name='post-create'),
    #them 1 gia tri pk, tuong ung voi id cua bai dang
    #/<pk>/ : day la cach gui du lieu qua phan phu tro bang cach su dung url, du lieu o day
    # la id cua bai viet
    path('delete/<pk>/', views.post_delete_view, name='post-delete'),
    path('edit/<pk>/', views.post_edit_view, name='post-edit'),
    path('page/<pk>/', views.post_page_view, name='post'),
    path('category/<tag>/', views.login, name='category'),
    path('accounts/', include('allauth.urls')),
    path('commentsend/<pk>/', views.comment_send, name='comment-send'),
    path('replysend/<pk>/', views.reply_send, name='reply-send'),
    path('comment/edit/<pk>/', views.comment_edit_view, name='comment-edit'),
    path('reply/edit/<pk>/', views.reply_edit_view, name='reply-edit'),
    path('comment/delete/<pk>/', views.comment_delete_view, name='comment-delete'),
    path('reply/delete/<pk>/', views.reply_delete_view, name='reply-delete'),
    #like post, comment, reply
    path('post/like/<pk>/', views.like_post, name='like-post'),
    path('comment/like/<pk>/', views.like_comment, name='like-comment'),
    path('reply/like/<pk>/', views.like_reply, name='like-reply'),
    #duong dan tim kiem user theo username
    path('search/', views.search_view, name='search'),

]
urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)