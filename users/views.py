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
from django.shortcuts import get_object_or_404, redirect

from django.contrib import messages
from django.db import IntegrityError

from django.contrib.auth import logout
from django.shortcuts import redirect
from .models import Item, CustomShoppingCart, ShoppingCartItem


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
        print("Authenticated user:", user.username)
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
    COUNTRIES = [
        ('AF', 'Afghanistan'), ('AL', 'Albania'), ('DZ', 'Algeria'), ('AS', 'American Samoa'),
        ('AD', 'Andorra'), ('AO', 'Angola'), ('AI', 'Anguilla'), ('AQ', 'Antarctica'),
        ('AG', 'Antigua and Barbuda'), ('AR', 'Argentina'), ('AM', 'Armenia'), ('AW', 'Aruba'),
        ('AU', 'Australia'), ('AT', 'Austria'), ('AZ', 'Azerbaijan'), ('BS', 'Bahamas'),
        ('BH', 'Bahrain'), ('BD', 'Bangladesh'), ('BB', 'Barbados'), ('BY', 'Belarus'),
        ('BE', 'Belgium'), ('BZ', 'Belize'), ('BJ', 'Benin'), ('BM', 'Bermuda'),
        ('BT', 'Bhutan'), ('BO', 'Bolivia'), ('BA', 'Bosnia and Herzegovina'), ('BW', 'Botswana'),
        ('BR', 'Brazil'), ('BN', 'Brunei Darussalam'), ('BG', 'Bulgaria'), ('BF', 'Burkina Faso'),
        ('BI', 'Burundi'), ('KH', 'Cambodia'), ('CM', 'Cameroon'), ('CA', 'Canada'),
        ('CV', 'Cape Verde'), ('KY', 'Cayman Islands'), ('CF', 'Central African Republic'),
        ('TD', 'Chad'), ('CL', 'Chile'), ('CN', 'China'), ('CO', 'Colombia'),
        ('KM', 'Comoros'), ('CG', 'Congo'), ('CD', 'Congo, the Democratic Republic of the'),
        ('CR', 'Costa Rica'), ('CI', 'Côte d\'Ivoire'), ('HR', 'Croatia'), ('CU', 'Cuba'),
        ('CY', 'Cyprus'), ('CZ', 'Czech Republic'), ('DK', 'Denmark'), ('DJ', 'Djibouti'),
        ('DM', 'Dominica'), ('DO', 'Dominican Republic'), ('EC', 'Ecuador'), ('EG', 'Egypt'),
        ('SV', 'El Salvador'), ('GQ', 'Equatorial Guinea'), ('ER', 'Eritrea'), ('EE', 'Estonia'),
        ('SZ', 'Eswatini'), ('ET', 'Ethiopia'), ('FJ', 'Fiji'), ('FI', 'Finland'),
        ('FR', 'France'), ('GA', 'Gabon'), ('GM', 'Gambia'), ('GE', 'Georgia'),
        ('DE', 'Germany'), ('GH', 'Ghana'), ('GR', 'Greece'), ('GD', 'Grenada'),
        ('GT', 'Guatemala'), ('GN', 'Guinea'), ('GW', 'Guinea-Bissau'), ('GY', 'Guyana'),
        ('HT', 'Haiti'), ('HN', 'Honduras'), ('HU', 'Hungary'), ('IS', 'Iceland'),
        ('IN', 'India'), ('ID', 'Indonesia'), ('IR', 'Iran'), ('IQ', 'Iraq'),
        ('IE', 'Ireland'), ('IL', 'Israel'), ('IT', 'Italy'), ('JM', 'Jamaica'),
        ('JP', 'Japan'), ('JO', 'Jordan'), ('KZ', 'Kazakhstan'), ('KE', 'Kenya'),
        ('KI', 'Kiribati'), ('KP', 'Korea, Democratic People\'s Republic of'), ('KR', 'South Korea'),
        ('KW', 'Kuwait'), ('KG', 'Kyrgyzstan'), ('LA', 'Lao People\'s Democratic Republic'),
        ('LV', 'Latvia'), ('LB', 'Lebanon'), ('LS', 'Lesotho'), ('LR', 'Liberia'),
        ('LY', 'Libya'), ('LI', 'Liechtenstein'), ('LT', 'Lithuania'), ('LU', 'Luxembourg'),
        ('MG', 'Madagascar'), ('MW', 'Malawi'), ('MY', 'Malaysia'), ('MV', 'Maldives'),
        ('ML', 'Mali'), ('MT', 'Malta'), ('MH', 'Marshall Islands'), ('MR', 'Mauritania'),
        ('MU', 'Mauritius'), ('MX', 'Mexico'), ('FM', 'Micronesia'), ('MD', 'Moldova'),
        ('MC', 'Monaco'), ('MN', 'Mongolia'), ('ME', 'Montenegro'), ('MA', 'Morocco'),
        ('MZ', 'Mozambique'), ('MM', 'Myanmar'), ('NA', 'Namibia'), ('NR', 'Nauru'),
        ('NP', 'Nepal'), ('NL', 'Netherlands'), ('NZ', 'New Zealand'), ('NI', 'Nicaragua'),
        ('NE', 'Niger'), ('NG', 'Nigeria'), ('NO', 'Norway'), ('OM', 'Oman'),
        ('PK', 'Pakistan'), ('PW', 'Palau'), ('PA', 'Panama'), ('PG', 'Papua New Guinea'),
        ('PY', 'Paraguay'), ('PE', 'Peru'), ('PH', 'Philippines'), ('PL', 'Poland'),
        ('PT', 'Portugal'), ('QA', 'Qatar'), ('RO', 'Romania'), ('RU', 'Russian Federation'),
        ('RW', 'Rwanda'), ('KN', 'Saint Kitts and Nevis'), ('LC', 'Saint Lucia'),
        ('VC', 'Saint Vincent and the Grenadines'), ('WS', 'Samoa'), ('SM', 'San Marino'),
        ('ST', 'Sao Tome and Principe'), ('SA', 'Saudi Arabia'), ('SN', 'Senegal'),
        ('RS', 'Serbia'), ('SC', 'Seychelles'), ('SL', 'Sierra Leone'), ('SG', 'Singapore'),
        ('SK', 'Slovakia'), ('SI', 'Slovenia'), ('SB', 'Solomon Islands'), ('SO', 'Somalia'),
        ('ZA', 'South Africa'), ('SS', 'South Sudan'), ('ES', 'Spain'), ('LK', 'Sri Lanka'),
        ('SD', 'Sudan'), ('SR', 'Suriname'), ('SE', 'Sweden'), ('CH', 'Switzerland'),
        ('SY', 'Syrian Arab Republic'), ('TW', 'Taiwan'), ('TJ', 'Tajikistan'),
        ('TZ', 'Tanzania'), ('TH', 'Thailand'), ('TL', 'Timor-Leste'), ('TG', 'Togo'),
        ('TO', 'Tonga'), ('TT', 'Trinidad and Tobago'), ('TN', 'Tunisia'), ('TR', 'Turkey'),
        ('TM', 'Turkmenistan'), ('UG', 'Uganda'), ('UA', 'Ukraine'), ('AE', 'United Arab Emirates'),
        ('GB', 'United Kingdom'), ('US', 'United States'), ('UY', 'Uruguay'),
        ('UZ', 'Uzbekistan'), ('VU', 'Vanuatu'), ('VE', 'Venezuela'), ('VN', 'Viet Nam'),
        ('YE', 'Yemen'), ('ZM', 'Zambia'), ('ZW', 'Zimbabwe'),
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
        country = request.POST['country']

        if password != retypepassword:
            messages.error(request, "Passwords do not match.")
            return render(request, 'register.html', {'states': US_STATES, 'countries': COUNTRIES})

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
                role=role,
                country=country
            )
            messages.success(request, "Account created successfully!")
            return redirect('login')

        except IntegrityError:
            messages.error(request, "Username already exists. Please choose a different one.")
            return render(request, 'register.html', {'states': US_STATES, 'countries': COUNTRIES})


        except Exception as e:
            messages.error(request, f"Error creating account: {e}")
            return render(request, 'register.html', {'states': US_STATES, 'countries': COUNTRIES})


    return render(request, 'register.html', {'states': US_STATES, 'countries': COUNTRIES})




