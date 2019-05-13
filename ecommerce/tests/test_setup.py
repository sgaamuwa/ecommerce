from ecommerce.models import (
    Customer,
    ShippingRegion,
    ShoppingCart,
    Department,
    Attribute,
    Category,
    Product,
    Review,
    Tax
)
from rest_framework.test import APIClient, APITestCase
from rest_framework.authtoken.


class BaseTestCase(APITestCase):
    """Base Test Case
    Sets up the different users to use for testing 
    """

    def setUp(self):
        # create two clients to use for testing
        self.client = APIClient()
        self.client_2 = APIClient()
        # add two users to the system
        self.user_1 = Customer.objects.create_user(
            username="sgaamuwa",
            email="sgaamuwa@example.com",
            password="sam7did83",
            name="samuelgaamuwa",
            credit_card="eidhaodkddkdoe",
            address_1="50 Othaya",
            address_2="Upper Hill Lane",
            city="Nairobi",
            region="East Africa",
            country="Kenya",
            day_phone="0788418457",
            eve_phone="0738481681",
            mob_phone="0765752183"
        )
        self.user_2 = Customer.objects.create_user(
            username="gsamuel",
            email="samuelgaamuwa@example.com",
            password="sam7did83",
            name="samuelgaamuwa",
            credit_card="eidhaodkddkdoe",
            address_1="50 Othaya",
            address_2="Upper Hill Lane",
            city="Nairobi",
            region="East Africa",
            country="Kenya",
            day_phone="0788418457",
            eve_phone="0738481681",
            mob_phone="0765752183"
        )
        # login in the users
        self.client.login(
            username="sgaamuwa",
            email="sgaamuwa@example.com",
            password="sam7did83"
        )
        self.client_2.login(
            username="gsamuel",
            email="samuelgaamuwa@example.com",
            password="sam7did83"
        )

        # get tokens for the users

