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
    CategoryDepartmentDetailView,
    ProductListView
)

urlpatterns = [
    url(r'^customer/$', CustomRegisterView.as_view()),
    url(r'^customer/', include('rest_auth.urls')),
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
        CategoryDepartmentDetailView.as_view()
    ),
    url(r'^products/$', ProductListView.as_view())
]
