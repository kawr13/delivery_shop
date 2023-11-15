from django.contrib import admin
from .models import *
# Register your models here.


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class BasketTabularInline(admin.TabularInline):
    model = Basket
    extra = 1

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ProductImageInline,
    ]
    list_display = ('name', 'description', 'price', 'quantity', 'is_active')

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'username', 'phone', 'address')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [
        BasketTabularInline,
    ]
    list_display = ('user', 'quantity', 'created_timestamp')

@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'created_timestamp')

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('street', 'city')

@admin.register(DeliveryOption)
class DeliveryOptionAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price')

@admin.register(RecurringDeliverySchedule)
class RecurringDeliveryScheduleAdmin(admin.ModelAdmin):
    list_display = ('delivery_option', 'start_date', 'end_date')

@admin.register(DeliveryAtAddress)
class DeliveryAtAddressAdmin(admin.ModelAdmin):
    list_display = ('delivery_option', 'address')

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image')

