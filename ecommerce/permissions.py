from ecommerce.models import Orders, Customer
from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Object-level permission to allow only owners to 
    Interact with an object, that is view, edit and create
    """

    def has_object_permission(self, request, view, obj):
        # return true if customer is owner of the order
        if type(obj) is Orders:
            return obj.customer_id == request.user
        if type(obj) is Customer:
            return obj.customer_id == request.user
