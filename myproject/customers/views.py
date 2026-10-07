from django.shortcuts import render
from django.template.loader import render_to_string
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login
from .forms import RegistrationForm, LoginForm
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from customers.forms import EnquiryForm
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from properties.models import Property, Enquiry, Payment,SavedProperty, Booking,VisitSchedule,SiteVisit
    
from customers.models import SupportTicket, Notification
from django.contrib.auth.hashers import make_password,check_password
from django.utils import timezone
from django.core.mail import send_mail
import random
from datetime import timedelta
 




# Create your views here.

User = get_user_model()

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.role = 'customer'
            user.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'redirect_url': reverse('login'),
                })
            messages.success(request, 'Account created successfully! Please login.')
            return redirect('login')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                errors = [
                    str(error)
                    for field_errors in form.errors.values()
                    for error in field_errors
                ]
                return JsonResponse({
                    'success': False,
                    'errors': errors,
                }, status=400)
    else:
        form = RegistrationForm()
    return render(request, 'customers/register.html', {'form': form})

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        identifier = request.POST.get('username_or_mobile')
        password = request.POST.get('password')
        login_role = request.POST.get('login_role') # Frontend se aaya role ('customer', 'agent', 'admin')
        
        user_obj = None
        if identifier:
            # 1. Email se check karein
            if '@' in identifier:
                try:
                    user_obj = User.objects.get(email=identifier)
                except User.DoesNotExist:
                    pass
            
            # 2. Mobile number se check karein
            if user_obj is None:
                try:
                    user_obj = User.objects.get(mobile_number=identifier)
                except User.DoesNotExist:
                    pass

        user = None
        if user_obj is not None:
            username_field = user_obj.USERNAME_FIELD
            user = authenticate(request, **{username_field: getattr(user_obj, username_field), 'password': password})

        if user is not None:
            # --- STRICT ROLE VALIDATION CHECK ---
            db_role = getattr(user, 'role', 'customer') # User ka database wala role
            
            # Agar Admin portal se login kar rahe hain
            if login_role == 'admin':
                if not (user.is_superuser or user.is_staff or db_role == 'admin'):
                    messages.error(request, 'Access Denied: You are not authorized as an Admin.')
                    return redirect('login')
            
            # Agar Agent portal se login kar rahe hain
            elif login_role == 'agent':
                if db_role != 'agent' and not user.is_superuser:
                    messages.error(request, 'Access Denied: This is not an Agent account.')
                    return redirect('login')
            
            # Agar Customer portal se login kar rahe hain
            elif login_role == 'customer':
                if db_role == 'admin' or db_role == 'agent':
                    messages.error(request, 'Please use the Admin or Agent portal to login.')
                    return redirect('login')

            # Sabhi checks pass hone par hi login hoga
            # login(request, user)
            # messages.success(request, 'Login Successfully!')



            # ==========================================
            # YAHAN request.session LAGANA HAI
            # ==========================================

            if login_role == 'admin':
                request.session['admin_user_id'] = user.pk

            elif login_role == 'agent':
                request.session['agent_user_id'] = user.pk

            elif login_role == 'customer':
                request.session['customer_user_id'] = user.pk

            # Currently active role for website header
            request.session['active_role'] = login_role

            messages.success(request, 'Login Successfully!')


            
            # --- Redirection ---
            if user.is_superuser or user.is_staff or db_role == 'admin':
                return redirect('/dashboard/')
            elif db_role == 'agent':
                return redirect('agent_dashboard') # Ya agent dashboard URL agar hai
            else:
                return redirect('customer_dashboard')
        else:
            messages.error(request, 'Invalid email/mobile or password.')
            return redirect('login')
            
    else:
        form = LoginForm()
    return render(request, 'customers/login.html', {'form': form})

#Forgot Password 

# def forgot_password_view(request):
#     if request.method == 'POST':
#         identifier = request.POST.get('username_or_mobile')
#         new_password = request.POST.get('new_password')
        
#         try:
#             # Check karein ki user email ya mobile se exist karta hai ya nahi
#             if '@' in identifier:
#                 user = User.objects.get(email=identifier)
#             else:
#                 user = User.objects.get(mobile_number=identifier)
            
#             # Naya password set kar dein
#             user.set_password(new_password)
#             user.save()
#             messages.success(request, 'Password reset successfully! Please login with your new password.')
#             return redirect('login')
            
#         except User.DoesNotExist:
#             messages.error(request, 'Email or Mobile number not found.')
            
#     return render(request, 'customers/forgot_password.html')