@login_required
def seller_dashboard(request):
    items = Item.objects.filter(vendor=request.user)
    return render(request, 'seller.html', {'items': items})

def logout_view(request):
    if request.method == 'POST':
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
    COUNTRIES = [
        ('AF', 'Afghanistan'), ('AL', 'Albania'), ('DZ', 'Algeria'), ('AS', 'American Samoa'),
        ('AD', 'Andorra'), ('AO', 'Angola'), ('AI', 'Anguilla'), ('AQ', 'Antarctica'),
        ('AG', 'Antigua and Barbuda'), ('AR', 'Argentina'), ('AM', 'Armenia'), ('AW', 'Aruba'),
        ('AU', 'Australia'), ('AT', 'Austria'), ('AZ', 'Azerbaijan'), ('BS', 'Bahamas'),
        ('BH', 'Bahrain'), ('BD', 'Bangladesh'), ('BB', 'Barbados'), ('BY', 'Belarus'),
        ('BE', 'Belgium'), ('BZ', 'Belize'), ('BJ', 'Benin'), ('BM', 'Bermuda'),
        ('BT', 'Bhutan'), ('BO', 'Bolivia'), ('BA', 'Bosnia and Herzegovina'), ('BW', 'Botswana'),
        ('BR', 'Brazil'), ('BN', 'Brunei Darussalam'), ('BG', 'Bulgaria'), ('BF', 'Burkina Faso'),
        ('BI', 'Burundi'), ('KH', 'Cambodia'), ('CM', 'Cameroon'), ('CA', 'Canada'),
        ('CV', 'Cape Verde'), ('KY', 'Cayman Islands'), ('CF', 'Central African Republic'),
        ('TD', 'Chad'), ('CL', 'Chile'), ('CN', 'China'), ('CO', 'Colombia'),
        ('KM', 'Comoros'), ('CG', 'Congo'), ('CD', 'Congo, the Democratic Republic of the'),
        ('CR', 'Costa Rica'), ('CI', 'Côte d\'Ivoire'), ('HR', 'Croatia'), ('CU', 'Cuba'),
        ('CY', 'Cyprus'), ('CZ', 'Czech Republic'), ('DK', 'Denmark'), ('DJ', 'Djibouti'),
        ('DM', 'Dominica'), ('DO', 'Dominican Republic'), ('EC', 'Ecuador'), ('EG', 'Egypt'),
        ('SV', 'El Salvador'), ('GQ', 'Equatorial Guinea'), ('ER', 'Eritrea'), ('EE', 'Estonia'),
        ('SZ', 'Eswatini'), ('ET', 'Ethiopia'), ('FJ', 'Fiji'), ('FI', 'Finland'),
        ('FR', 'France'), ('GA', 'Gabon'), ('GM', 'Gambia'), ('GE', 'Georgia'),
        ('DE', 'Germany'), ('GH', 'Ghana'), ('GR', 'Greece'), ('GD', 'Grenada'),
        ('GT', 'Guatemala'), ('GN', 'Guinea'), ('GW', 'Guinea-Bissau'), ('GY', 'Guyana'),
        ('HT', 'Haiti'), ('HN', 'Honduras'), ('HU', 'Hungary'), ('IS', 'Iceland'),
        ('IN', 'India'), ('ID', 'Indonesia'), ('IR', 'Iran'), ('IQ', 'Iraq'),
        ('IE', 'Ireland'), ('IL', 'Israel'), ('IT', 'Italy'), ('JM', 'Jamaica'),
        ('JP', 'Japan'), ('JO', 'Jordan'), ('KZ', 'Kazakhstan'), ('KE', 'Kenya'),
        ('KI', 'Kiribati'), ('KP', 'Korea, Democratic People\'s Republic of'), ('KR', 'South Korea'),
        ('KW', 'Kuwait'), ('KG', 'Kyrgyzstan'), ('LA', 'Lao People\'s Democratic Republic'),
        ('LV', 'Latvia'), ('LB', 'Lebanon'), ('LS', 'Lesotho'), ('LR', 'Liberia'),
        ('LY', 'Libya'), ('LI', 'Liechtenstein'), ('LT', 'Lithuania'), ('LU', 'Luxembourg'),
        ('MG', 'Madagascar'), ('MW', 'Malawi'), ('MY', 'Malaysia'), ('MV', 'Maldives'),
        ('ML', 'Mali'), ('MT', 'Malta'), ('MH', 'Marshall Islands'), ('MR', 'Mauritania'),
        ('MU', 'Mauritius'), ('MX', 'Mexico'), ('FM', 'Micronesia'), ('MD', 'Moldova'),
        ('MC', 'Monaco'), ('MN', 'Mongolia'), ('ME', 'Montenegro'), ('MA', 'Morocco'),
        ('MZ', 'Mozambique'), ('MM', 'Myanmar'), ('NA', 'Namibia'), ('NR', 'Nauru'),
        ('NP', 'Nepal'), ('NL', 'Netherlands'), ('NZ', 'New Zealand'), ('NI', 'Nicaragua'),
        ('NE', 'Niger'), ('NG', 'Nigeria'), ('NO', 'Norway'), ('OM', 'Oman'),
        ('PK', 'Pakistan'), ('PW', 'Palau'), ('PA', 'Panama'), ('PG', 'Papua New Guinea'),
        ('PY', 'Paraguay'), ('PE', 'Peru'), ('PH', 'Philippines'), ('PL', 'Poland'),
        ('PT', 'Portugal'), ('QA', 'Qatar'), ('RO', 'Romania'), ('RU', 'Russian Federation'),
        ('RW', 'Rwanda'), ('KN', 'Saint Kitts and Nevis'), ('LC', 'Saint Lucia'),
        ('VC', 'Saint Vincent and the Grenadines'), ('WS', 'Samoa'), ('SM', 'San Marino'),
        ('ST', 'Sao Tome and Principe'), ('SA', 'Saudi Arabia'), ('SN', 'Senegal'),
        ('RS', 'Serbia'), ('SC', 'Seychelles'), ('SL', 'Sierra Leone'), ('SG', 'Singapore'),
        ('SK', 'Slovakia'), ('SI', 'Slovenia'), ('SB', 'Solomon Islands'), ('SO', 'Somalia'),
        ('ZA', 'South Africa'), ('SS', 'South Sudan'), ('ES', 'Spain'), ('LK', 'Sri Lanka'),
        ('SD', 'Sudan'), ('SR', 'Suriname'), ('SE', 'Sweden'), ('CH', 'Switzerland'),
        ('SY', 'Syrian Arab Republic'), ('TW', 'Taiwan'), ('TJ', 'Tajikistan'),
        ('TZ', 'Tanzania'), ('TH', 'Thailand'), ('TL', 'Timor-Leste'), ('TG', 'Togo'),
        ('TO', 'Tonga'), ('TT', 'Trinidad and Tobago'), ('TN', 'Tunisia'), ('TR', 'Turkey'),
        ('TM', 'Turkmenistan'), ('UG', 'Uganda'), ('UA', 'Ukraine'), ('AE', 'United Arab Emirates'),
        ('GB', 'United Kingdom'), ('US', 'United States'), ('UY', 'Uruguay'),
        ('UZ', 'Uzbekistan'), ('VU', 'Vanuatu'), ('VE', 'Venezuela'), ('VN', 'Viet Nam'),
        ('YE', 'Yemen'), ('ZM', 'Zambia'), ('ZW', 'Zimbabwe'),
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
        countries=request.POST['countries']

        user=request.user
        user.credit_card_number=credit_card_number
        user.expiration_date=expiration_date
        user.security_code=security_code
        user.street_address=street_address
        user.city=city
        user.state=state
        user.zip_code=zip_code
        user.countries=countries
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

def seller_update_or_delete(request):
    if request.method == "POST":
        item_id = request.POST.get('item_id')
        action = request.POST.get('action')

        if not item_id:
            return redirect('seller')

        try:
            item = Item.objects.get(item_id=item_id)
        except Item.DoesNotExist:
            return redirect('seller')  

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
    items = Item.objects.all()
    return render(request, 'homepage.html', {'items': items})

#@login_required
#def view_cart(request):
#    return render(request, 'Cart.html')
@login_required
def view_checkout(request):
    return render(request, 'Checkout.html')
@login_required
def view_transactions(request):
    return render(request, 'Transaction.html')


@login_required
def add_to_cart(request):
    if request.method == "POST":
        item_id = request.POST.get('item_id')
        item = get_object_or_404(Item, item_id=item_id)

        # Get or create cart for the current user
        cart, created = CustomShoppingCart.objects.get_or_create(user=request.user)

        # Check if item already exists in the cart
        cart_item, created = ShoppingCartItem.objects.get_or_create(cart=cart, item=item)

        if not created:
            cart_item.quantity += 1
            cart_item.save()

        return redirect('view_cart')
    else:
        return redirect('home')



@login_required
def view_cart(request):
    cart, _ = CustomShoppingCart.objects.get_or_create(user=request.user)

    cart_items = ShoppingCartItem.objects.filter(cart=cart)
    total = 0

    print("The Items in the cart are:")
    for item in cart_items:
        print(f"Item Name: {item.item.name}\tItem Price: {item.item.price}\tQuantity: {item.quantity}\tItem Photo URL: {item.item.item_photo.url}")
        total += item.quantity * item.item.price

    print(f"Cart Price: {total}")

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total_price': total
    })
@login_required
def admin_monitor_users(request):
    if request.user.role != 'Admin':
        return redirect('home')  
    users = User.objects.all() 
    return render(request, 'admin_monitor_users.html', {'users': users})


def admin_monitor_products(request):
    if request.user.role != 'Admin':
        return redirect('home')  
    products = Item.objects.all()  
    return render(request, 'admin_monitor_products.html', {'products': products})


def admin_delete_account(request, user_id):
    if request.user.role != 'Admin':
        return redirect('home')  
    try:
        user = User.objects.get(id=user_id)
        user.delete()  
        messages.success(request, "Account successfully deleted.")
    except User.DoesNotExist:
        messages.error(request, "User not found.")
    return redirect('admin_monitor_users')


@login_required
def view_Terms(request):
    return render(request, 'Terms and Services.html')
    