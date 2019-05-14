# from django.shortcuts import render
from rest_auth.registration.views import RegisterView
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.db import Error, transaction
from ecommerce.serializers import (
    ShoppingCartItemCreateSerializer,
    ShoppingCartItemUpdateSerializer,
    ShoppingCartItemSerializer,
    ProductLocationsSerializer,
    AttributeValueSerializer,
    ShippingRegionSerializer,
    ReviewCreateSerializer,
    DepartmentsSerializer,
    OrderDetailSerializer,
    ReviewListSerializer,
    AttributeSerializer,
    CategorySerializer,
    ShippingSerializer,
    ProductSerializer,
    TaxSerializer
)
from ecommerce.models import (
    Customer,
    ShoppingCartItem,
    ShippingRegion,
    ShoppingCart,
    OrderDetail,
    Department,
    Attribute,
    Category,
    Product,
    Orders,
    Tax
)
from ecommerce.pagination import StandardListPagination
from ecommerce.utils import calculateTotalAmountForCartItems
import uuid
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
    pagination_class = StandardListPagination


class DepartmentDetailView(generics.RetrieveAPIView):
    """View to get a specific department"""

    queryset = Department.objects.all()
    serializer_class = DepartmentsSerializer


class CategoryListView(generics.ListAPIView):
    """View returning the categorylist"""
    serializer_class = CategorySerializer
    pagination_class = StandardListPagination

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
    pagination_class = StandardListPagination

    def get_queryset(self):
        department_id = self.kwargs.get("department_id")
        return Category.objects.filter(department_id=department_id)


class CategoryProductListView(generics.ListAPIView):
    """View to return categories attached to a particular product"""
    serializer_class = CategorySerializer
    pagination_class = StandardListPagination

    def get_queryset(self):
        product_id = self.kwargs.get("product_id")
        return Category.objects.filter(products__product_id=product_id)


class AttributeListView(generics.ListAPIView):
    """View to return the various attributes we have available"""
    queryset = Attribute.objects.all()
    serializer_class = AttributeSerializer
    pagination_class = StandardListPagination


class AttributeDetailView(generics.RetrieveAPIView):
    """View to return a particular attribute based on the id passed in"""
    queryset = Attribute.objects.all()
    serializer_class = AttributeSerializer


class AttributeValuesListView(generics.ListAPIView):
    """View that returns the values associated with an attribute"""
    serializer_class = AttributeValueSerializer
    pagination_class = StandardListPagination

    def get_queryset(self):
        attribute_id = self.kwargs.get("attribute_id")
        return Attribute.objects.get(attribute_id=attribute_id).attribute_values.all()  # noqa: E501


class ProductListView(generics.ListAPIView):
    """View returning the categorylist"""
    serializer_class = ProductSerializer
    pagination_class = StandardListPagination

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
    pagination_class = StandardListPagination

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
    pagination_class = StandardListPagination

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
    serializer_class = ReviewCreateSerializer
    pagination_class = StandardListPagination
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        product_id = self.kwargs.get("pk")
        return Product.objects.get(product_id=product_id).reviews.all()

    def perform_create(self, serializer):
        product_id = self.kwargs.get("pk")
        product = Product.objects.get(product_id=product_id)
        user = self.request.user
        serializer.save(product_id=product, customer_id=user)

    def get_serializer_class(self):
        if self.action == 'list':
            return ReviewListSerializer
        return ReviewCreateSerializer,


class ProductLocationsListView(generics.ListAPIView):
    """View that returns the different categories a product is in"""
    serializer_class = ProductLocationsSerializer

    def get_queryset(self):
        product_id = self.kwargs.get("pk")
        return Product.objects.get(product_id=product_id).categories.all()


class TaxListView(generics.ListAPIView):
    """View that returns the taxes to be used"""
    queryset = Tax.objects.all()
    serializer_class = TaxSerializer
    pagination_class = StandardListPagination


class TaxDetailView(generics.RetrieveAPIView):
    """View to return a particular tax"""
    queryset = Tax.objects.all()
    serializer_class = TaxSerializer


class ShippingRegionListView(generics.ListAPIView):
    """View to list the different shipping regions"""
    queryset = ShippingRegion.objects.all()
    serializer_class = ShippingRegionSerializer
    pagination_class = StandardListPagination


class ShippingRegionShippingsListView(generics.ListAPIView):
    """View to return a list of shippings associated with a shipping region"""
    serializer_class = ShippingSerializer
    pagination_class = StandardListPagination

    def get_queryset(self):
        shipping_region_id = self.kwargs.get("pk")
        shippings = ShippingRegion.objects.get(
            shipping_region_id=shipping_region_id).shippings.all()
        return shippings


class ShoppingCartItemListView(generics.ListAPIView):
    """View to return the items inside a particular cart"""
    serializer_class = ShoppingCartItemSerializer

    def get_queryset(self):
        cart_id = self.kwargs.get("cart_id")
        return ShoppingCart.objects.get(cart_id=cart_id).shopping_cart_items


class ShoppingCartRetrieveCartView(APIView):

    def get(self, request, format=None):
        """Generate and return the cart id for a shopping cart"""
        cart_id = str(uuid.uuid4())
        shopping_cart = ShoppingCart(cart_id=cart_id)
        shopping_cart.save()
        return Response({"cart_id": cart_id})


