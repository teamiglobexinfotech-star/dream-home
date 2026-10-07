from django.shortcuts import render, redirect, get_object_or_404
from properties.models import Property, PropertyImage, Agent, Enquiry, Project, Payment, BlogPost, SiteVisit, Commission,VisitSchedule
from django.contrib.auth import update_session_auth_hash, login, get_backends
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import JsonResponse
from django.contrib.auth import logout
#from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from customers.models import User,Notification
from django.db.models.functions import ExtractMonth
from django.db.models import Count, Sum
from customers.forms import PropertyForm 
from datetime import timedelta
from django.utils import timezone
from datetime import date
import json
from django.core.serializers.json import DjangoJSONEncoder
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.forms import PasswordChangeForm
# from django.contrib.auth import update_session_auth_hash
# from django.http import JsonResponse
from django.shortcuts import render
from properties.models import Booking
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from properties.forms import ProjectForm,BlogPostForm
from django.db import transaction

User = get_user_model()

@login_required(login_url='login')
def dashboard_view(request):
    # 1. Top Stat Counters (Database se exact count nikalna)
    total_properties = Property.objects.count()
    #available_properties = Property.objects.filter(status='Sale').count()

    completed_booking_property_ids = Booking.objects.filter(
        status='Completed'
    ).values_list('property_id', flat=True)

    available_properties = Property.objects.filter(
        status='Sale'
    ).exclude(
        id__in=completed_booking_property_ids
    ).count()
    
    sold_properties = Booking.objects.filter(status='Completed').count()
    rented_properties = Property.objects.filter(status='Rent').count() 
    
    total_agents = Agent.objects.count()
    total_leads = Enquiry.objects.count()  
    total_enquiries = Enquiry.objects.count()
    total_projects = Project.objects.count()

    # --- TODAY'S ENQUIRIES LOGIC ---
    today = timezone.localdate() # Django ka localdate() exact aaj ki date nikalta hai
    
    todays_enquiries = Enquiry.objects.filter(created_at__date=today).order_by('-created_at')
    todays_enquiries_count = todays_enquiries.count()
    
    # 2. Table & List Data (Latest entries fetch karna)
    latest_properties = Property.objects.all().order_by('-created_at')[:5]
    today_enquiries = Enquiry.objects.all().order_by('-created_at')[:4]

    # --- UPCOMING SITE VISITS LOGIC ---
    now = timezone.now()

    upcoming_visits = VisitSchedule.objects.filter(
        visit_date__gte=now
    ).select_related(
        'property',
        'agent'
    ).order_by('visit_date')[:4]

    # 3. Chart Data: Properties by Type (Donut Chart ke liye)
    property_types_data = list(Property.objects.values('category__name').annotate(count=Count('id')))

    # 4. Chart Data: Sales Overview (Line Chart ke liye)
    # sales_overview = (
    #     Property.objects.annotate(month=ExtractMonth('created_at'))
    #     .values('month')
    #     .annotate(count=Count('id'))
    #     .order_by('month')
    # )
    
    # sales_data = [0] * 12
    # for item in sales_overview:
    #     if item['month']:
    #         month_idx = item['month'] - 1  
    #         if 0 <= month_idx < 12:
    #             sales_data[month_idx] = item['count']

    sales_overview = (
        Booking.objects.filter(status='Completed', booking_date__isnull=False)
        .annotate(month=ExtractMonth('booking_date'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )

    completed_sales_count = Booking.objects.filter(
        status='Completed'
    ).count()

    sales_data = [0] * 12
    for item in sales_overview:
        if item['month']:
            month_idx = item['month'] - 1
            if 0 <= month_idx < 12:
                sales_data[month_idx] = item['count']

    # 5. Lead Conversion Funnel Data
    site_visit_count = VisitSchedule.objects.exclude(status='Cancelled').count()
    active_leads = Enquiry.objects.filter(created_at__gte=timezone.now() - timedelta(days=3)).count()
    processed_leads = Enquiry.objects.filter(status='Replied').count()

    funnel_data = {
        'new_leads': total_leads,
        'contacted': processed_leads if processed_leads > 0 else total_leads,
        'site_visit': site_visit_count,
        'negotiation': 0,
        'converted': Booking.objects.filter(status='Completed').count(),
    }

    # 6. Revenue Overview Chart & Total Revenue Data
    # revenue_overview = (
    #     Property.objects.annotate(month=ExtractMonth('created_at'))
    #     .values('month')
    #     .annotate(total_revenue=Sum('price'))
    #     .order_by('month')
    # )
    
    # revenue_data = [0] * 12
    # for item in revenue_overview:
    #     if item['month']:
    #         month_idx = item['month'] - 1  
    #         if 0 <= month_idx < 12:
    #             revenue_data[month_idx] = float(item['total_revenue'] or 0)

    # # --- SMART REVENUE LOGIC (Testing + Client dono ke liye) ---
    # current_month = timezone.now().month
    # current_year = timezone.now().year
    
    # current_month_revenue = Property.objects.filter(
    #     created_at__month=current_month, 
    #     created_at__year=current_year
    # ).aggregate(total=Sum('price'))['total'] or 0

    # monthly_revenue = current_month_revenue if current_month_revenue > 0 else sum(revenue_data)

    revenue_overview = (
        Payment.objects.filter(status='Completed')
        .annotate(month=ExtractMonth('payment_date'))
        .values('month')
        .annotate(total_revenue=Sum('amount'))
        .order_by('month')
    )

    revenue_data = [0] * 12
    for item in revenue_overview:
        if item['month']:
            month_idx = item['month'] - 1
            if 0 <= month_idx < 12:
                revenue_data[month_idx] = float(item['total_revenue'] or 0)

    current_month = timezone.now().month
    current_year = timezone.now().year

    current_month_revenue = Payment.objects.filter(
        status='Completed',
        payment_date__month=current_month,
        payment_date__year=current_year
    ).aggregate(total=Sum('amount'))['total'] or 0

    monthly_revenue = current_month_revenue

    

    # 7. Recent Activities Data
    recent_activities = []
    
    for prop in latest_properties:
        if prop.created_at:
            recent_activities.append({
                'title': f'New property "{prop.title}" added',
                'time': prop.created_at,
                'user': 'Admin User',
                'icon': 'fa-plus',
                'bg_color': 'blue'
            })
            
    for enq in today_enquiries:
        if enq.created_at:
            recent_activities.append({
                'title': f'New enquiry from {enq.name}',
                'time': enq.created_at,
                'user': enq.name,
                'icon': 'fa-user-plus',
                'bg_color': 'green'
            })

    recent_activities = sorted(recent_activities, key=lambda x: x['time'], reverse=True)[:5]

    context = {
        'total_properties': total_properties,
        'available_properties': available_properties,
        'sold_properties': sold_properties,            
        'rented_properties': rented_properties,
        'total_agents': total_agents,
        'total_leads': total_leads,                      
        'total_enquiries': total_enquiries,
        'total_projects': total_projects,
        'monthly_revenue': monthly_revenue,        
        'revenue_data': revenue_data,                
        'latest_properties': latest_properties,
        'today_enquiries': today_enquiries,
        'property_types_data': property_types_data,
        'sales_data': sales_data,
        'completed_sales_count': completed_sales_count,
        'funnel_data': funnel_data,
        'recent_activities': recent_activities,
        'todays_enquiries': todays_enquiries,            
        'todays_enquiries_count': todays_enquiries_count,
        'upcoming_visits': upcoming_visits,    
    }
    
    return render(request, 'dashboard/admin_dashboard.html', context)

# 1. Add Property View
# def add_property_view(request):
#     if request.method == 'POST':
#         form = PropertyForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             if request.headers.get('x-requested-with') == 'XMLHttpRequest':
#                 properties = Property.objects.all().order_by('-id')
#                 return render(request, 'dashboard/property_list.html', {'properties': properties})
#             return redirect('admin_dashboard')  
#     else:
#         form = PropertyForm()
    
#     if request.headers.get('x-requested-with') == 'XMLHttpRequest':
#         return render(request, 'dashboard/add_property.html', {'form': form})
#     return render(request, 'dashboard/add_property.html', {'form': form})

def add_property_view(request):

    if request.method == 'POST':

        form = PropertyForm(
            request.POST,
            request.FILES
        )

        # Selected property images
        images = request.FILES.getlist('images')

        # Minimum 1 image
        if len(images) < 1:
            form.add_error(
                'images',
                'Please upload at least 1 property image.'
            )

        # Maximum 5 images
        elif len(images) > 5:
            form.add_error(
                'images',
                'You can upload maximum 5 images.'
            )

        # Form + image validation successful
        if form.is_valid() and 1 <= len(images) <= 5:

            try:

                with transaction.atomic():

                    # Property create
                    property_obj = form.save(commit=False)

                    # First image = main property image
                    property_obj.image = images[0]

                    property_obj.save()

                    # Remaining images save
                    for image in images[1:]:

                        PropertyImage.objects.create(
                            property=property_obj,
                            image=image
                        )

                # Existing Admin AJAX response
                if request.headers.get(
                    'x-requested-with'
                ) == 'XMLHttpRequest':

                    properties = Property.objects.all().order_by('-id')

                    return render(
                        request,
                        'dashboard/property_list.html',
                        {
                            'properties': properties
                        }
                    )

                return redirect('admin_dashboard')

            except Exception as e:

                form.add_error(
                    None,
                    f'Unable to save property: {str(e)}'
                )

        # AJAX validation error
        if request.headers.get(
            'x-requested-with'
        ) == 'XMLHttpRequest':

            return render(
                request,
                'dashboard/add_property.html',
                {
                    'form': form
                }
            )

    else:

        form = PropertyForm()

    return render(
        request,
        'dashboard/add_property.html',
        {
            'form': form
        }
    )

# 2. Edit/Update Property View (Fixed using request.POST or Form properly handled)
# def edit_property_view(request, pk):
#     property_item = get_object_or_404(Property, pk=pk)
    
#     if request.method == 'POST':
#         form = PropertyForm(request.POST, request.FILES, instance=property_item)
#         if form.is_valid():
#             form.save()
            
#             if request.headers.get('x-requested-with') == 'XMLHttpRequest':
#                 properties = Property.objects.all().order_by('-id')
#                 return render(request, 'dashboard/property_list.html', {'properties': properties})
                
#             return redirect('admin_dashboard')
#     else:
#         form = PropertyForm(instance=property_item)
        
#     context = {'form': form, 'property': property_item}
    
#     if request.headers.get('x-requested-with') == 'XMLHttpRequest':
#         return render(request, 'dashboard/edit_property.html', context)
        
#     return render(request, 'dashboard/edit_property.html', context)

def edit_property_view(request, pk):

    property_item = get_object_or_404(
        Property,
        pk=pk
    )

    if request.method == 'POST':

        form = PropertyForm(
            request.POST,
            request.FILES,
            instance=property_item
        )

        # -----------------------------------------
        # MAIN IMAGE
        # -----------------------------------------

        new_main_image = request.FILES.get(
            'main_image'
        )

        # -----------------------------------------
        # EXISTING GALLERY IMAGES
        # -----------------------------------------

        retained_image_ids = request.POST.getlist(
            'existing_images'
        )

        valid_existing_ids = set(
            PropertyImage.objects.filter(
                property=property_item,
                id__in=retained_image_ids
            ).values_list(
                'id',
                flat=True
            )
        )

        # -----------------------------------------
        # NEW GALLERY IMAGES
        # -----------------------------------------

        new_images = request.FILES.getlist(
            'images'
        )

        # -----------------------------------------
        # IMAGE VALIDATION
        # -----------------------------------------

        if new_main_image:

            if not new_main_image.content_type.startswith(
                'image/'
            ):

                form.add_error(
                    None,
                    'Please upload a valid main image.'
                )

                new_main_image = None

        for image in new_images:

            if not image.content_type.startswith(
                'image/'
            ):

                form.add_error(
                    None,
                    'Please upload valid image files only.'
                )

                break

        # -----------------------------------------
        # FINAL IMAGE COUNT
        # -----------------------------------------

        main_image_count = 1

        retained_gallery_count = len(
            valid_existing_ids
        )

        new_gallery_count = len(
            new_images
        )

        final_image_count = (
            main_image_count
            + retained_gallery_count
            + new_gallery_count
        )

        # -----------------------------------------
        # MAXIMUM 5 IMAGES
        # -----------------------------------------

        if final_image_count > 5:

            form.add_error(
                None,
                'You can have maximum 5 property images.'
            )

        # -----------------------------------------
        # SAVE
        # -----------------------------------------

        if (
            form.is_valid()
            and 1 <= final_image_count <= 5
        ):

            try:

                with transaction.atomic():

                    # ---------------------------------
                    # SAVE PROPERTY DETAILS
                    # ---------------------------------

                    property_obj = form.save(
                        commit=False
                    )

                    # ---------------------------------
                    # CHANGE MAIN IMAGE
                    # ---------------------------------

                    if new_main_image:

                        property_obj.image = new_main_image

                    else:

                        property_obj.image = property_item.image

                    property_obj.save()

                    # ---------------------------------
                    # REMOVE GALLERY IMAGES
                    # JO ADMIN NE REMOVE KIYE
                    # ---------------------------------

                    PropertyImage.objects.filter(
                        property=property_obj
                    ).exclude(
                        id__in=valid_existing_ids
                    ).delete()

                    # ---------------------------------
                    # NEW GALLERY IMAGES
                    # ---------------------------------

                    for image in new_images:

                        PropertyImage.objects.create(
                            property=property_obj,
                            image=image
                        )

                # ---------------------------------
                # AJAX SUCCESS
                # ---------------------------------

                if request.headers.get(
                    'x-requested-with'
                ) == 'XMLHttpRequest':

                    properties = Property.objects.all().order_by(
                        '-id'
                    )

                    return render(
                        request,
                        'dashboard/property_list.html',
                        {
                            'properties': properties
                        }
                    )

                return redirect(
                    'admin_dashboard'
                )

            except Exception as e:

                form.add_error(
                    None,
                    f'Unable to update property: {str(e)}'
                )

    else:

        form = PropertyForm(
            instance=property_item
        )

    # -----------------------------------------
    # EXISTING GALLERY
    # -----------------------------------------

    existing_images = PropertyImage.objects.filter(
        property=property_item
    ).order_by('id')

    context = {
        'form': form,
        'property': property_item,
        'existing_images': existing_images,
    }

    return render(
        request,
        'dashboard/edit_property.html',
        context
    )

# 3. Delete Property View
def delete_property_view(request, pk):
    property_item = get_object_or_404(Property, pk=pk)
    property_item.delete()
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        properties = Property.objects.all().order_by('-id')
        return render(request, 'dashboard/property_list.html', {'properties': properties})
    return redirect('admin_dashboard')

# 4. View All Activities View
def all_activities_view(request):
    latest_properties = Property.objects.all().order_by('-created_at')
    all_enquiries = Enquiry.objects.all().order_by('-created_at')
    
    all_activities = []
    for prop in latest_properties:
        if prop.created_at:
            all_activities.append({
                'title': f'New property "{prop.title}" added',
                'time': prop.created_at,
                'user': 'Admin User',
                'icon': 'fa-plus',
                'bg_color': 'blue'
            })
            
    for enq in all_enquiries:
        if enq.created_at:
            all_activities.append({
                'title': f'New enquiry from {enq.name}',
                'time': enq.created_at,
                'user': enq.name,
                'icon': 'fa-user-plus',
                'bg_color': 'green'
            })

    all_activities = sorted(all_activities, key=lambda x: x['time'], reverse=True)
    context = {'all_activities': all_activities}
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'dashboard/all_activities.html', context)
    return render(request, 'dashboard/all_activities.html', context)

# 5. Property Management List View
def property_list_view(request):
    properties = Property.objects.all().order_by('-id')
    context = {'properties': properties}
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'dashboard/property_list.html', context)
    return render(request, 'dashboard/property_list.html', context)

