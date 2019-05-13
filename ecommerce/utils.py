def calculateTotalAmountForCartItems(cart_items):
    """Function to calculate the total amount for given number of cart items"""
    totalAmount = sum([
        (cart_item.quantity*cart_item.product_id.price) for cart_item in cart_items  # noqa: E501
    ])
    return totalAmount
