from rest_framework import serializers
from ecommerce.models import (
    Customer,
    Department,
    Category,
    Product
)


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = (
            "customer_id",
            "name",
            "email",
            "address_1",
            "address_2",
            "city",
            "region"
        )


class DepartmentsSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Department
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"