def project_list_view(request):
    projects = Project.objects.all().order_by('-id')

    context = {
        'projects': projects
    }

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'dashboard/project_list.html', context)

    return render(request, 'dashboard/project_list.html', context)

def add_project_view(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                projects = Project.objects.all().order_by('-id')
                return render(
                    request,
                    'dashboard/project_list.html',
                    {'projects': projects}
                )

            return redirect('admin_dashboard')

    else:
        form = ProjectForm()

    return render(
        request,
        'dashboard/add_project.html',
        {'form': form}
    )

def edit_project_view(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if request.method == 'POST':
        form = ProjectForm(
            request.POST,
            request.FILES,
            instance=project
        )

        if form.is_valid():
            form.save()

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                projects = Project.objects.all().order_by('-id')

                return render(
                    request,
                    'dashboard/project_list.html',
                    {'projects': projects}
                )

            return redirect('admin_dashboard')

    else:
        form = ProjectForm(instance=project)

    context = {
        'form': form,
        'project': project
    }

    return render(
        request,
        'dashboard/edit_project.html',
        context
    )

def delete_project_view(request, pk):
    project = get_object_or_404(Project, pk=pk)
    project.delete()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        projects = Project.objects.all().order_by('-id')
        return render(
            request,
            'dashboard/project_list.html',
            {'projects': projects}
        )

    return redirect('admin_dashboard')

# 6. Lead Management List View
def lead_list_view(request):
    leads = Enquiry.objects.all().order_by('-created_at')
    #all_agents = User.objects.filter(role='agent')
    context = {'leads': leads}
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'dashboard/lead_list.html', context)
    return render(request, 'dashboard/lead_list.html', context)

# 7. Edit Lead View
def edit_lead_view(request, pk):
    lead_item = get_object_or_404(Enquiry, pk=pk)
    if request.method == 'POST':
        lead_item.name = request.POST.get('name')
        lead_item.email = request.POST.get('email')
        lead_item.phone = request.POST.get('phone')
        lead_item.message = request.POST.get('message')
        lead_item.save()
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            leads = Enquiry.objects.all().order_by('-id')
            #all_agents = User.objects.filter(role='agent')
            return render(request, 'dashboard/lead_list.html', {'leads': leads})
            
        return redirect('lead_list')
        
    context = {'lead': lead_item}
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'dashboard/edit_lead.html', context)
    return render(request, 'dashboard/edit_lead.html', context)

