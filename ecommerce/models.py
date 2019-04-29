from django.db import models

# Create your models here.
    

class Department(models.Model):
    """ Model for the different departments"""
    department_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    descprition = models.CharField(max_length=1000)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    """Model for the different categories"""
    category_id = models.AutoField(primary_key=True)
    department_id = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="categories"
    )
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    """Model for the different products"""
    product_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.CharField(max_length=150, null=True, blank=True)
    image_2 = models.CharField(max_length=150, null=True, blank=True)
    thumbnail = models.CharField(max_length=150, null=True, blank=True)
    display = models.SmallIntegerField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Attribute(models.Model):
    """
        Stores Attributes for the products
        Attributes include things like size and colour
    """
    attribute_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    products = models.ManyToManyField(Product)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class AttributeValue(models.Model):
    """
        Stores the different values for each attribute
        Attribute Values include things like XXL, M, White, Yellow
    """
    attribute_value_id = models.AutoField(primary_key=True)
    attribute_id = models.ForeignKey(
        Attribute,
        on_delete=models.CASCADE,
        related_name="attribute_values"
    )
    value = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.value


class ShoppingCart(models.Model):
    """Defines the Shopping Cart as it is used"""

    item_id = models.AutoField(primary_key=True)
    cart_id = models.CharField(max_length=32)
    product_id = models.IntegerField()
    attributes = models.CharField(max_length=1000)
    quantity = models.IntegerField()
    buy_now = models.BooleanField(default=False)
    added_on = models.DateTimeField(auto_now_add=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)


class ShippingRegion(models.Model):
    """Defines and lists the different shipping regions available"""
    shipping_region_id = models.AutoField(primary_key=True)
    shipping_region = models.CharField(max_length=100)

    def __str__(self):
        return self.shipping_region


class Customer(models.Model):
    """Defines the customer and their attributes"""
    customer_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=50)
    credit_card = models.TextField(null=True, blank=True)
    address_1 = models.CharField(max_length=100, null=True, blank=True)
    address_2 = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    region = models.CharField(max_length=100, null=True, blank=True)
    postal_code = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    shipping_region_id = models.ForeignKey(
        ShippingRegion,
        on_delete=models.CASCADE
    )
    day_phone = models.CharField(max_length=100, null=True, blank=True)
    eve_phone = models.CharField(max_length=100, null=True, blank=True)
    mob_phone = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name


class Shipping(models.Model):
    shipping_id = models.AutoField(primary_key=True)
    shipping_type = models.CharField(max_length=100)
    shipping_cost = models.DecimalField(max_digits=10, decimal_place=2)
    shipping_region_id = models.ForeignKey(
        ShippingRegion,
        on_delete=models.CASCADE
    )


class Tax(models.Model):
    """Defines the different tax types to be attached to orders"""
    tax_id = models.AutoField(primary_key=True)
    tax_type = models.CharField(max_length=100)
    tax_percentage = models.DecimalField(max_digits=10, decimal_place=2)

    def __str__(self):
        return self.tax_type


class Orders(models.Model):
    """Defines the different orders"""
    order_id = models.AutoField(primary_key=True)
    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00
    )
    created_on = models.DateTimeField(auto_now_add=True)
    shipped_on = models.DateTimeField(null=True, blank=True)
    status = models.IntegerField(default=0)
    comments = models.CharField(max_length=255, null=True, blank=True)
    customer_id = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="orders",
        null=True,
        blank=True
    )
    auth_code = models.CharField(max_length=50, null=True, blank=True)
    reference = models.CharField(max_length=50, null=True, blank=True)
    shipping_id = models.ForeignKey(
        Shipping,
        on_delete=models.CASCADE,
        related_name="orders",
        null=True,
        blank=True
    )
    tax_id = models.ForeignKey(
        Tax,
        on_delete=models.CASCADE,
        related_name="orders",
        null=True,
        blank=True
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)


class OrderDetail(models.Model):
    """Defines the details for a given order"""
    item_id = models.AutoField(primary_key=True)
    order_id = models.ForeignKey(
        Orders,
        on_delete=models.CASCADE,
        related_name="order_details"
    )
    product_id = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    attributes = models.CharField(max_length=1000)
    quantity = models.IntegerField()
    unit_cost = models.DecimalField(max_digits=10, decimal_place=2)


class Audit(models.Model):
    audit_id = models.AutoField(primary_key=True)
    order_id = models.ForeignKey(
        Orders,
        on_delete=models.CASCADE
    )
    created_on = models.DateTimeField(auto_now_add=True)
    message = models.TextField()
    code = models.IntegerField()


class Review(models.Model):
    """Defines the reviews made by customers for each product"""
    review_id = models.AutoField(primary_key=True)
    customer_id = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    product_id = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    review = models.TextField()
    rating = models.SmallIntegerField()
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.review


