from django.db import models
from account.models import MyUser

def product_directory_path(instance, filename):
    return 'products/{}/{}'.format(instance.title, filename)


class ProductCategory(models.Model):
    title = models.CharField(max_length=30, unique=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title

class Product(models.Model):
    title = models.CharField(max_length=30)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    description = models.TextField()
    cost = models.IntegerField(default=0)
    points = models.IntegerField()
    hearts = models.IntegerField(default=0)
    basket = models.IntegerField(default=0)
    image = models.ImageField(upload_to=product_directory_path)

    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class ProductRequest(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='productrequests')
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='productrequests')
    fullfilled = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Function for sending the product request to the admin
    def send_request_to_admin(self):
        pass

    def __str__(self):
        return self.product.title