def forgot_password_view(request):
    if request.method == 'POST':
        identifier = request.POST.get('username_or_mobile', '').strip()

        if not identifier:
            messages.error(request, 'Please enter your email or mobile number.')
            return redirect('forgot_password')

        try:
            # Email se user find
            if '@' in identifier:
                user = User.objects.get(email__iexact=identifier)

            # Mobile se user find
            else:
                user = User.objects.get(mobile_number=identifier)

        except User.DoesNotExist:
            messages.error(
                request,
                'No account found with this email or mobile number.'
            )
            return redirect('forgot_password')

        # 6 digit OTP
        otp = str(random.randint(100000, 999999))

        # OTP ki expiry - 5 minutes
        expiry = timezone.now() + timedelta(minutes=5)

        # OTP ka hash session mein store
        request.session['forgot_password_user_id'] = user.id
        request.session['forgot_password_otp'] = make_password(otp)
        request.session['forgot_password_otp_expiry'] = expiry.isoformat()
        request.session['forgot_password_otp_attempts'] = 0

        request.session.modified = True

        # OTP email
        send_mail(
            subject='Hume Properties - Password Reset OTP',
            message=(
                f'Your password reset OTP is: {otp}\n\n'
                'This OTP is valid for 5 minutes.\n'
                'If you did not request a password reset, please ignore this email.'
            ),
            from_email=None,
            recipient_list=[user.email],
            fail_silently=False,
        )

        messages.success(
            request,
            'OTP has been sent to your registered email address.'
        )

        return redirect('verify_otp')

    return render(
        request,
        'customers/forgot_password.html'
    )


#Add Lead View
def add_lead_view(request):
    if request.method == 'POST':
        form = EnquiryForm(request.POST)
        if form.is_valid():
            enquiry = form.save(commit=False)
            if request.user.is_authenticated:
                enquiry.user = request.user # Logged-in user assign kar rahe hain
            enquiry.save()
            return redirect('admin_dashboard')
    else:
        form = EnquiryForm()
    return render(request, 'dashboard/add_lead.html', {'form': form})

#Add Agent View
# def add_agent_view(request):
#     from properties.models import Agent
#     if request.method == 'POST':
#         # Direct form data se Agent create karna (No Form class needed)
#         name = request.POST.get('name')
#         father_name = request.POST.get('father_name')
#         role = request.POST.get('role')
#         experience = request.POST.get('experience')
#         phone = request.POST.get('phone')
#         email = request.POST.get('email')
#         image = request.FILES.get('image')
#         aadhaar_document = request.FILES.get('aadhaar_document')
#         pan_document = request.FILES.get('pan_document')
#         assigned_properties_count = request.POST.get('assigned_properties_count', 0)
        
#         Agent.objects.create(
#             name=name,
#             father_name=father_name,
#             role=role,
#             experience=experience,
#             phone=phone,
#             email=email,
#             image=image,
#             aadhaar_document=aadhaar_document,
#             pan_document=pan_document,
#             assigned_properties_count=assigned_properties_count
#         )
#         messages.success(request, 'Agent added successfully!')
#         return redirect('/dashboard/')
        
#     return render(request, 'dashboard/add_agent.html')

# Add Agent View
def add_agent_view(request):
    from properties.models import Agent

    if request.method == 'POST':
        name = request.POST.get('name')
        father_name = request.POST.get('father_name')
        role = request.POST.get('role')
        experience = request.POST.get('experience')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        password = request.POST.get('password')

        image = request.FILES.get('image')
        aadhaar_document = request.FILES.get('aadhaar_document')
        pan_document = request.FILES.get('pan_document')
        assigned_properties_count = request.POST.get('assigned_properties_count', 0)

        # Agent Login Account Create
        if email and password:

            if User.objects.filter(email=email).exists():
                messages.error(request, 'This email is already registered.')
                return redirect('/dashboard/')

            if User.objects.filter(mobile_number=phone).exists():
                messages.error(request, 'This mobile number is already registered.')
                return redirect('/dashboard/')

            User.objects.create_user(
                email=email,
                full_name=name,
                mobile_number=phone,
                password=password,
                role='agent'
            )

        Agent.objects.create(
            name=name,
            father_name=father_name,
            role=role,
            experience=experience,
            phone=phone,
            email=email,
            image=image,
            aadhaar_document=aadhaar_document,
            pan_document=pan_document,
            assigned_properties_count=assigned_properties_count
        )

        messages.success(request, 'Agent added successfully!')
        return redirect('/dashboard/')

    return render(request, 'dashboard/add_agent.html')

# def edit_agent_view(request, pk):
#     from properties.models import Agent
#     # Database se us agent ko dhundho jiski ID click ki gayi hai
#     agent = get_object_or_404(Agent, pk=pk)
    
#     if request.method == 'POST':
#         # Naye data se purane data ko replace/update karo
#         agent.name = request.POST.get('name')
#         agent.father_name = request.POST.get('father_name')
#         agent.role = request.POST.get('role')
#         agent.experience = request.POST.get('experience')
#         agent.phone = request.POST.get('phone')
#         agent.email = request.POST.get('email')
        
#         if request.FILES.get('image'):
#             agent.image = request.FILES.get('image')

#         if request.FILES.get('aadhaar_document'):
#             agent.aadhaar_document = request.FILES.get('aadhaar_document')

#         if request.FILES.get('pan_document'):
#             agent.pan_document = request.FILES.get('pan_document')
            
#         agent.assigned_properties_count = request.POST.get('assigned_properties_count', 0)
#         agent.save()
        
#         messages.success(request, 'Agent ki details update ho gayi hain!')
#         return redirect('/dashboard/') # Update hone ke baad wapas dashboard par le jao
        
