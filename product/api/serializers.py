from product.models import Product, ProductRequest

from rest_framework import serializers

class ProductSerailizer(serializers.ModelSerializer):

    class Meta:
        model = Product
        exclude = ['category', 'cost', 'is_active']

class ProductDetailSerailizer(serializers.ModelSerializer):
    related = serializers.SerializerMethodField('get_related')

    class Meta:
        model = Product
        exclude = ['category', 'cost', 'is_active']

    def get_related(self, product):
        related = Product.objects.filter(category=product.category).exclude(pk=product.id)[:10]
        serializer = ProductSerailizer(related, many=True)
        return serializer.data