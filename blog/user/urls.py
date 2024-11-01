# Django imports
from django.urls import path
from django.shortcuts import render
from django.contrib.auth.views import LogoutView
# User views imports
from user.views import LogoutView, CustomLoginView, SignupView
# jwt token based authentication
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
urlpatterns = [
    # ORM based authentication
    path('login/', CustomLoginView.as_view(), name="login"),
    path('home/', lambda request: render(request, 'user/home.html'), name='home'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', SignupView.as_view(), name="create_user"),
    
    # jwt token based authentication
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), # token generation
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # token refresh
    path('api/token/logout/', LogoutView.as_view(), name='token_logout'), # token blacklist
]


# Token part -> header , payload, signature(each part is separated by a dot)
# ex token(access/request): eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzMwMzAzNjU5LCJpYXQiOjE3MzAzMDMyNjUsImp0aSI6IjVmYjg0MjMwNDFiNDQ3ZGNhNzk0ODI0OWMzMjdkOGRiIiwidXNlcl9pZCI6MX0.C-lJBzCUDrPEidqxL2Cv2SmFCVsHWNMDSchXB2bKKZU
# header -> eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9
# payload -> eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzMwMzAzNjU5LCJpYXQiOjE3MzAzMDMyNjUsImp0aSI6IjVmYjg0MjMwNDFiNDQ3ZGNhNzk0ODI0OWMzMjdkOGRiIiwidXNlcl9pZCI6MX0.
# signature -> C-lJBzCUDrPEidqxL2Cv2SmFCVsHWNMDSchXB2bKKZU
# Website to decode token : https://jwt.io/