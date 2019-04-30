# from django.shortcuts import render
from rest_auth.registration.views import RegisterView
from rest_framework.response import Response
from rest_framework import status, generics
from ecommerce.serializers import (
    DepartmentsSerializer,
    CategorySerializer,
    ProductSerializer
)
from ecommerce.models import (
    Department,
    Category,
    Product
)
# Create your views here.


class CustomRegisterView(RegisterView):
    # serializer_class = RegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(self.get_response_data(user),
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


class CategoryDepartmentDetailView(generics.ListAPIView):
    """View to return categories within a specific department"""
    serializer_class = CategorySerializer

    def get_queryset(self):
        department_id = self.kwargs.get("department_id")
        return Category.objects.filter(department_id=department_id)


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
