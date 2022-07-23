from distutils.command.upload import upload
from pyexpat import model
from tabnanny import verbose
from tkinter.tix import Tree
from django.urls import reverse
from django.db import models
from accounts.models import Account
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Category(models.Model):
    category_name=models.CharField(max_length=50,unique=True)
    slug=models.SlugField(max_length=100,unique=True)
    descriptions=models.TextField(max_length=250,unique=True)
    cat_image = models.ImageField(upload_to='photos/category',blank=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.category_name

    def get_url(self):
        return reverse('products_by_category',args=[self.slug])

        
class Category_Offer(models.Model):
    category = models.OneToOneField(Category,on_delete=models.CASCADE)
    discount = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(100)])
    active = models.BooleanField( default=True)
    def __str__(self):
            return self.category.category_name