#     return render(request, 'dashboard/edit_agent.html', {'agent': agent})

def edit_agent_view(request, pk):
    from properties.models import Agent

    agent = get_object_or_404(Agent, pk=pk)

    if request.method == 'POST':

        old_email = agent.email

        agent.name = request.POST.get('name')
        agent.father_name = request.POST.get('father_name')
        agent.role = request.POST.get('role')
        agent.experience = request.POST.get('experience')
        agent.phone = request.POST.get('phone')
        agent.email = request.POST.get('email')

        password = request.POST.get('password')

        if request.FILES.get('image'):
            agent.image = request.FILES.get('image')

        if request.FILES.get('aadhaar_document'):
            agent.aadhaar_document = request.FILES.get('aadhaar_document')

        if request.FILES.get('pan_document'):
            agent.pan_document = request.FILES.get('pan_document')

        agent.assigned_properties_count = request.POST.get(
            'assigned_properties_count', 0
        )

        # Existing Agent Login User find/update
        try:
            user_obj = User.objects.get(email=old_email)

            user_obj.email = agent.email
            user_obj.full_name = agent.name
            user_obj.role = 'agent'

            # Password blank hai to old password hi rahega
            if password:
                user_obj.set_password(password)

            user_obj.save()

        except User.DoesNotExist:

            # Agar Agent ka login account nahi hai
            # aur password diya gaya hai to naya account create hoga
            if password:

                if User.objects.filter(email=agent.email).exists():
                    messages.error(request, 'This email is already registered.')
                    return redirect('/dashboard/')

                if User.objects.filter(
                    mobile_number=agent.phone
                ).exists():
                    messages.error(
                        request,
                        'This mobile number is already registered.'
                    )
                    return redirect('/dashboard/')

                User.objects.create_user(
                    email=agent.email,
                    full_name=agent.name,
                    mobile_number=agent.phone,
                    password=password,
                    role='agent'
                )

        # Agent profile save
        agent.save()

        messages.success(
            request,
            'Agent ki details update ho gayi hain!'
        )

        return redirect('/dashboard/')

    return render(
        request,
        'dashboard/edit_agent.html',
        {'agent': agent}
    )

def delete_agent_view(request, pk):
    from properties.models import Agent
    # Agent ko dhundho aur turant delete kar do
    agent = get_object_or_404(Agent, pk=pk)
    agent.delete()
    
    messages.success(request, 'Agent delete ho gaya hai!')
    return redirect('/dashboard/')


#Customer Dashboard View

# @login_required
# def customer_dashboard_view(request):
#     current_user = request.user
    
#     # Is user ki saved properties
#     user_saved = SavedProperty.objects.filter(user=current_user).select_related('property')
#     saved_properties = [item.property for item in user_saved]
    
#     # Is user ki enquiries aur site visits
#     customer_enquiries = Enquiry.objects.filter(user=current_user)
#     upcoming_visits = customer_enquiries
    
#     # Is user ki payments
#     customer_bookings = Booking.objects.filter(user=current_user)
#     customer_payments = Payment.objects.filter(user=current_user)
#     total_paid = sum(p.amount for p in customer_payments if p.status == 'Completed')
#     total_pending = sum(p.amount for p in customer_payments if p.status == 'Pending')
    
#     context = {
#         'customer': current_user,
#         'saved_properties': saved_properties,
#         'saved_properties_count': len(saved_properties),
#         'dash_saved_props': user_saved,
#         'customer_bookings': customer_bookings,
#         'upcoming_visits': upcoming_visits,
#         'site_visits_count': upcoming_visits.count(),
#         'enquiries_count': customer_enquiries.count(),
#         'recent_enquiries': customer_enquiries[:5],
#         'payments': customer_payments,
#         'total_paid': total_paid,
#         'total_pending': total_pending,
#         'bookings_count': customer_bookings.count(),
#         'documents_count': 4,
#     }
    
#     return render(request, 'customers/customer_dashboard.html', context)


