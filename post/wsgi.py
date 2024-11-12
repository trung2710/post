"""
WSGI config for post project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""
#Web Server Gateway Interface
'''Giao diện Cổng vào Máy chủ Web là một quy ước gọi đơn giản cho các máy chủ web 
để chuyển tiếp các yêu cầu đến các ứng dụng web hoặc khuôn khổ được viết bằng 
ngôn ngữ lập trình Python.'''
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'post.settings')

application = get_wsgi_application()
