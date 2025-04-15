from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()

from django.contrib import messages
from django.db import IntegrityError
from store.models import Item

from django.contrib.auth import logout
from django.shortcuts import redirect


# Register View
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Customize login response
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = {
            "id": self.user.id,
            "username": self.user.username,
            "email": self.user.email,
            "role": self.user.role,
        }
        return data

class CustomLoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class DeleteAccountView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        logout(request)
        user.delete()
        messages.success(request, "Your account has been deleted.")
        return redirect('homepage')



def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print("what is wrong with you?")
        user = authenticate(request, username=username, password=password)
        print("Username")
        if user is not None:
            login(request, user)
            return redirect('home')  
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    
    return render(request, 'login.html')



def register_view(request):
    US_STATES = [
        ('AL', 'Alabama'), ('AK', 'Alaska'), ('AZ', 'Arizona'), ('AR', 'Arkansas'),
        ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'),
        ('FL', 'Florida'), ('GA', 'Georgia'), ('HI', 'Hawaii'), ('ID', 'Idaho'),
        ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'),
        ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'),
        ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'),
        ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'),
        ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'),
        ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('OH', 'Ohio'), ('OK', 'Oklahoma'),
        ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'),
        ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'),
        ('VT', 'Vermont'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'),
        ('WI', 'Wisconsin'), ('WY', 'Wyoming'),
    ]

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        retypepassword = request.POST['retypepassword']
        name = request.POST['name']
        credit_card_number = request.POST['creditcard']
        expiration_date = request.POST['expirationdate']
        security_code = request.POST['securitycode']
        street_address = request.POST['streetAddress']
        city = request.POST['city']
        state = request.POST['state']
        zip_code = request.POST['zip']

        if password != retypepassword:
            messages.error(request, "Passwords do not match.")
            return render(request, 'register.html', {'states': US_STATES})

        try:
            CustomUser = get_user_model()
            user = CustomUser.objects.create_user(
                username=username,
                password=password,
                first_name=name,
                credit_card_number=credit_card_number,
                expiration_date=expiration_date,
                security_code=security_code,
                street_address=street_address,
                city=city,
                state=state,
                zip_code=zip_code,
            )
            user.save()
            messages.success(request, "Account created successfully!")
            return redirect('login')

        except IntegrityError:
            messages.error(request, "Username already exists. Please choose a different one.")
            return render(request, 'register.html', {'states': US_STATES})

        except Exception as e:
            messages.error(request, f"Error creating account: {e}")
            return render(request, 'register.html', {'states': US_STATES})

    return render(request, 'register.html', {'states': US_STATES})

@login_required
def homepage_view(request):
    return render(request, 'homepage.html')

@login_required
def seller_dashboard(request):
    if request.user.role != 'seller':
        return HttpResponseForbidden("You are not authorized to view this page.")

    items = Item.objects.filter(vendor=request.user)
    return render(request, 'seller_dashboard.html', {'items': items})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return render(request, 'loggedout.html')  # Show confirmation page
    return render(request, 'logout.html')  # Ask for confirmation


def loggedout_view(request):
    return render(request, 'loggedout.html')
