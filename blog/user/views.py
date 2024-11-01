from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.views import TemplateView, LoginView
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
# rest_framework_simplejwt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status

# Custom Login view
class CustomLoginView(LoginView):
    form_class = AuthenticationForm
    template_name = 'user/login.html'
    redirect_authenticated_user = True 
    success_url = reverse_lazy('home') 

    def get_success_url(self):
        return self.success_url or self.get_redirect_url() or reverse_lazy('home')
    
# Custom Signup view
class SignupView(CreateView):
    form_class = UserCreationForm
    template_name = 'user/register.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('home')
    
    def get_success_url(self):
        return self.success_url or self.get_redirect_url() or reverse_lazy('home')

# Custom Logout API view for blacklisting the refresh token
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # get the refresh token from the request data
            refresh_token = request.data["refresh"]
            # instantiate a RefreshToken object with the refresh token
            token = RefreshToken(refresh_token)
            # add the token to the blacklist
            token.blacklist()
            return Response({"message": "Logged out successfully"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)