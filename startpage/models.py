from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AnonymousUser


class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.ForeignKey('Address', on_delete=models.CASCADE, blank=True, null=True)
    device = models.CharField(max_length=256)

    def __str__(self):
        if self.username:
            username = self.username
        else:
            username = self.device
        return str(username)


class Address(models.Model):
    street = models.CharField(max_length=150)
    city = models.CharField(max_length=100)
    hause = models.CharField(max_length=100)
    apartment = models.CharField(max_length=100)
    orders = models.ForeignKey('Order', on_delete=models.CASCADE, blank=True, null=True)


class BasketQuerySet(models.QuerySet):

    def total_sum(self):
        return sum(basket.total() for basket in self)

    def total_quantity(self):
        return sum(basket.quantity for basket in self)


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    order = models.ForeignKey('Order', on_delete=models.CASCADE, null=True, blank=True)
    objects = BasketQuerySet.as_manager()

    def total(self):
        return self.quantity * self.product.price


class Product(models.Model):

    name = models.CharField(max_length=256)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField()
    category = models.ForeignKey('Category', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)  # Делаем сортировку по дате публикации
        indexes = (
            models.Index(fields=['-created_at']),  # Добавляем индексы для ускорения работы с базой данных
        )

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products_images')


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    delivery_option = models.ForeignKey('DeliveryOption', on_delete=models.CASCADE, blank=True, null=True)
    total_sum = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return str(self.id)


class DeliveryOption(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class RecurringDeliverySchedule(models.Model):  
    delivery_option = models.ForeignKey(DeliveryOption, on_delete=models.CASCADE)    
    start_date = models.DateField()
    end_date = models.DateField()


class DeliveryAtAddress(models.Model):
   delivery_option = models.ForeignKey(DeliveryOption, on_delete=models.CASCADE)
   address = models.ForeignKey(Address, on_delete=models.CASCADE)
   
   
   git filter-branch --force --index-filter "git rm --cached --ignore-unmatch static/vezb3ky9.exe --prune-empty --tag-name-filter cat -- --all