@login_required
def customer_dashboard_view(request):
    current_user = request.user

    # -----------------------------
    # SAVED PROPERTIES
    # -----------------------------
    user_saved = SavedProperty.objects.filter(
        user=current_user
    ).select_related('property')

    saved_properties = [item.property for item in user_saved]

    # -----------------------------
    # ENQUIRIES
    # -----------------------------
    customer_enquiries = Enquiry.objects.filter(
        user=current_user
    ).order_by('-created_at')

    # -----------------------------
    # CUSTOMER SITE VISITS
    # -----------------------------
    customer_email = (current_user.email or '').strip().lower()
    customer_phone = (current_user.mobile_number or '').strip()

    # First try customer's email
    site_visit_schedules = VisitSchedule.objects.filter(
        email__iexact=customer_email
    ).select_related(
        'property',
        'agent'
    ).order_by('-created_at')

    # If email record is not found, try mobile number
    if not site_visit_schedules.exists() and customer_phone:
        site_visit_schedules = VisitSchedule.objects.filter(
            phone=customer_phone
        ).select_related(
            'property',
            'agent'
        ).order_by('-created_at')

    # Related SiteVisit records
    site_visit_records = SiteVisit.objects.filter(
        schedule__in=site_visit_schedules
    ).select_related(
        'schedule',
        'schedule__property',
        'schedule__agent'
    ).order_by('-created_at')

    # -----------------------------
    # BOOKINGS
    # -----------------------------
    customer_bookings = Booking.objects.filter(
        user=current_user
    )

    # -----------------------------
    # PAYMENTS
    # -----------------------------
    customer_payments = Payment.objects.filter(
        user=current_user
    )

    total_paid = sum(
        p.amount
        for p in customer_payments
        if p.status == 'Completed'
    )

    total_pending = sum(
        p.amount
        for p in customer_payments
        if p.status == 'Pending'
    )

    # -----------------------------
    # CONTEXT
    # -----------------------------
    context = {
        'customer': current_user,

        # Saved Properties
        'saved_properties': saved_properties,
        'saved_properties_count': len(saved_properties),
        'dash_saved_props': user_saved,

        # Enquiries
        'customer_enquiries': customer_enquiries,
        'enquiries_count': customer_enquiries.count(),
        'recent_enquiries': customer_enquiries[:5],

        # Site Visits
        'upcoming_visits': site_visit_schedules,
        'site_visit_schedules': site_visit_schedules,
        'site_visit_records': site_visit_records,
        'site_visits_count': site_visit_schedules.count(),

        # Bookings
        'customer_bookings': customer_bookings,
        'bookings_count': customer_bookings.count(),

        # Payments
        'payments': customer_payments,
        'total_paid': total_paid,
        'total_pending': total_pending,

        # Other
        'documents_count': 4,
    }

    return render(
        request,
        'customers/customer_dashboard.html',
        context
    )


@login_required
def toggle_save_property(request, property_id):
    property_obj = get_object_or_404(Property, id=property_id)
    
    # Check karein ki pehle se saved hai ya nahi
    saved_item = SavedProperty.objects.filter(user=request.user, property=property_obj)
    
    if saved_item.exists():
        # Agar pehle se saved hai, toh remove kar do (Unsave)
        saved_item.delete()
        messages.info(request, "Property removed from your saved list.")
    else:
        # Agar saved nahi hai, toh save kar do
        SavedProperty.objects.create(user=request.user, property=property_obj)
        messages.success(request, "Property successfully saved to your dashboard!")
        
    # User jahan se aaya tha wapas usi page par bhej do
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
def ajax_all_saved_properties(request):
    saved_items = SavedProperty.objects.filter(user=request.user).select_related('property')
    
    # Aapka jo saved properties wala HTML template hai, use render karna
    html_content = render_to_string('customers/saved_properties.html', {
        'saved_items': saved_items
    }, request=request)
    
    return JsonResponse({'html': html_content})

#Booking Property View
# @login_required
# def book_property(request, property_id):
#     property_obj = get_object_or_404(Property, id=property_id)
    
#     # Bina kisi restriction ke har click par nayi booking request create hogi
#     Booking.objects.create(
#         user=request.user, 
#         property=property_obj, 
#         status='Pending'
#     )
    
#     messages.success(request, "Booking request sent successfully! Status: Pending")
#     return redirect(request.META.get('HTTP_REFERER', 'properties'))


# @login_required
# def book_property(request, property_id):
#     property_obj = get_object_or_404(Property, id=property_id)

#     if request.user.role != 'customer':
#         messages.error(request, "Only customers can book properties.")
#         return redirect(request.META.get('HTTP_REFERER', 'properties'))

#     # Already active booking check
#     active_booking = Booking.objects.filter(
#         property=property_obj,
#         status__in=['Pending', 'Confirmed']
#     ).exists()

#     if active_booking:
#         messages.warning(request, "This property is already booked.")
#         return redirect(request.META.get('HTTP_REFERER', 'properties'))

#     # Create new booking
#     Booking.objects.create(
#         user=request.user,
#         property=property_obj,
#         status='Pending'
#     )

#     messages.success(
#         request,
#         "Property booked successfully! Your booking is pending admin confirmation."
#     )

#     return redirect(request.META.get('HTTP_REFERER', 'properties'))



# @login_required
# def book_property(request, property_id):
#     property_obj = get_object_or_404(Property, id=property_id)

#     # Only customers can book
#     if request.user.role != 'customer':
#         return JsonResponse({
#             'success': False,
#             'message': 'Only customers can book properties.'
#         }, status=403)

#     # Booking sirf POST request se hogi
#     if request.method != 'POST':
#         return JsonResponse({
#             'success': False,
#             'message': 'Invalid request.'
#         }, status=400)

#     # Check if property already has an active booking
#     active_booking = Booking.objects.filter(
#         property=property_obj,
#         status__in=['Pending', 'Confirmed']
#     ).exists()

#     if active_booking:
#         return JsonResponse({
#             'success': False,
#             'message': 'This property is already booked.'
#         }, status=400)

#     # Customer details
#     customer_name = request.POST.get(
#         'customer_name',
#         ''
#     ).strip()

#     mobile_number = request.POST.get(
#         'mobile_number',
#         ''
#     ).strip()