# 8. Delete Lead View
def delete_lead_view(request, pk):
    lead_item = get_object_or_404(Enquiry, pk=pk)
    lead_item.delete()
    
    # Agar request AJAX hai toh dashboard ke andar hi updated lead list bhej do
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        leads = Enquiry.objects.all().order_by('-created_at')
        #all_agents = User.objects.filter(role='agent')
        return render(request, 'dashboard/lead_list.html', {'leads': leads})
        
    return redirect('lead_list')

# 9. Customer Management List View
def customer_list_view(request):
    customers = User.objects.filter(role='customer').order_by('-id')
    context = {'customers': customers}
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'dashboard/customer_list.html', context)
    return render(request, 'dashboard/customer_list.html', context)

# 10. Add Customer View
def add_customer_view(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        mobile_number = request.POST.get('mobile_number')
        password = request.POST.get('password')
        
        User.objects.create_user(
            email=email, 
            full_name=full_name, 
            mobile_number=mobile_number, 
            password=password, 
            role='customer'
        )
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            customers = User.objects.filter(role='customer').order_by('-id')
            return render(request, 'dashboard/customer_list.html', {'customers': customers})
        return redirect('customer_list')
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'dashboard/add_customer.html')
    return render(request, 'dashboard/add_customer.html')

# 11. Edit Customer View
def edit_customer_view(request, pk):
    customer = get_object_or_404(User, pk=pk, role='customer')
    if request.method == 'POST':
        customer.full_name = request.POST.get('full_name')
        customer.email = request.POST.get('email')
        customer.mobile_number = request.POST.get('mobile_number')
        customer.save()
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            customers = User.objects.filter(role='customer').order_by('-id')
            return render(request, 'dashboard/customer_list.html', {'customers': customers})
        return redirect('customer_list')
        
    context = {'customer': customer}
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'dashboard/edit_customer.html', context)
    return render(request, 'dashboard/edit_customer.html', context)