class ShoppingCartItemCreateView(APIView):
    """View to create and add an item to a shopping cart"""

    def post(self, request, format=None):
        cart_id = request.data["cart_id"]
        # the cart Id provided is not the primary key for the shopping cart
        # we need to get the primary key to use for the relationship
        returned_shopping_cart_id = ShoppingCart.objects.get(
            cart_id=cart_id
            ).shopping_cart_id
        data = {
            "shopping_cart_id": returned_shopping_cart_id,
            "product_id": request.data["product_id"],
            "attributes": request.data["attributes"],
        }
        # check if the product already exists and increase the quantity instead
        if ShoppingCartItem.objects.filter(product_id=request.data["product_id"]).exists():  # noqa: E501
            item_to_update = ShoppingCartItem.objects.get(
                product_id=request.data["product_id"]
            )
            new_quantity = item_to_update.quantity + 1
            self.serializer = ShoppingCartItemUpdateSerializer(
                item_to_update,
                data={"quantity": new_quantity}
            )
        else:
            self.serializer = ShoppingCartItemCreateSerializer(data=data)
        if self.serializer.is_valid():
            self.serializer.save()
            # we need an output serializer for the list
            # only shopping cart items that a buy now should be returned
            output_serializer = ShoppingCartItemSerializer(
                ShoppingCart.objects.get(cart_id=cart_id).shopping_cart_items.filter(buy_now=True),  # noqa: E501
                many=True
            )
            return Response(
                output_serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            self.serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class ShoppingCartItemUpdateView(APIView):
    """Use this view to update an item in the shopping cart"""
    # queryset = ShoppingCartItem.objects.all()
    # serializer_class = ShoppingCartItemUpdateSerializer
    def patch(self, request, pk, format=None):
        try:
            self.shopping_cart_item = ShoppingCartItem.objects.get(item_id=pk)
        except ShoppingCartItem.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # reduce the received data down to only the quantity for update
        update_data = {
            key: value for key, value in request.data.items() if key == "quantity"  # noqa: E501
        }
        serializer = ShoppingCartItemUpdateSerializer(
            self.shopping_cart_item,
            data=update_data
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ShoppingCartMoveItemtoCartView(APIView):
    """View to move saved items back to the shopping cart"""

    def get(self, request, pk, format=None):
        try:
            self.shopping_cart_item = ShoppingCartItem.objects.get(item_id=pk)
        except ShoppingCartItem.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if self.shopping_cart_item.buy_now is True:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        self.shopping_cart_item.buy_now = True
        self.shopping_cart_item.save()
        return Response(status=status.HTTP_200_OK)


class ShoppingCartSaveItemForLaterView(APIView):
    """View to move item from the cart and save it for later"""

    def get(self, request, pk, format=None):
        try:
            self.shopping_cart_item = ShoppingCartItem.objects.get(item_id=pk)
        except ShoppingCartItem.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if self.shopping_cart_item.buy_now is False:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        self.shopping_cart_item.buy_now = False
        self.shopping_cart_item.save()
        return Response(status=status.HTTP_200_OK)


class ShoppingCartTotalAmountView(APIView):
    """View to return the total amount for the items in a cart"""

    def get(self, request, pk, format=None):
        try:
            self.shopping_cart = ShoppingCart.objects.get(cart_id=pk)
        except ShoppingCart.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        cart_items = self.shopping_cart.shopping_cart_items.filter(buy_now=True)  # noqa: E501
        total_amount = calculateTotalAmountForCartItems(cart_items)
        return Response(
            {"totalAmount": total_amount},
            status=status.HTTP_200_OK
        )


class ShoppingCartRemoveProductView(generics.DestroyAPIView):
    """View to delete an item from the cart"""
    serializer_class = ShoppingCartItemSerializer
    queryset = ShoppingCartItem.objects.all()


class ShoppingCartGetSavedItemsView(APIView):
    """View to return the items that were saved for later in the cart"""

    def get(self, request, pk, format=None):
        try:
            self.shopping_cart = ShoppingCart.objects.get(cart_id=pk)
        except ShoppingCart.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        cart_items = self.shopping_cart.shopping_cart_items.filter(buy_now=False).values_list("product_id", flat=True)  # noqa: E501
        print(cart_items)
        serializer = ProductSerializer(
            Product.objects.filter(product_id__in=cart_items),
            many=True
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class ShoppingCartEmptyCart(generics.DestroyAPIView):
    """View that deletes all the items in a cart"""
    serializer_class = ShoppingCartItemSerializer

    def get_queryset(self):
        cart_id = self.kwargs.get("cart_id")
        return ShoppingCart.objects.get(cart_id=cart_id).shopping_cart_items.all()  # noqa: E501


class OrdersListView(generics.ListAPIView):
    """View to return the different orders for a user"""
    serializer_class = OrderDetailSerializer

    def get_queryset(self):
        customer_id = self.request.user.id
        return Orders.objects.filter(customer_id=customer_id)


class OrdersCreateView(APIView):
    """
    View to create an order from a supplied cart
    """
    def post(self, request, format=None):
        cart_id = request.data["cart_id"]
        shopping_cart_items = ShoppingCart.objects.get(cart_id=cart_id).shopping_cart_items.filter(buy_now=True)  # noqa: E501
        if not shopping_cart_items:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        total_amount = calculateTotalAmountForCartItems(shopping_cart_items)

        order = Orders.objects.create(total_amount=total_amount)
        order.save()
        # interate through and create the order items from the list
        try:
            # we need to reverse the changes if one of them fails
            with transaction.atomic():
                for shopping_cart_item in shopping_cart_items:
                    order_detail = OrderDetail.create_from_shopping_cart_item(
                        shopping_cart_item,
                        order
                    )
                    order_detail.save()
        except Error:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(
            {"order_id": order.order_id},
            status=status.HTTP_201_CREATED
        )


class OrdersDetailView(generics.RetrieveAPIView):
    """
        View to return the details of an order
    """
    serializer_class = OrderDetailSerializer
    queryset = Orders.objects.all()
