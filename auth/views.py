from rest_framework import status, permissions, generics
from rest_framework.response import Response
from auth.models import User, UserDetails
from auth.serializers import UserSerializer, UserDetailsSerializer, UserLoginSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = UserLoginSerializer

class SignUpView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        user = User.objects.filter(email=email).first()
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class UserDetailsView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = UserDetails.objects.all()
    serializer_class = UserDetailsSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    

class UpdateProfileView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserDetailsSerializer

    def get_object(self):
        user = self.request.user
        try:
            return UserDetails.objects.get(user=user)
        except UserDetails.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)  
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class DeleteUserView(APIView):
    permission_classes = [IsAuthenticated]
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

    def delete(self, request):
        request.user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