# 12. Delete Customer View
def delete_customer_view(request, pk):
    customer = get_object_or_404(User, pk=pk, role='customer')
    customer.delete()
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        customers = User.objects.filter(role='customer').order_by('-id')
        return render(request, 'dashboard/customer_list.html', {'customers': customers})
    return redirect('customer_list')

# 13. Agent Management List View
def agent_list_view(request):
    agents = Agent.objects.all().order_by('-id')
    context = {'agents': agents}
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'dashboard/agent_list.html', context)
    return render(request, 'dashboard/agent_list.html', context)

# 14. Add Agent View
def add_agent_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        father_name = request.POST.get('father_name')
        role = request.POST.get('role', 'Property Consultant')
        experience = request.POST.get('experience')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        password = request.POST.get('password')
        image = request.FILES.get('image')
        aadhaar_document = request.FILES.get('aadhaar_document')
        pan_document = request.FILES.get('pan_document')

        if email and password:
            if not User.objects.filter(username=email).exists():
                User.objects.create_user(
                    username=email,  # Email ko username banaya gaya hai
                    email=email,
                    password=password,
                    first_name=name,
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
            pan_document=pan_document
        )
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            agents = Agent.objects.all().order_by('-id')
            return render(request, 'dashboard/agent_list.html', {'agents': agents})
        return redirect('agent_list')
        
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'dashboard/add_agent.html')
    return render(request, 'dashboard/add_agent.html')

# 15. Edit Agent View
def edit_agent_view(request, pk):
    agent = get_object_or_404(Agent, pk=pk)
    if request.method == 'POST':
        old_email = agent.email
        agent.name = request.POST.get('name')
        agent.father_name = request.POST.get('father_name')
        agent.role = request.POST.get('role', agent.role)
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
 

        agent.save()

        try:
            user_obj = User.objects.get(username=old_email)
            user_obj.email = agent.email
            user_obj.username = agent.email  # Email ko username banaya hai
            user_obj.first_name = agent.name
            user_obj.role = 'agent'
            if password:  # Agar naya password dala gaya hai tabhi change karein
                user_obj.set_password(password)
            user_obj.save()
        except User.DoesNotExist:
            # Agar user table mein pehle se nahi tha aur password diya hai, toh naya bana dein
            if password:
                User.objects.create_user(
                    username=agent.email,
                    email=agent.email,
                    password=password,
                    first_name=agent.name,
                    role='agent'
                )
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            agents = Agent.objects.all().order_by('-id')
            return render(request, 'dashboard/agent_list.html', {'agents': agents})
        return redirect('agent_list')
        
    context = {'agent': agent}
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'dashboard/edit_agent.html', context)
    return render(request, 'dashboard/edit_agent.html', context)

def toggle_agent_status(request, pk):
    agent = get_object_or_404(Agent, pk=pk)
    agent.is_active = not agent.is_active
    agent.save()

    return redirect('agent_list')

