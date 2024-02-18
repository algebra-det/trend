from django.contrib import admin
from .models import Product, ProductCategory, ProductRequest

admin.site.register(Product)
admin.site.register(ProductCategory)


def fullfil(modeladmin, request, queryset):
    queryset.update(fullfilled=True)
    fullfil.short_description = 'Mark selected request(s) as fullfilled'

def unfullfil(modeladmin, request, queryset):
    queryset.update(fullfilled=False)
    unfullfil.short_description = 'Mark selected request(s) as unfulfilled'


@admin.register(ProductRequest)
class ProductRequestAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'fullfilled']
    search_fields = ['user__username', 'fullfilled']
    actions = [ fullfil, unfullfil]