#     is_property_dealer = request.POST.get(
#         'is_property_dealer',
#         ''
#     ).strip()

#     # Validation
#     if not customer_name:
#         return JsonResponse({
#             'success': False,
#             'message': 'Customer name is required.'
#         }, status=400)

#     if not mobile_number:
#         return JsonResponse({
#             'success': False,
#             'message': 'Mobile number is required.'
#         }, status=400)

#     if is_property_dealer not in ['Yes', 'No']:
#         return JsonResponse({
#             'success': False,
#             'message': 'Please select whether you are a property dealer.'
#         }, status=400)

#     # Create booking
#     Booking.objects.create(
#         user=request.user,
#         property=property_obj,
#         customer_name=customer_name,
#         mobile_number=mobile_number,
#         is_property_dealer=is_property_dealer,
#         status='Pending'
#     )

#     return JsonResponse({
#         'success': True,
#         'message': 'Property booked successfully! Your booking is pending admin confirmation.'
#     })


@login_required
def book_property(request, property_id):

    property_obj = get_object_or_404(
        Property,
        id=property_id,
        is_approved=True
    )

    # Only customers can book
    if getattr(request.user, 'role', None) != 'customer':
        return JsonResponse({
            'success': False,
            'message': 'Only customers can book properties.'
        }, status=403)

    # Booking sirf POST request se hogi
    if request.method != 'POST':
        return JsonResponse({
            'success': False,
            'message': 'Invalid request.'
        }, status=400)

    # -------------------------------------------------
    # ONLY CONFIRMED BOOKING PROPERTY KO BOOKED KAREGI
    # -------------------------------------------------
    confirmed_booking = Booking.objects.filter(
        property=property_obj,
        status__in=['Confirmed', 'Completed']
    ).exists()

    if confirmed_booking:
        return JsonResponse({
            'success': False,
            'message': 'This property is already booked.'
        }, status=400)

    # -------------------------------------------------
    # BOOKING FORM DATA
    # -------------------------------------------------
    booking_date = request.POST.get(
        'booking_date',
        ''
    ).strip()

    message = request.POST.get(
        'message',
        ''
    ).strip()

    # -------------------------------------------------
    # CUSTOMER DETAILS
    # Backend profile se liye jayenge
    # -------------------------------------------------
    customer_name = (
        request.user.full_name or ''
    ).strip()

    customer_email = (
        request.user.email or ''
    ).strip()

    mobile_number = (
        request.user.mobile_number or ''
    ).strip()

    # -------------------------------------------------
    # VALIDATION
    # -------------------------------------------------
    if not customer_name:
        return JsonResponse({
            'success': False,
            'message': 'Customer name is not available in your profile.'
        }, status=400)

    if not customer_email:
        return JsonResponse({
            'success': False,
            'message': 'Customer email is not available in your profile.'
        }, status=400)

    if not mobile_number:
        return JsonResponse({
            'success': False,
            'message': 'Customer mobile number is not available in your profile.'
        }, status=400)

    if not booking_date:
        return JsonResponse({
            'success': False,
            'message': 'Booking date is required.'
        }, status=400)

    # -------------------------------------------------
    # CREATE PENDING BOOKING
    # -------------------------------------------------
    Booking.objects.create(
        user=request.user,
        property=property_obj,
        customer_name=customer_name,
        customer_email=customer_email,
        mobile_number=mobile_number,
        booking_date=booking_date,
        message=message,
        status='Pending'
    )

    return JsonResponse({
        'success': True,
        'message': (
            'Booking request submitted successfully! '
            'Your booking is pending admin confirmation.'
        )
    })





# @login_required
# def ajax_my_bookings(request):
#     bookings = Booking.objects.filter(user=request.user)
#     html_content = render_to_string('customers/my_bookings.html', {
#         'bookings': bookings,
#     }, request=request)
#     return JsonResponse({'html': html_content})

@login_required
def ajax_my_bookings(request):
    bookings = Booking.objects.filter(
        user=request.user
    ).select_related('property').order_by('-created_at')

    html_content = render_to_string(
        'customers/my_bookings.html',
        {
            'bookings': bookings,
        },
        request=request
    )

    return JsonResponse({
        'html': html_content
    })

@login_required
def ajax_my_enquiries(request):
    enquiries = Enquiry.objects.filter(user=request.user).order_by('-id')
    
    enquiries_data = []
    for enq in enquiries:
        enquiries_data.append({
            'id': enq.id,
            'property_type': enq.property_type if enq.property_type else 'General Property',
            'phone': enq.phone,
            'message': enq.message,
            #'status': 'Resolved' if enq.is_visited else 'Pending',
            'date': enq.created_at.strftime('%d %b %Y') if enq.created_at else 'Recent',
        })
        
    return JsonResponse({'enquiries': enquiries_data})

# @login_required
# def ajax_my_site_visits(request):
#     visits = Enquiry.objects.filter(
#         user=request.user
#     ).order_by('-id')

#     visits_data = []