# 16. Delete Agent View
def delete_agent_view(request, pk):
    agent = get_object_or_404(Agent, pk=pk)
    agent.delete()
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        agents = Agent.objects.all().order_by('-id')
        return render(request, 'dashboard/agent_list.html', {'agents': agents})
    return redirect('agent_list')

# Payment Management List View
def payment_list_view(request):
    payments = Payment.objects.all().order_by('-id')
    context = {'payments': payments}
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'dashboard/payment_list.html', context)
    return render(request, 'dashboard/payment_list.html', context)

# Add Payment View
def add_payment_view(request):
    properties = Property.objects.all()
    if request.method == 'POST':
        property_id = request.POST.get('property_id')
        customer_name = request.POST.get('customer_name')
        amount = request.POST.get('amount')
        status = request.POST.get('status')
        transaction_id = request.POST.get('transaction_id')
        
        property_obj = Property.objects.filter(pk=property_id).first() if property_id else None
        
        Payment.objects.create(
            property=property_obj,
            customer_name=customer_name,
            amount=amount,
            status=status,
            transaction_id=transaction_id
        )
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            payments = Payment.objects.all().order_by('-id')
            return render(request, 'dashboard/payment_list.html', {'payments': payments})
        return redirect('payment_list')
        
    context = {'properties': properties}
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'dashboard/add_payment.html', context)
    return render(request, 'dashboard/add_payment.html', context)

# Delete Payment View
def delete_payment_view(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    payment.delete()
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        payments = Payment.objects.all().order_by('-id')
        return render(request, 'dashboard/payment_list.html', {'payments': payments})
    return redirect('payment_list')

def update_payment_status(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    if request.method == 'POST':
        payment.status = request.POST.get('status')
        payment.save()
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        payments = Payment.objects.all().order_by('-id')
        return render(request, 'dashboard/payment_list.html', {'payments': payments})
    return redirect('payment_list')

def edit_payment_view(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    properties = Property.objects.all()
    if request.method == 'POST':
        payment.customer_name = request.POST.get('customer_name')
        property_id = request.POST.get('property_id')
        payment.property = Property.objects.filter(pk=property_id).first() if property_id else None
        payment.amount = request.POST.get('amount')
        payment.transaction_id = request.POST.get('transaction_id')
        payment.status = request.POST.get('status')
        payment.save()
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            payments = Payment.objects.all().order_by('-id')
            return render(request, 'dashboard/payment_list.html', {'payments': payments})
        return redirect('payment_list')
        
    context = {'payment': payment, 'properties': properties}
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'dashboard/edit_payment.html', context)
    return render(request, 'dashboard/edit_payment.html', context)

def reports_analytics_view(request):
    total_properties = Property.objects.count()
    total_enquiries = Enquiry.objects.count() if 'Enquiry' in globals() or 'Enquiry' in locals() else 0
    
    total_payments_count = Payment.objects.count()
    total_revenue = Payment.objects.filter(status='Completed').aggregate(Sum('amount'))['amount__sum'] or 0
    pending_revenue = Payment.objects.filter(status='Pending').aggregate(Sum('amount'))['amount__sum'] or 0

    context = {
        'total_properties': total_properties,
        'total_enquiries': total_enquiries,
        'total_payments_count': total_payments_count,
        'total_revenue': total_revenue,
        'pending_revenue': pending_revenue,
    }
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'dashboard/reports.html', context)
    return render(request, 'dashboard/reports.html', context)

# User Profile View
@login_required(login_url='login')
def profile_view(request, edit=None):
    user = request.user

    if request.method == 'POST':
        user.full_name = request.POST.get('full_name')
        user.email = request.POST.get('email')
        user.mobile_number = request.POST.get('mobile_number')
        user.designation = request.POST.get('designation')
        user.bio = request.POST.get('bio')
        user.office_address = request.POST.get('office_address')
        
        if request.FILES.get('profile_image'):
            user.profile_image = request.FILES.get('profile_image')
            
        user.save()
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return render(request, 'dashboard/profile.html', {'user': user, 'success': True})
        return redirect('admin_profile')

    # Agar URL se edit=true aaya hai ya kwargs mein edit='true' hai
    if request.GET.get('edit') == 'true' or edit == 'true':
        context = {'user': user}
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return render(request, 'dashboard/edit_profile.html', context)
        return render(request, 'dashboard/edit_profile.html', context)

    # Default Normal Profile View (Read-only)
    context = {'user': user}
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'dashboard/profile.html', context)
    return render(request, 'dashboard/profile.html', context)

#Change Password View
# @login_required
# def change_password_view(request):

#     if request.method == 'POST':

#         form = PasswordChangeForm(
#             user=request.user,
#             data=request.POST
#         )

#         if form.is_valid():

#             user = form.save()

#             update_session_auth_hash(request, user)

#             messages.success(
#                 request,
#                 'Password updated successfully!'
#             )

#             form = PasswordChangeForm(
#                 user=request.user
#             )

#         else:

#             messages.error(
#                 request,
#                 'Old password is incorrect or the new passwords do not match.'
#             )

#     else:

#         form = PasswordChangeForm(
#             user=request.user
#         )

#     return render(
#         request,
#         'dashboard/change_password.html',
#         {
#             'form': form
#         }
#     )
@login_required(login_url='login')
def change_password_view(request):

    if request.method == "POST":

        form = PasswordChangeForm(
            user=request.user,
            data=request.POST
        )

        if form.is_valid():

            user = form.save()

            # Keep the user logged in after changing password
            update_session_auth_hash(request, user)

            return JsonResponse({
                "status": "success",
                "message": "Password updated successfully!"
            })

        else:

            errors = []

            for field, field_errors in form.errors.items():
                for error in field_errors:
                    errors.append(error)

            return JsonResponse({
                "status": "error",
                "message": " ".join(errors)
            }, status=400)

    form = PasswordChangeForm(
        user=request.user
    )

    return render(
        request,
        "dashboard/change_password.html",
        {
            "form": form
        }
    )
