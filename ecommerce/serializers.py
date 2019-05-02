from rest_framework import serializers
from rest_auth.registration.serializers import RegisterSerializer
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from ecommerce.models import (
    ShippingRegion,
    Department,
    Category,
    Customer,
    Shipping,
    Product,
    Review,
    Tax
)


class RegistrationSerializer(RegisterSerializer):
    print('got here first')
    customer_id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100)
    credit_card = serializers.CharField(max_length=255)
    address_1 = serializers.CharField(allow_blank=True, required=False)
    address_2 = serializers.CharField(allow_blank=True, required=False)
    city = serializers.CharField(allow_blank=True, required=False)
    region = serializers.CharField(allow_blank=True, required=False)
    postal_code = serializers.CharField(allow_blank=True, required=False)
    country = serializers.CharField(allow_blank=True, required=False)
    day_phone = serializers.CharField(allow_blank=True, required=False)
    eve_phone = serializers.CharField(allow_blank=True, required=False)
    mob_phone = serializers.CharField(allow_blank=True, required=False)

    def get_cleaned_data(self):
        data_dict = super(RegistrationSerializer, self).get_cleaned_data()
        data_dict['name'] = self.validated_data.get('name')
        data_dict['credit_card'] = self.validated_data.get('credit_card')
        data_dict['address_1'] = self.validated_data.get('address_1')
        data_dict['address_2'] = self.validated_data.get('address_2')
        data_dict['city'] = self.validated_data.get('city')
        data_dict['region'] = self.validated_data.get('region')
        data_dict['postal_code'] = self.validated_data.get('postal_code')
        data_dict['country'] = self.validated_data.get('country')
        data_dict['day_phone'] = self.validated_data.get('day_phone')
        data_dict['eve_phone'] = self.validated_data.get('eve_phone')
        data_dict['mob_phone'] = self.validated_data.get('mob_phone')
        return data_dict


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = (
            "customer_id",
            "name",
            "email",
            "address_1",
            "address_2",
            "city",
            "region",
            "postal_code",
            "country",
            "shipping_region_id",
            "day_phone",
            "eve_phone",
            "mob_phone",
            "credit_card"
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


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"


class TaxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tax
        fields = "__all__"


class ShippingRegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingRegion
        fields = "__all__"


class ShippingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipping
        fields = "__all__"
