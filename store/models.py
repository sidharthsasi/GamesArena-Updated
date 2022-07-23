from distutils.command.upload import upload
from django.db import models
from category.models import Category
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.validators import FileExtensionValidator
# Create your models here.

class Product(models.Model):
    product_name = models.CharField(max_length=250, unique=True)
    slug         = models.SlugField(max_length=250, unique=True)
    description  = models.TextField( max_length=500, blank=True)
    price        = models.IntegerField()
    offer_price = models.IntegerField(null=True, blank=True)
    offer_perc =  models.IntegerField(null=True, blank=True, default= 0)
    images       =models.ImageField(upload_to='photos/product',validators=[FileExtensionValidator(allowed_extensions=["jpg","jpeg","webp"])])
    images2      =models.ImageField(upload_to ='photos/product',null=True,validators=[FileExtensionValidator(allowed_extensions=["jpg","jpeg","webp"])])
    images3      =models.ImageField(upload_to ='photos/product',null=True,validators=[FileExtensionValidator(allowed_extensions=["jpg","jpeg","webp"])])
    thumbnail = models.ImageField(upload_to='photos/product',null=True)
    stock        = models.IntegerField()
    is_available =models.BooleanField(default=True)
    category     = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date =models.DateTimeField( auto_now_add=True)
    modified_date=models.DateTimeField( auto_now=True)
    product_offer = models.IntegerField(null=True, blank=True ,default= 0, validators=[MinValueValidator(0),MaxValueValidator(100)])
    Is_offer_active = models.BooleanField(default=True)



    def get_url(self):
        return reverse('product_page',args=[self.category.slug, self.slug])

    def __str__(self):
        return self.product_name