@login_required
def logout_view(request):
    #logout(request)
    request.session.pop('admin_user_id', None)
    messages.success(request, 'Successfully logged out!')
    return redirect('home')

# Admin Dashboard View
def admin_dashboard(request):
    notifications = Notification.objects.filter(is_read=False).order_by('-created_at')[:5]
    notif_count = Notification.objects.filter(is_read=False).count()

    context = {
        'notifications': notifications,
        'notif_count': notif_count,
    }
    return render(request, 'dashboard/admin_dashboard.html', context)

def fetch_notifications_ajax(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        notifications = Notification.objects.filter(is_read=False).order_by('-created_at')[:5]
        notif_count = Notification.objects.filter(is_read=False).count()

        notif_data = []
        for n in notifications:
            notif_data.append({
                'id': n.id,
                'title': n.title,
                'message': n.message[:35]
            })

        return JsonResponse({
            'notif_count': notif_count,
            'notifications': notif_data
        })
    return JsonResponse({'error': 'Invalid request'}, status=400)

def mark_notification_read(request, pk):
    notification = get_object_or_404(Notification, pk=pk)
    notification.is_read = True
    notification.save()
    return redirect(request.META.get('HTTP_REFERER', 'admin_dashboard'))

def mark_ajax_read(request):
    if request.method == "POST":
        notif_id = request.POST.get('notif_id')
        try:
            notif = Notification.objects.get(id=notif_id)
            notif.is_read = True
            notif.save()
            return JsonResponse({'status': 'success'})
        except Notification.DoesNotExist:
            return JsonResponse({'status': 'not_found'}, status=404)
    return JsonResponse({'status': 'invalid'}, status=400)

#Booking Management View
# @login_required
# def admin_booking_management(request):
#     # Saari bookings fetch karein aur user ki details bhi sath me le aayein
#     all_bookings = Booking.objects.select_related('user').all().order_by('-id')
#     total_bookings_count = all_bookings.count()
    
#     context = {
#         'bookings': all_bookings,
#         'total_bookings': total_bookings_count,
#     }
    
#     return render(request, 'dashboard/admin_booking_management.html', context)

@login_required
def admin_booking_management(request):

    all_bookings = Booking.objects.select_related(
        'user',
        'property',
        'property__category'
    ).all().order_by('-id')

    total_bookings_count = all_bookings.count()

    context = {
        'bookings': all_bookings,
        'total_bookings': total_bookings_count,
    }

    return render(
        request,
        'dashboard/admin_booking_management.html',
        context
    )

@login_required
def update_booking_status(request, booking_id):

    if request.method != 'POST':
        return JsonResponse({
            'success': False,
            'message': 'Invalid request method.'
        }, status=400)

    try:
        booking = Booking.objects.get(id=booking_id)

        new_status = request.POST.get('status')

        allowed_statuses = [
            'Pending',
            'Confirmed',
            'Completed',
            'Cancelled'
        ]

        if new_status not in allowed_statuses:
            return JsonResponse({
                'success': False,
                'message': 'Invalid booking status.'
            }, status=400)

        booking.status = new_status
        booking.save(update_fields=['status'])

        return JsonResponse({
            'success': True,
            'message': 'Booking status updated successfully.',
            'status': booking.status
        })

    except Booking.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Booking not found.'
        }, status=404)

    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'Something went wrong.'
        }, status=500)


@login_required
def delete_booking(request, booking_id):

    if request.method != 'POST':
        return JsonResponse({
            'success': False,
            'message': 'Invalid request method.'
        }, status=400)

    try:
        booking = Booking.objects.get(id=booking_id)

        booking.delete()

        return JsonResponse({
            'success': True,
            'message': 'Booking deleted successfully.'
        })

    except Booking.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Booking not found.'
        }, status=404)

    except Exception as e:
        print("BOOKING DELETE ERROR:", e)

        return JsonResponse({
            'success': False,
            'message': 'Something went wrong.'
        }, status=500)



@staff_member_required
def admin_approve_property(request, pk):
    property_item = get_object_or_404(Property, pk=pk)
    property_item.is_approved = True
    property_item.save()
    return redirect('admin_dashboard')


# 1. Page render karne ke liye view
# def site_visit_approvals_view(request):
#     # Pending visits aur History visits dono fetch karein
#     pending_visits = SiteVisit.objects.filter(status='Pending').order_by('-created_at')
#     history_visits = SiteVisit.objects.exclude(status='Pending').order_by('-created_at')
    
#     context = {
#         'pending_visits': pending_visits,
#         'history_visits': history_visits,
#     }
#     return render(request, 'dashboard/site_visit_approvals.html', context)

