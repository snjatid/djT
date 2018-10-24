from django.db import models

from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,AbstractUser,UserManager,User,BaseUserManager

class UserManage(BaseUserManager):
    # 创建用户
    def _create_user(self, username, telephone, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        user = self.model(username=username, telephone=telephone, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, username, telephone, password, **extra_fields):
        extra_fields['is_superuser'] = False
        extra_fields['is_staff'] = False
        return self._create_user(username, telephone, password, **extra_fields)

    def create_superuser(self, username, telephone, password, **extra_fields):
        extra_fields['is_superuser'] = True
        extra_fields['is_staff'] = True
        print(extra_fields)
        return self._create_user(username, telephone, password, **extra_fields)




class User(AbstractBaseUser,PermissionsMixin):
    '''
    User重构  拓展
    '''
    telephone = models.CharField(max_length=11,unique=True)
    username = models.CharField(max_length=50)
    email = models.EmailField(blank=True)
    # 账号是否激活
    is_active = models.BooleanField(default=True)
    # 登陆时间
    join_data = models.DateTimeField(auto_now_add=True)
    #是否员工    blank = True表示可以为空  null = True 表示可以为null
    is_staff = models.BooleanField(blank=True)

    #python manage.py createsuperuser (email,) telephone username password
    # 更换注册顺序，手机号，用户名，密码

    EMAIL_FIELD = 'email'
    # 使用authenticate验证时用那个字段验证，
    USERNAME_FIELD = 'telephone'
    # python manage.py createsuperuser 使用时第一个字段为手机号telephone 第二个为username,第三个email,第四个password
    REQUIRED_FIELDS = ['username','email']

    objects = UserManager()

