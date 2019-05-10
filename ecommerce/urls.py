from django.urls import re_path
from django.conf.urls import url, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_auth.registration.views import VerifyEmailView
from ecommerce.views import (
    CustomRegisterView,
    DepartmentListView,
    DepartmentDetailView,
    CategoryListView,
    CategoryDetailView,
    CategoryProductListView,
    CategoryDepartmentListView,
    AttributeListView,
    AttributeDetailView,
    AttributeValuesListView,
    ProductListView,
    ProductDetailView,
    ProductCategoryListView,
    ProductDepartmentListView,
    ProductReviewListCreateView,
    TaxListView,
    TaxDetailView,
    ShippingRegionListView,
    ShippingRegionShippingsListView,
    ShoppingCartEmptyCart,
    ShoppingCartItemListView,
    ShoppingCartItemCreateView,
    ShoppingCartItemUpdateView,
    ShoppingCartTotalAmountView,
    ShoppingCartRetrieveCartView,
    ShoppingCartRemoveProductView,
    ShoppingCartGetSavedItemsView,
    ShoppingCartMoveItemtoCartView,
    ShoppingCartSaveItemForLaterView,
)

urlpatterns = [
    url(r'^customers/$', CustomRegisterView.as_view()),
    url(r'^customers/', include('rest_auth.urls')),
    url(r'^token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    url(r'^token/refresh/', TokenRefreshView.as_view()),
    re_path(r'^account-confirm-email/', VerifyEmailView.as_view()),
    re_path(
        r'^account-confirm-email/(?P<key>[-:\w]+)/$',
        VerifyEmailView.as_view(),
        name='account_confirm_email'
    ),
    url(r'^departments/$', DepartmentListView.as_view()),
    url(r'^departments/(?P<pk>[0-9]+)', DepartmentDetailView.as_view()),
    url(r'^categories/$', CategoryListView.as_view()),
    url(r'^categories/(?P<pk>[0-9]+)', CategoryDetailView.as_view()),
    url(
        r'^categories/inDepartment/(?P<department_id>[0-9]+)',
        CategoryDepartmentListView.as_view()
    ),
    url(
        r'^categories/inProduct/(?P<product_id>[0-9]+)',
        CategoryProductListView.as_view()
    ),
    url(r'^attributes/$', AttributeListView.as_view()),
    url(r'^attributes/(?P<pk>[0-9]+)/$', AttributeDetailView.as_view()),
    url(
        r'^attributes/values/(?P<attribute_id>[0-9]+)/$',
        AttributeValuesListView.as_view()
    ),
    url(r'^products/$', ProductListView.as_view()),
    url(r'^products/(?P<pk>[0-9]+)/$', ProductDetailView.as_view()),
    url(
        r'^products/inCategory/(?P<category_id>[0-9]+)',
        ProductCategoryListView.as_view()
    ),
    url(
        r'^products/inDepartment/(?P<department_id>[0-9]+)',
        ProductDepartmentListView.as_view()
    ),
    url(
        r'^products/(?P<pk>[0-9]+)/reviews/$',
        ProductReviewListCreateView.as_view()
    ),
    url(r'^tax/$', TaxListView.as_view()),
    url(r'^tax/(?P<pk>[0-9]+)', TaxDetailView.as_view()),
    url(r'^shipping/regions/$', ShippingRegionListView.as_view()),
    url(
        r'^shipping/regions/(?P<pk>[0-9]+)',
        ShippingRegionShippingsListView.as_view()
    ),
    url(
        r'^shoppingcart/generateUniqueId/$',
        ShoppingCartRetrieveCartView.as_view()
    ),
    url(r'^shoppingcart/add/$', ShoppingCartItemCreateView.as_view()),
    url(
        r'^shoppingcart/(?P<cart_id>[0-9a-f-]+)',
        ShoppingCartItemListView.as_view()
    ),
    url(
        r'^shoppingcart/update/(?P<pk>[0-9]+)',
        ShoppingCartItemUpdateView.as_view()
    ),
    url(
        r'^shoppingcart/empty/(?P<cart_id>[0-9a-f-]+)',
        ShoppingCartEmptyCart.as_view()
    ),
    url(
        r'^shoppingcart/moveToCart/(?P<pk>[0-9]+)',
        ShoppingCartMoveItemtoCartView.as_view()
    ),
    url(
        r'^shoppingcart/totalAmount/(?P<pk>[0-9a-f-]+)',
        ShoppingCartTotalAmountView.as_view()
    ),
    url(
        r'^shoppingcart/saveForLater/(?P<pk>[0-9]+)',
        ShoppingCartSaveItemForLaterView.as_view()
    ),
    url(
        r'^shoppingcart/getSaved/(?P<pk>[0-9a-f-]+)',
        ShoppingCartGetSavedItemsView.as_view()
    ),
    url(
        r'^shoppingcart/removeProduct/(?P<pk>[0-9]+)',
        ShoppingCartRemoveProductView.as_view()
    )
]
