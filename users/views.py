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
from .models import Item

from django.contrib.auth import logout
from django.shortcuts import redirect
from .models import Item


# Register View
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        print("Authenticated user:", user)
        if user is None:
            return render(request, 'login.html', {'error': 'Invalid username or password'})  
        else:
            login(request, user)
            return redirect('home') 
    
    return render(request, 'login.html')



def delete_account_view(request):
    if request.user.is_authenticated:
        #logout(request)
        request.user.delete()
        messages.success(request, "Account deleted.")
        return redirect('homepage')
    else:
        return redirect('login')





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
        email = request.POST['email']
        role = request.POST['accountType']

        if password != retypepassword:
            messages.error(request, "Passwords do not match.")
            return render(request, 'register.html', {'states': US_STATES})

        try:
            CustomUser = get_user_model()
            CustomUser.objects.create_user(
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
                email=email,
                role=role
            )
            messages.success(request, "Account created successfully!")
            return redirect('login')

        except IntegrityError:
            messages.error(request, "Username already exists. Please choose a different one.")
            return render(request, 'register.html', {'states': US_STATES})

        except Exception as e:
            messages.error(request, f"Error creating account: {e}")
            return render(request, 'register.html', {'states': US_STATES})

    return render(request, 'register.html', {'states': US_STATES})

#@login_required
#def homepage_view(request):
#
#    role=request.user.role
#    print("User role is: ",role)
#    return render(request, 'homepage.html')


@login_required
def seller_dashboard(request):
    #if request.user.role != 'Seller':
    #    seller_items = Item.objects.filter(vendor=request.user)
    #return render(request, 'seller_dashboard.html', {'items': seller_items})
    #return render(request, 'seller.html')
#def seller_view(request):
    items = Item.objects.filter(vendor=request.user)
    return render(request, 'seller.html', {'items': items})

def logout_view(request):
    if request.method == 'POST':
        #print("here")
        #logout(request)
        return render(request, 'loggedout.html')  # Show confirmation page
    return render(request, 'logout.html')  # Ask for confirmation




def loggedout_view(request):
    logout(request)
    return render(request, 'loggedout.html')

@login_required
def update_view(request):
    print("Update.html page vistited")
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

    return render(request, 'update.html',{'states': US_STATES})

@login_required
def update_updatedb(request):
    if request.method == "POST":
        credit_card_number = request.POST['creditcard']
        expiration_date = request.POST['expirationdate']
        security_code = request.POST['securitycode']
        street_address = request.POST['streetAddress']
        city = request.POST['city']
        state = request.POST['state']
        zip_code = request.POST['zip']

        user=request.user
        user.credit_card_number=credit_card_number
        user.expiration_date=expiration_date
        user.security_code=security_code
        user.street_address=street_address
        user.city=city
        user.state=state
        user.zip_code=zip_code
        user.save()   
        messages.success(request, "Account updated successfully!")
    return redirect(request, "homepage.html")


def add_item(request):
    
    if request.method == "POST":
        name = request.POST['itemName']
        description = request.POST['description']
        price = request.POST['price']
        stock = request.POST['quantity']
        item_photo = request.FILES['image']
        item = Item(
            name=name,
            description=description,
            price=price,
            stock=stock,
            vendor=request.user,
            item_photo=item_photo
        )
        item.save()
    return redirect('seller')
#def delete_item(request): 
#    if request.method == "POST":
#        item = Item.objects.get(id=item.item_id)
#        item.delete()    
#    return redirect('seller')


#def seller_update_or_delete(request):
#    if request.method == "POST":
#        action = request.POST.get('action')
#        item_id = request.POST.get('item_id')
#        name = request.POST['itemName']
#        description = request.POST['description']
#        price = request.POST['price']
#        stock = request.POST['quantity']
#        item_photo = request.FILES['image']
#
#        if action == "delete":
#            Item.objects.filter(item_id=item_id).delete()
#
#        elif action == "update":
#            print("I am in update")
#            item = Item.objects.get(item_id=item_id)
#            name = request.POST.get('name')
#            price = request.POST.get('price')
#            # update fields if provided
#            if name: item.name = name
#            if price: item.price = price
#            item.save()
#
#    return redirect('seller')

def seller_update_or_delete(request):
    if request.method == "POST":
        item_id = request.POST.get('item_id')
        action = request.POST.get('action')

        if not item_id:
            return redirect('seller')  # handle missing ID

        try:
            item = Item.objects.get(item_id=item_id)
        except Item.DoesNotExist:
            return redirect('seller')  # handle bad ID

        if action == "delete":
            item.delete()

        elif action == "update":
            name = request.POST.get('name')
            price = request.POST.get('price')
            stock = request.POST.get('stock')
            description = request.POST.get('description')
            image = request.FILES.get('image')

            if name: item.name = name
            if price: item.price = price
            if stock: item.stock = stock
            if description: item.description = description
            if image: item.item_photo = image

            item.save()

    return redirect('seller')


def homepage_view(request):
    items = Item.objects.all()[:3]  # Limit to 3 for featured
    return render(request, 'homepage.html', {'items': items})

