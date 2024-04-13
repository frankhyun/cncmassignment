from django.urls import path
from .views import SignUpView, LoginView, UserDetailsView, UpdateProfileView, DeleteUserView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('user-details/', UserDetailsView.as_view(), name='user_details'),
    path('update-profile/<int:pk>/', UpdateProfileView.as_view(), name='update_profile'),
    path('delete-user/<int:pk>/', DeleteUserView.as_view(), name='delete_user'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name="token_refresh")
]