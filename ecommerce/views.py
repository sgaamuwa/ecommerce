# from django.shortcuts import render
from django.conf import settings
from allauth.account import app_settings as allauth_settings
from rest_auth.registration.views import RegisterView
from rest_framework.response import Response
from rest_framework import generics, status
from rest_auth.app_settings import (TokenSerializer,
                                    JWTSerializer,
                                    create_token)
from ecommerce.serializers import (
    ShippingRegionSerializer,
    DepartmentsSerializer,
    CategorySerializer,
    ShippingSerializer,
    ProductSerializer,
    ReviewSerializer,
    TaxSerializer
)
from ecommerce.models import (
    Customer,
    ShippingRegion,
    Department,
    Category,
    Product,
    Review,
    Tax
)
# Create your views here.


class CustomRegisterView(RegisterView):
    queryset = Customer.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        data = {
            "customer": {
                "schema": self.get_response_data(user)['user']
            },
            "accessToken": "Bearer "+self.get_response_data(user)['token'],
            "expires_in": "24h"
        }
        return Response(data,
                        status=status.HTTP_201_CREATED,
                        headers=headers)


class DepartmentListView(generics.ListAPIView):
    """View to get the department list"""

    queryset = Department.objects.all()
    serializer_class = DepartmentsSerializer


class DepartmentDetailView(generics.RetrieveAPIView):
    """View to get a specific department"""

    queryset = Department.objects.all()
    serializer_class = DepartmentsSerializer


class CategoryListView(generics.ListAPIView):
    """View returning the categorylist"""
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.all()

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        count = queryset.count()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        data = {
            "count": count,
            "rows": serializer.data
        }
        return Response(data)


class CategoryDetailView(generics.RetrieveAPIView):
    """View to return a single category"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDepartmentListView(generics.ListAPIView):
    """View to return categories within a specific department"""
    serializer_class = CategorySerializer

    def get_queryset(self):
        department_id = self.kwargs.get("department_id")
        return Category.objects.filter(department_id=department_id)


class CategoryProductListView(generics.ListAPIView):
    """View to return categories attached to a particular product"""
    serializer_class = CategorySerializer

    def get_queryset(self):
        product_id = self.kwargs.get("product_id")
        return Category.objects.filter(products__product_id=product_id)


class ProductListView(generics.ListAPIView):
    """View returning the categorylist"""
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.all()

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        count = queryset.count()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        data = {
            "count": count,
            "rows": serializer.data
        }
        return Response(data)


class ProductDetailView(generics.RetrieveAPIView):
    """View to return a single product based on it's id"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductCategoryListView(generics.ListAPIView):
    """View to return products in a given category"""
    serializer_class = ProductSerializer

    def get_queryset(self):
        category_id = self.kwargs.get("category_id")
        return Product.objects.filter(categories=category_id)

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        count = queryset.count()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        data = {
            "count": count,
            "rows": serializer.data
        }
        return Response(data)


class ProductDepartmentListView(generics.ListAPIView):
    """View to return the products within a certain department"""
    serializer_class = ProductSerializer

    def get_queryset(self):
        department_id = self.kwargs.get("department_id")
        categories = Category.objects.filter(department_id=department_id)
        return Product.objects.filter(categories__in=categories)

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        count = queryset.count()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        data = {
            "count": count,
            "rows": serializer.data
        }
        return Response(data)


class ProductReviewListCreateView(generics.ListCreateAPIView):
    """View that returns the reviews for a particular produc"""
    serializer_class = ReviewSerializer

    def get_queryset(self):
        product_id = self.kwargs.get("pk")
        reviews = Product.objects.get(product_id=product_id).reviews.all()
        return Review.objects.filter(review_id__in=reviews)

    def perform_create(self, serializer):
        product_id = self.kwargs.get("pk")
        serializer.save(product_id=product_id)


class TaxListView(generics.ListAPIView):
    """View that returns the taxes to be used"""
    queryset = Tax.objects.all()
    serializer_class = TaxSerializer


class TaxDetailView(generics.RetrieveAPIView):
    """View to return a particular tax"""
    queryset = Tax.objects.all()
    serializer_class = TaxSerializer


class ShippingRegionListView(generics.ListAPIView):
    """View to list the different shipping regions"""
    queryset = ShippingRegion.objects.all()
    serializer_class = ShippingRegionSerializer


class ShippingRegionShippingsListView(generics.ListAPIView):
    """View to return a list of shippings associated with a shipping region"""
    serializer_class = ShippingSerializer

    def get_queryset(self):
        shipping_region_id = self.kwargs.get("pk")
        shippings = ShippingRegion.objects.get(shipping_region_id=shipping_region_id).shippings
        return shippings