def site_visit_approvals_view(request):

    # -----------------------------
    # TODAY
    # -----------------------------
    today = timezone.localdate()


    # =========================================================
    # 1. TOTAL VISITS
    # =========================================================

    total_visit_list = VisitSchedule.objects.select_related(
        'property',
        'agent'
    ).all().order_by('visit_date')

    total_visits = total_visit_list.count()


    # =========================================================
    # 2. COMPLETED VISITS
    # =========================================================

    completed_visit_list = VisitSchedule.objects.select_related(
        'property',
        'agent'
    ).filter(
        status='Completed'
    ).order_by('-visit_date')

    completed_visits = completed_visit_list.count()


    # =========================================================
    # 3. PENDING VISITS
    # Today / Past Date + Assigned
    # =========================================================

    pending_visit_list = VisitSchedule.objects.select_related(
        'property',
        'agent'
    ).filter(
        visit_date__date__lte=today,
        status='Assigned'
    ).order_by('visit_date')

    pending_visits = pending_visit_list.count()


    # =========================================================
    # 4. UPCOMING VISITS
    # Future Date + Assigned
    # =========================================================

    upcoming_visit_list = VisitSchedule.objects.select_related(
        'property',
        'agent'
    ).filter(
        visit_date__date__gt=today,
        status='Assigned'
    ).order_by('visit_date')

    upcoming_visits = upcoming_visit_list.count()


    # =========================================================
    # 5. APPROVED SITE VISITS
    # =========================================================

    approved_visit_list = SiteVisit.objects.filter(
        status='Approved'
    ).order_by('-created_at')

    approved_visits = approved_visit_list.count()


    # =========================================================
    # 6. REJECTED SITE VISITS
    # =========================================================

    rejected_visit_list = SiteVisit.objects.filter(
        status='Rejected'
    ).order_by('-created_at')

    rejected_visits = rejected_visit_list.count()


    # =========================================================
    # 7. PENDING SITE VISIT APPROVAL REQUESTS
    # =========================================================

    pending_site_visits = SiteVisit.objects.filter(
        status='Pending'
    ).order_by('-created_at')

    approval_visits = pending_site_visits.count()


    # =========================================================
    # 8. SITE VISIT HISTORY
    # Approved + Rejected
    # =========================================================

    history_visits = SiteVisit.objects.exclude(
        status='Pending'
    ).order_by('-created_at')


    # =========================================================
    # CONTEXT
    # =========================================================

    context = {

        # -------------------------
        # Total
        # -------------------------
        'total_visit_list': total_visit_list,
        'total_visits': total_visits,


        # -------------------------
        # Completed
        # -------------------------
        'completed_visit_list': completed_visit_list,
        'completed_visits': completed_visits,


        # -------------------------
        # Pending
        # -------------------------
        'pending_visit_list': pending_visit_list,
        'pending_visits': pending_visits,


        # -------------------------
        # Upcoming
        # -------------------------
        'upcoming_visit_list': upcoming_visit_list,
        'upcoming_visits': upcoming_visits,


        # -------------------------
        # Approved
        # -------------------------
        'approved_visit_list': approved_visit_list,
        'approved_visits': approved_visits,


        # -------------------------
        # Rejected
        # -------------------------
        'rejected_visit_list': rejected_visit_list,
        'rejected_visits': rejected_visits,


        # -------------------------
        # Pending Approval
        # -------------------------
        'approval_visits': approval_visits,
        'pending_site_visits': pending_site_visits,


        # -------------------------
        # History
        # -------------------------
        'history_visits': history_visits,
    }


    return render(
        request,
        'dashboard/site_visit_approvals.html',
        context
    )


# 2. AJAX ke through Accept/Reject handle karne ke liye view
def handle_visit_action_ajax(request, pk, action):
    if request.method == 'POST' or request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            visit = SiteVisit.objects.get(pk=pk)
            if action == 'approve':
                visit.status = 'Approved'
            elif action == 'reject':
                visit.status = 'Rejected'
            visit.save()
            return JsonResponse({'success': True, 'message': f'Visit {visit.status} successfully!'})
        except SiteVisit.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Visit not found.'}, status=404)
    return JsonResponse({'success': False, 'message': 'Invalid request.'}, status=400)

# 3. History se record delete karne ke liye view
def delete_site_visit(request, visit_id):
    if request.method == 'POST':
        visit = get_object_or_404(SiteVisit, id=visit_id)
        visit.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'message': 'Invalid request.'}, status=400) 


@staff_member_required
def admin_commission_management(request):
    commissions = Commission.objects.all().order_by('-id')
    agents = User.objects.filter(is_staff=False)

    if request.method == 'POST':
        agent_id = request.POST.get('agent')
        deal_title = request.POST.get('deal_title')
        amount = request.POST.get('amount')
        status = request.POST.get('status', 'Pending')

        if agent_id and deal_title and amount:
            agent_instance = User.objects.get(id=agent_id)
            Commission.objects.create(
                agent=agent_instance,
                deal_title=deal_title,
                amount=amount,
                status=status
            )
            return redirect('admin_commission_management')

    context = {
        'commissions': commissions,
        'agents': agents,
    }
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'dashboard/admin_commission.html', context)
    
    return render(request, 'dashboard/admin_dashboard.html', context)

@staff_member_required
def update_commission_status(request, pk):
    commission = get_object_or_404(Commission, pk=pk)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['Pending', 'Paid']:
            commission.status = new_status
            commission.save()
    return redirect('admin_commission_management')


def visit_schedule_list_view(request):
    schedules = VisitSchedule.objects.select_related(
        'property',
        'agent'
    ).all().order_by('-created_at')

    agents = User.objects.filter(role='agent').order_by('full_name', 'email')

    context = {
        'schedules': schedules,
        'agents': agents,
    }

    return render(
        request,
        'dashboard/visit_schedule_list.html',
        context
    )


@login_required
def assign_schedule_agent(request, schedule_id):
    if request.method != "POST":
        return JsonResponse({
            'success': False,
            'message': 'Invalid request.'
        }, status=400)

    schedule = get_object_or_404(VisitSchedule, id=schedule_id)

    agent_id = request.POST.get('agent_id')

    if not agent_id:
        schedule.agent = None
        schedule.save()
        return JsonResponse({
            'success': True,
            'message': 'Agent unassigned successfully.'
        })

    try:
        agent = User.objects.get(
            id=agent_id,
            role='agent'
        )
    except User.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Agent not found.'
        }, status=404)

    schedule.agent = agent
    schedule.status = 'Assigned'
    schedule.save()

    Notification.objects.create(
        user=agent,
        title='New Site Visit Assigned',
        message=f'A new site visit has been assigned to you for {schedule.visit_date}.'
    )

    return JsonResponse({
        'success': True,
        'message': 'Agent Assigned Successfully!',
        'agent_name': (
            agent.full_name
            if agent.full_name
            else agent.email
        )
    })


