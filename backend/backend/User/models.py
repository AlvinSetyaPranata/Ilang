from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)



class CustomUserManager(BaseUserManager):
    def create_user(self, **kwargs):
        user = self.model(**kwargs)
        user.set_password(kwargs["password"])

        user.save(using=self.db)

        return user



# Create your models here.
class CustomUser(AbstractBaseUser):
    id = models.BigAutoField(verbose_name="id", primary_key=True, unique=True)
    username = models.CharField(verbose_name="Username", max_length=20, unique=True)
    email = models.EmailField(verbose_name="Email", default=0, unique=True)
    phone = models.CharField(verbose_name="Phone", unique=True, max_length=20)
    bio = models.TextField(verbose_name="Bio", max_length=500)
    image = models.CharField(verbose_name="Image", max_length=300)    
    timestamp = models.DateTimeField(verbose_name="user-created", auto_now_add=True, editable=False)


    def has_module_perms(self, app_label):
        return True
    
    def has_perm(self, perm, obj=None):
        return True
    
    def has_perms(self, perm_list):
        return True

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'



class Post(models.Model):
    id = models.BigAutoField(verbose_name="id", primary_key=True, unique=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField(verbose_name="content", max_length=1000)
    date_created = models.DateTimeField(verbose_name="post-created" ,auto_now_add=True, editable=False)