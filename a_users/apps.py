from django.apps import AppConfig


class AUsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'a_users'
    #luu tin hieu dang nhap tu nguoi dung de tu dong tao 1 profile
    def ready(self):
        import a_users.signals