@login_required
def update_schedule_date_time(request, schedule_id):

    if request.method != "POST":
        return JsonResponse({
            'success': False,
            'message': 'Invalid request.'
        }, status=400)

    schedule = get_object_or_404(
        VisitSchedule,
        id=schedule_id
    )

    visit_date = request.POST.get('visit_date')
    visit_time = request.POST.get('visit_time')

    if not visit_date or not visit_time:
        return JsonResponse({
            'success': False,
            'message': 'Date and time are required.'
        }, status=400)

    try:
        from datetime import datetime
        from django.utils import timezone

        date_time = datetime.strptime(
            f"{visit_date} {visit_time}",
            "%Y-%m-%d %H:%M"
        )

        if timezone.is_naive(date_time):
            date_time = timezone.make_aware(
                date_time,
                timezone.get_current_timezone()
            )

        schedule.visit_date = date_time
        schedule.save(update_fields=['visit_date'])

        return JsonResponse({
            'success': True,
            'message': 'Visit date and time updated successfully.',
            'date': schedule.visit_date.strftime('%d %b %Y'),
            'time': schedule.visit_date.strftime('%I:%M %p')
        })

    except ValueError:
        return JsonResponse({
            'success': False,
            'message': 'Invalid date or time.'
        }, status=400)


@login_required
def delete_visit_schedule(request, schedule_id):

    if request.method != "POST":
        return JsonResponse({
            'success': False,
            'message': 'Invalid request.'
        }, status=400)

    schedule = get_object_or_404(
        VisitSchedule,
        id=schedule_id
    )

    schedule.delete()

    return JsonResponse({
        'success': True,
        'message': 'Schedule deleted successfully.'
    })



def mark_enquiry_read(request, pk):
    if request.method == "POST":
        try:
            enquiry = Enquiry.objects.get(pk=pk)
            enquiry.status = "Read"
            enquiry.save()

            return JsonResponse({
                "success": True,
                "status": "Read"
            })

        except Enquiry.DoesNotExist:
            return JsonResponse({
                "success": False,
                "message": "Enquiry not found."
            }, status=404)

    return JsonResponse({
        "success": False,
        "message": "Invalid request."
    }, status=400)


def mark_enquiry_replied(request, pk):

    if request.method != "POST":
        return JsonResponse({
            "success": False,
            "message": "Invalid request."
        }, status=400)

    try:
        enquiry = Enquiry.objects.get(pk=pk)

        data = json.loads(request.body or "{}")

        subject = data.get("subject", "").strip()
        message = data.get("message", "").strip()

        if not subject:
            return JsonResponse({
                "success": False,
                "message": "Subject is required."
            }, status=400)

        if not message:
            return JsonResponse({
                "success": False,
                "message": "Reply message is required."
            }, status=400)

        if not enquiry.email:
            return JsonResponse({
                "success": False,
                "message": "Customer email address is missing."
            }, status=400)

        # Send email
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [enquiry.email],
            fail_silently=False,
        )

        # Email successfully sent → Mark as Replied
        enquiry.status = "Replied"
        enquiry.save(update_fields=["status"])

        return JsonResponse({
            "success": True,
            "status": "Replied",
            "message": "Reply sent successfully."
        })

    except Enquiry.DoesNotExist:

        return JsonResponse({
            "success": False,
            "message": "Enquiry not found."
        }, status=404)

    except Exception as e:

        print("Reply Email Error:", e)

        return JsonResponse({
            "success": False,
            "message": "Email could not be sent. Please check email settings."
        }, status=500)





def agent_details_ajax(request, pk):
    agent = get_object_or_404(Agent, pk=pk)

    return JsonResponse({
        'name': agent.name,
        'father_name': agent.father_name,
        'role': agent.role,
        'experience': agent.experience,
        'email': agent.email,
        'phone': agent.phone,
        'is_active': agent.is_active,
        'aadhaar_url': agent.aadhaar_document.url if agent.aadhaar_document else '',
        'pan_url': agent.pan_document.url if agent.pan_document else '',
    })

# Blog Management List View
def blog_list_view(request):
    blogs = BlogPost.objects.select_related(
        'category'
    ).prefetch_related(
        'tags'
    ).all().order_by('-created_at')

    context = {
        'blogs': blogs
    }

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(
            request,
            'dashboard/blog_list.html',
            context
        )

    return render(
        request,
        'dashboard/blog_list.html',
        context
    )

# Add Blog View
def add_blog_view(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                blogs = BlogPost.objects.select_related(
                    'category'
                ).prefetch_related(
                    'tags'
                ).all().order_by('-created_at')

                return render(
                    request,
                    'dashboard/blog_list.html',
                    {'blogs': blogs}
                )

            return redirect('admin_dashboard')

    else:
        form = BlogPostForm()

    return render(
        request,
        'dashboard/add_blog.html',
        {'form': form}
    )

# Edit Blog View
def edit_blog_view(request, pk):
    blog = get_object_or_404(BlogPost, pk=pk)

    if request.method == 'POST':
        form = BlogPostForm(
            request.POST,
            request.FILES,
            instance=blog
        )

        if form.is_valid():
            form.save()

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                blogs = BlogPost.objects.select_related(
                    'category'
                ).prefetch_related(
                    'tags'
                ).all().order_by('-created_at')

                return render(
                    request,
                    'dashboard/blog_list.html',
                    {'blogs': blogs}
                )

            return redirect('admin_dashboard')

    else:
        form = BlogPostForm(instance=blog)

    context = {
        'form': form,
        'blog': blog
    }

    return render(
        request,
        'dashboard/edit_blog.html',
        context
    )

# Delete Blog View
def delete_blog_view(request, pk):
    blog = get_object_or_404(BlogPost, pk=pk)

    blog.delete()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        blogs = BlogPost.objects.select_related(
            'category'
        ).prefetch_related(
            'tags'
        ).all().order_by('-created_at')

        return render(
            request,
            'dashboard/blog_list.html',
            {'blogs': blogs}
        )

    return redirect('admin_dashboard')