from rest_framework import serializers
from rest_auth.registration.serializers import RegisterSerializer
from ecommerce.models import (
    ShoppingCartItem,
    AttributeValue,
    ShippingRegion,
    ShoppingCart,
    OrderDetail,
    Department,
    Attribute,
    Category,
    Customer,
    Shipping,
    Product,
    Review,
    Orders,
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


class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = ("attribute_id", "name",)


class AttributeValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeValue
        fields = ("attribute_value_id", "value",)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class ProductLocationsSerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField()
    department_id = serializers.SerializerMethodField()
    department_name = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = (
            "category_id",
            "category_name",
            "department_id",
            "department_name"
        )

    def get_category_name(self, obj):
        return obj.name

    def get_department_id(self, obj):
        return obj.department_id.department_id

    def get_department_name(self, obj):
        return obj.department_id.name


class ReviewCreateSerializer(serializers.ModelSerializer):
    customer_id = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.all(),
        required=False
    )

    class Meta:
        model = Review
        fields = "__all__"


class ReviewListSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ("name", "review", "rating", "created_on")

    def get_name(self, obj):
        return obj.customer_id.name


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


class ShoppingCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingCart
        fields = ("cart_id",)


class ShoppingCartItemSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()
    subtotal = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    attributes = serializers.SerializerMethodField()

    class Meta:
        model = ShoppingCartItem
        fields = (
            'item_id',
            'name',
            'attributes',
            'product_id',
            'price',
            'quantity',
            'image',
            'subtotal'
        )

    # price is not part of the item so we have to source for it
    def get_price(self, obj):
        return obj.product_id.price

    # we need to calculate the subtotal for each of the items
    def get_subtotal(self, obj):
        return obj.product_id.price*obj.quantity

    def get_name(self, obj):
        return obj.product_id.name

    def get_image(self, obj):
        return obj.product_id.image

    def get_attributes(self, obj):
        return [attribute.value for attribute in obj.attributes.all()]


class ShoppingCartItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingCartItem
        fields = ("shopping_cart_id", "product_id", "attributes")


class ShoppingCartItemUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingCartItem
        fields = ("quantity",)


class OrderDetailItemSerializer(serializers.ModelSerializer):
    subtotal = serializers.SerializerMethodField()
    product_name = serializers.SerializerMethodField()
    attributes = serializers.SerializerMethodField()

    class Meta:
        model = OrderDetail
        fields = (
            "product_id",
            "attributes",
            "product_name",
            "quantity",
            "unit_cost",
            "subtotal"
        )

    def get_subtotal(self, obj):
        return obj.quantity*obj.product_id.price

    def get_product_name(self, obj):
        return obj.product_id.name

    def get_attributes(self, obj):
        return [attribute.value for attribute in obj.attributes.all()]


class OrderDetailSerializer(serializers.ModelSerializer):
    order_details = OrderDetailItemSerializer(many=True)

    class Meta:
        model = Orders
        fields = (
            "order_id",
            "order_details",
        )


class OrderCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = ("cart")
