from distutils.command.upload import upload
import email
from pyexpat import model
from sre_parse import State
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,User
from django.forms import IntegerField
from django.utils.html import format_html



# Create your models here.
class MyAcountManager(BaseUserManager):
    def create_user(self,first_name,last_name,username,email,phone_number,password=None):
        if not email:
            raise ValueError('user must have an email address')

        if not username:
            raise ValueError('user must have username')

        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
            phone_number=phone_number,

        )

        user.set_password(password)
        user.save(using=self.db)
        return user
    def create_superuser(self, first_name, last_name,email,username,password,phone_number):
        user = self.create_user(
            email  = self.normalize_email(email),
            username = username,
            password= password,
            first_name= first_name,
            last_name= last_name,
            phone_number=phone_number,
        )

        user.is_admin=True
        user.is_active=True
        user.is_staff=True
        user.is_superadmin=True
        user.save(using=self._db)
        return user
        
   


class Account(AbstractBaseUser): 
    first_name          =models.CharField( max_length=50)
    last_name           =models.CharField( max_length=50)
    username            =models.CharField( max_length=50,unique=True)
    email               =models.EmailField( max_length=254,unique=True)
    phone_number        =models.CharField( max_length=50, blank=True)
    

    #required 
    date_joined         =models.DateTimeField(auto_now_add=True)
    last_login          =models.DateTimeField(auto_now_add=True)
    is_admin            =models.BooleanField(default=False)
    is_staff            =models.BooleanField(default=False)
    is_active           =models.BooleanField(default=True)
    is_superadmin       =models.BooleanField(default=False)
    referel_code = models.CharField(max_length=50 , null=True , blank = True)
    referel_activated = models.BooleanField(default=False ,null = True )


    USERNAME_FIELD      ='email'
    REQUIRED_FIELDS     =['username','first_name','last_name']
    objects = MyAcountManager()

    def __str__(self):
        return self.email

    def has_perm(self,perm,obj=None):
        return self.is_admin


    def has_module_perms(self,add_label):

        return True


# class Profile(models.Model):
#     user = models.OneToOneField(Account,on_delete=models.CASCADE ,related_name='profile')
#     otp = models.CharField(max_length=100, null=True ,blank=True)


class UserProfile(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    first_name = models.CharField(blank=True,max_length=100,null=True)
    last_name = models.CharField(blank=True,max_length=100,null=True)
    email = models.EmailField(blank=True,max_length=100,null=True)
    address_line_1=models.CharField(blank=True, max_length=100)
    address_line_2=models.CharField(blank=True, max_length=100)
    profile_picture = models.ImageField(blank=True, upload_to='userprofile/')
    city = models.CharField(blank=True,max_length=100)
    State = models.CharField(blank=True,max_length=100)
    country = models.CharField(blank=True,max_length=100)
    pin =models.IntegerField(blank=True,null=True)

    def __str__(self):
        return self.user.first_name

    def full_address(self):
        return f'(self.address_line_1) (self.address_line_2)'



class Wallet(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    balance = models.FloatField( max_length=20, null = True, default= 0 )
    is_applied = models.BooleanField(default=False)