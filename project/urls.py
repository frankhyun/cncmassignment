from django.urls import path
from ..auth.views import SignUpView, LoginView, UserDetailsView, UpdateProfileView, DeleteUserView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('user-details/', UserDetailsView.as_view(), name='user-details'),
    path('update-profile/<int:pk>/', UpdateProfileView.as_view(), name='update-profile'),
    path('delete-user/<int:pk>/', DeleteUserView.as_view(), name='delete-user'),
]