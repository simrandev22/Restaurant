from django.db import models

# Create your models here.
class Form(models.Model):
    name=models.CharField(max_length=100)
    phone=models.CharField(max_length=50)
    email=models.EmailField()
    message=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)

class Category(models.Model):
    title=models.CharField(max_length=200)
    image=models.ImageField(upload_to="category_images",null=True)


    def __str__(self):
        return self.title


class Momo(models.Model):
    name=models.CharField(max_length=200)
    category=models. ForeignKey(Category, on_delete=models.CASCADE,related_name='items',null=True)
    desc=models.TextField()
    price=models.DecimalField(max_digits=8,decimal_places=2)
    images=models.ImageField(upload_to="images")
    is_available=models.BooleanField(default=True)
    created_at=models.DateField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)


class Review(models.Model):
    name=models.CharField(max_length=200)
    message=models.TextField()
    order=models.CharField(max_length=200,null=True)
    rating=models.PositiveSmallIntegerField()