#     for visit in visits:
#         visits_data.append({
#             'id': visit.id,
#             'property_type': visit.property_type if visit.property_type else 'Property Visit',
#             'phone': visit.phone,
#             'message': visit.message if visit.message else 'No additional notes',
#             'date': visit.created_at.strftime('%d %b %Y') if visit.created_at else 'Recent',
#             'status': visit.status if visit.status else 'Pending',
#         })

#     return JsonResponse({
#         'visits': visits_data
#     })

@login_required
def ajax_my_site_visits(request):

    # -----------------------------------
    # CURRENT CUSTOMER DETAILS
    # -----------------------------------
    customer_email = (request.user.email or '').strip().lower()
    customer_phone = (request.user.mobile_number or '').strip()

    # -----------------------------------
    # FIND CUSTOMER'S VISIT SCHEDULES
    # -----------------------------------
    schedules = VisitSchedule.objects.filter(
        email__iexact=customer_email
    ).select_related(
        'property',
        'agent'
    ).order_by('-created_at')

    # If email does not find any record,
    # search using mobile number
    if not schedules.exists() and customer_phone:
        schedules = VisitSchedule.objects.filter(
            phone=customer_phone
        ).select_related(
            'property',
            'agent'
        ).order_by('-created_at')

    visits_data = []

    # -----------------------------------
    # PREPARE CUSTOMER SITE VISITS
    # -----------------------------------
    for schedule in schedules:

        # Find SiteVisit submitted by Agent
        site_visit = SiteVisit.objects.filter(
            schedule=schedule
        ).order_by('-created_at').first()

        # -----------------------------------
        # DEFAULT STATUS
        # -----------------------------------
        status = schedule.status

        # -----------------------------------
        # SITE VISIT STATUS
        # -----------------------------------
        if site_visit:

            if site_visit.status == 'Approved':
                status = 'Approved'

            elif site_visit.status == 'Rejected':
                status = 'Rejected'

            else:
                status = 'Under Review'

        # -----------------------------------
        # AGENT DETAILS
        # -----------------------------------
        agent_name = ''
        agent_phone = ''

        if schedule.agent:
            agent_name = schedule.agent.full_name
            agent_phone = schedule.agent.mobile_number

        # -----------------------------------
        # NOTES
        # -----------------------------------
        notes = ''

        if site_visit and site_visit.notes:
            notes = site_visit.notes
        elif schedule.message:
            notes = schedule.message

        # -----------------------------------
        # LOCATION
        # -----------------------------------
        location = ''

        if site_visit and site_visit.location_visited:
            location = site_visit.location_visited
        elif schedule.property:
            location = schedule.property.location or ''

        # -----------------------------------
        # PROPERTY IMAGE
        # -----------------------------------
        property_image = ''

        if schedule.property and schedule.property.image:
            property_image = schedule.property.image.url

        # -----------------------------------
        # SITE VISIT IMAGE
        # -----------------------------------
        visit_image = ''

        if site_visit and site_visit.visit_image:
            visit_image = site_visit.visit_image.url

        # -----------------------------------
        # ADD DATA
        # -----------------------------------
        visits_data.append({

            'id': schedule.id,

            'property_id': (
                schedule.property.id
                if schedule.property
                else None
            ),

            'property_name': (
                schedule.property.title
                if schedule.property
                else 'Property Visit'
            ),

            'property_type': (
                schedule.property.category.name
                if schedule.property and schedule.property.category
                else 'Property Visit'
            ),

            'property_image': property_image,

            'visit_image': visit_image,

            'location': location,

            'phone': schedule.phone,

            'visit_date': (
                schedule.visit_date.strftime(
                    '%d %b %Y, %I:%M %p'
                )
                if schedule.visit_date
                else 'Not Scheduled'
            ),

            'status': status,

            'agent_name': agent_name,

            'agent_phone': agent_phone,

            'notes': notes,

            'site_visit_id': (
                site_visit.id
                if site_visit
                else None
            ),

            'visit_type': (
                site_visit.visit_type
                if site_visit
                else ''
            ),

            'visit_purpose': (
                site_visit.visit_purpose
                if site_visit
                else ''
            ),
        })

    return JsonResponse({
        'visits': visits_data
    })


@login_required
def customer_site_visits_page(request):
    return render(
        request,
        'customers/site_visits.html'
    )

