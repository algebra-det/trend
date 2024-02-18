from product.models import Product, ProductRequest
from .serializers import ProductSerailizer, ProductDetailSerailizer

from django.db.models import Q

from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination

from trend.pagination import CustomPagination

# For filter functionality
from rest_framework.filters import SearchFilter, OrderingFilter

class ProductAPIView(ListAPIView):
    serializer_class = ProductSerailizer
    queryset = Product.objects.filter(is_active=True)
    pagination_class = CustomPagination

    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title']
    ordering = ['points'] #for default ordering

    def get(self, request):
        return self.list(request)


class ProductDetailView(APIView):

    def get(self, request):
        try:
            id = request.GET.get('product_id')
            product = Product.objects.get(pk=id)
            if not product.is_active:
                return Response({"error": "Product doesn't exist"})
        except Product.DoesNotExist:
            return Response({"error": "product does not exist"}, status=404)
        
        serializer = ProductDetailSerailizer(product)
        result = {}
        result.update(serializer.data)
        result.update({"status": True})
        return Response(result, status=200)



class ProductBuyView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            user = request.user
            product = Product.objects.get(pk=request.data['product_id'])
            if not product.is_active:
                return Response({"error": "Product doesn't exist"})
        except Product.DoesNotExist:
            return Response({"error": "No Product Found"})
        
        if user.profile.credits >= product.points:
            product_request = ProductRequest()
            product_request.product = product
            product_request.user = user
            product_request.save()
            user.profile.credits = user.profile.credits - product.points
            user.profile.save()
            product.basket += 1
            product.save()
            return Response({"status": True, "message": "Prodotto ordinato con successo."})
        else:
            return Response({"error": "You do not have enough credits"})