#Customer Support View
def customer_support_view(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        if subject and message:
            SupportTicket.objects.create(
                customer=request.user,
                subject=subject,
                message=message
            )
            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error'}, status=400)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        tickets = SupportTicket.objects.filter(customer=request.user).order_by('-created_at')
        html = render_to_string('customers/customer_support_partial.html', {
            'tickets': tickets
        }, request=request)
        return JsonResponse({'html': html})

#Customer Profile View
@login_required
def customer_profile(request):
    if request.method == 'POST':
        user = request.user
        user.full_name = request.POST.get('full_name', user.full_name)
        user.mobile_number = request.POST.get('mobile_number', user.mobile_number)
        user.office_address = request.POST.get('office_address', user.office_address)
        user.bio = request.POST.get('bio', user.bio)
        
        if 'profile_image' in request.FILES:
            user.profile_image = request.FILES['profile_image']
            
        user.save()
        
        # Agar AJAX request hai, toh save hone ke baad read-only partial view return karein
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            html = render_to_string('customers/customer_profile_partial.html', {'user': request.user}, request=request)
            return HttpResponse(html)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_to_string('customers/customer_profile_partial.html', {'user': request.user}, request=request)
        return HttpResponse(html)
    
    return render(request, 'customers/customer_dashboard.html', {'user': request.user})

# 2. Edit Form View (Dashboard ke andar load hoga)
@login_required
def ajax_customer_profile_edit(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_to_string('customers/customer_profile_edit.html', {'user': request.user}, request=request)
        return HttpResponse(html)
    return render(request, 'customers/customer_dashboard.html', {'user': request.user})

#Customer Change Password
@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user) # Session expire hone se bachane ke liye
            return JsonResponse({'success': True, 'message': 'Password updated successfully!'})
        else:
            # Agar old password galat hai ya match nahi hua, toh error message nikalenge
            error_message = "Please correct the errors below."
            for field, errors in form.errors.items():
                error_message = errors[0]
                break
            return JsonResponse({'success': False, 'message': error_message})
            
    # Agar AJAX request hai toh form ka HTML return karega
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_to_string('customers/customer_password_change.html', {'user': request.user}, request=request)
        return HttpResponse(html)
        
    return render(request, 'customers/customer_dashboard.html', {'user': request.user})

# Notification View
def customer_dashboard(request):
    notifications = list(Notification.objects.filter(user=request.user, is_read=False).order_by('-created_at'))
    
    # Session se hidden/read enquiries ki list nikalain
    hidden_enqs = request.session.get('hidden_enquiries', [])
    enquiries = Enquiry.objects.filter(user=request.user).exclude(id__in=hidden_enqs).order_by('-created_at')[:5]
    
    for enq in enquiries:
        class VirtualNotif:
            def __init__(self, title, message, created_at, id):
                self.title = title
                self.message = message
                self.created_at = created_at
                self.id = f"enq_{id}"
                self.is_read = False
        
        status_text = getattr(enq, 'status', 'Accepted')
        notif_title = f"Property Enquiry ({enq.property_type or 'General'})"
        
        v_notif = VirtualNotif(
            title=notif_title,
            message=(enq.message or 'Property')[:35],
            created_at=getattr(enq, 'created_at', None),
            id=enq.id
        )
        notifications.append(v_notif)

    notifications = sorted(notifications, key=lambda x: x.created_at if getattr(x, 'created_at', None) else '', reverse=True)[:5]
    
    notif_count = Notification.objects.filter(user=request.user, is_read=False).count() + Enquiry.objects.filter(user=request.user).exclude(id__in=hidden_enqs).count()

    context = {
        'notifications': notifications,
        'notif_count': notif_count,
    }
    return render(request, 'customers/dashboard.html', context)


def fetch_customer_notifications_ajax(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.user.is_authenticated:
        notifications = list(Notification.objects.filter(user=request.user, is_read=False).order_by('-created_at'))
        
        hidden_enqs = request.session.get('hidden_enquiries', [])
        enquiries = Enquiry.objects.filter(user=request.user).exclude(id__in=hidden_enqs).order_by('-created_at')[:5]
        
        notif_data = []
        
        for n in notifications:
            notif_data.append({
                'id': str(n.id),
                'title': n.title,
                'message': n.message[:35],
                'created_at': getattr(n, 'created_at', None)
            })
            
        for enq in enquiries:
            notif_data.append({
                'id': f"enq_{enq.id}",
                'title': f"Property Enquiry ({enq.property_type or 'General'})",
                'message': (enq.message or 'Property')[:35],
                'created_at': getattr(enq, 'created_at', None)
            })
            
        notif_data = sorted(notif_data, key=lambda x: x['created_at'] if x['created_at'] else '', reverse=True)[:5]
        
        notif_count = Notification.objects.filter(user=request.user, is_read=False).count() + Enquiry.objects.filter(user=request.user).exclude(id__in=hidden_enqs).count()

        return JsonResponse({
            'notif_count': notif_count,
            'notifications': notif_data
        })
    return JsonResponse({'error': 'Invalid request'}, status=400)


def mark_customer_ajax_read(request):
    if request.method == "POST" and request.user.is_authenticated:
        notif_id = request.POST.get('notif_id')
        
        if str(notif_id).startswith('enq_'):
            enq_id = str(notif_id).replace('enq_', '')
            hidden_enqs = request.session.get('hidden_enquiries', [])
            if enq_id not in hidden_enqs:
                hidden_enqs.append(enq_id)
                request.session['hidden_enquiries'] = hidden_enqs
                request.session.modified = True
            return JsonResponse({'status': 'success'})
            
        try:
            notif = Notification.objects.get(id=notif_id, user=request.user)
            notif.is_read = True
            notif.save()
            return JsonResponse({'status': 'success'})
        except (Notification.DoesNotExist, ValueError):
            return JsonResponse({'status': 'not_found'}, status=404)
            
    return JsonResponse({'status': 'invalid'}, status=400)




@csrf_exempt
def popup_login_view(request):
    if request.method != 'POST':
        return JsonResponse({
            'success': False,
            'message': 'Invalid request.'
        })

    identifier = request.POST.get('username_or_mobile')
    password = request.POST.get('password')

    user_obj = None

    if identifier:
        if '@' in identifier:
            try:
                user_obj = User.objects.get(email=identifier)
            except User.DoesNotExist:
                pass

        if user_obj is None:
            try:
                user_obj = User.objects.get(mobile_number=identifier)
            except User.DoesNotExist:
                pass

    if user_obj is None:
        return JsonResponse({
            'success': False,
            'message': 'Invalid email/mobile or password.'
        })

    user = authenticate(
        request,
        email=user_obj.email,
        password=password
    )

    if user is None:
        return JsonResponse({
            'success': False,
            'message': 'Invalid email/mobile or password.'
        })

    if getattr(user, 'role', 'customer') != 'customer':
        return JsonResponse({
            'success': False,
            'message': 'Please use a Customer account.'
        })

    #login(request, user)
    request.session['customer_user_id'] = user.pk

    request.session['active_role'] = 'customer'

    return JsonResponse({
        'success': True,
        'message': 'Login successful!',

        'customer': {
            'name': user.full_name or '',
            'email': user.email or '',
            'mobile': user.mobile_number or '',
        }
    })



def verify_otp_view(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp', '').strip()

        if not entered_otp:
            messages.error(request, 'Please enter the OTP.')
            return render(request, 'customers/verify_otp.html')

        stored_otp_hash = request.session.get('forgot_password_otp')
        expiry_string = request.session.get('forgot_password_otp_expiry')
        user_id = request.session.get('forgot_password_user_id')

        if not stored_otp_hash or not expiry_string or not user_id:
            messages.error(
                request,
                'OTP session expired. Please request a new OTP.'
            )
            return redirect('forgot_password')

        # OTP expiry check
        try:
            expiry = timezone.datetime.fromisoformat(expiry_string)
        except (ValueError, TypeError):
            messages.error(
                request,
                'Invalid OTP session. Please request a new OTP.'
            )
            return redirect('forgot_password')

        if timezone.now() > expiry:
            messages.error(
                request,
                'OTP has expired. Please request a new OTP.'
            )

            request.session.pop('forgot_password_otp', None)
            request.session.pop('forgot_password_otp_expiry', None)
            request.session.pop('forgot_password_otp_attempts', None)

            return redirect('forgot_password')

        # OTP attempt limit
        attempts = request.session.get(
            'forgot_password_otp_attempts',
            0
        )

        if attempts >= 5:
            messages.error(
                request,
                'Too many incorrect OTP attempts. Please request a new OTP.'
            )

            request.session.pop('forgot_password_otp', None)
            request.session.pop('forgot_password_otp_expiry', None)
            request.session.pop('forgot_password_otp_attempts', None)

            return redirect('forgot_password')

        # OTP verify
        if not check_password(entered_otp, stored_otp_hash):
            request.session['forgot_password_otp_attempts'] = attempts + 1
            request.session.modified = True

            messages.error(
                request,
                'Invalid OTP. Please try again.'
            )

            return render(
                request,
                'customers/verify_otp.html'
            )

        # OTP correct
        request.session['forgot_password_verified'] = True

        return redirect('reset_password')

    return render(
        request,
        'customers/verify_otp.html'
    )


def reset_password_view(request):
    if not request.session.get('forgot_password_verified'):
        messages.error(
            request,
            'Please verify OTP before resetting your password.'
        )
        return redirect('forgot_password')

    user_id = request.session.get('forgot_password_user_id')

    if not user_id:
        messages.error(
            request,
            'Password reset session expired. Please try again.'
        )
        return redirect('forgot_password')

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(
            request,
            'User account not found.'
        )
        return redirect('forgot_password')

    if request.method == 'POST':
        new_password = request.POST.get('new_password', '')
        confirm_password = request.POST.get('confirm_password', '')

        if not new_password:
            messages.error(
                request,
                'Please enter a new password.'
            )
            return render(
                request,
                'customers/reset_password.html'
            )

        if new_password != confirm_password:
            messages.error(
                request,
                'Passwords do not match.'
            )
            return render(
                request,
                'customers/reset_password.html'
            )

        if len(new_password) < 8:
            messages.error(
                request,
                'Password must be at least 8 characters.'
            )
            return render(
                request,
                'customers/reset_password.html'
            )

        user.set_password(new_password)
        user.save()

        # Clear password reset session
        request.session.pop('forgot_password_user_id', None)
        request.session.pop('forgot_password_otp', None)
        request.session.pop('forgot_password_otp_expiry', None)
        request.session.pop('forgot_password_otp_attempts', None)
        request.session.pop('forgot_password_verified', None)

        request.session.modified = True

        messages.success(
            request,
            'Password reset successfully! Please login with your new password.'
        )

        return redirect('login')

    return render(
        request,
        'customers/reset_password.html'
    )



@login_required
def customer_logout_view(request):
    request.session.pop('customer_user_id', None)

    messages.success(request, 'Successfully logged out!')

    return redirect('home')
