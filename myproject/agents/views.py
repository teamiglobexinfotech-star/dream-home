from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from properties.models import Property, PropertyImage, Enquiry, SiteVisit, Commission, VisitSchedule
from customers.forms import PropertyForm
from django.http import JsonResponse
#from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.db.models import Count, Q
from customers.models import Notification
from django.db.models.functions import ExtractMonth
from datetime import datetime
from django.utils.dateparse import parse_datetime
from django.utils import timezone
from django.db import transaction


# Create your views here.
@login_required
def agent_dashboard_view(request):
    properties = Property.objects.filter(
        agent=request.user
    ).order_by('-created_at')

    leads_qs = VisitSchedule.objects.filter(
        agent=request.user
    ).order_by('-created_at')

    sitevisit_count = SiteVisit.objects.filter(
        agent=request.user
    ).count()

    notifications = Notification.objects.filter(
        user=request.user,
        is_read=False
    ).order_by('-created_at')

    notification_count = notifications.count()

    upcoming_visits = VisitSchedule.objects.filter(
        agent=request.user
    ).order_by('visit_date')

    recent_notifications = Notification.objects.filter(
        user=request.user
    ).order_by('-created_at')[:3]

    tab_filter = request.GET.get('filter', 'all')

    if tab_filter == 'new':
        leads = leads_qs.filter(status='Assigned')

    elif tab_filter == 'follow_up':
        leads = leads_qs.filter(status='Pending')

    elif tab_filter == 'site_visit':
        leads = leads_qs.filter(
            site_visits__isnull=False
        ).distinct()

    else:
        leads = leads_qs

    total_leads = leads_qs.count()

    visited_count = leads_qs.filter(
        status='Completed'
    ).count()

    pending_visit_count = leads_qs.filter(
        status='Pending'
    ).count()

    current_year = datetime.now().year

    monthly_leads_qs = (
        VisitSchedule.objects.filter(
            agent=request.user,
            created_at__year=current_year
        )
        .annotate(month=ExtractMonth('created_at'))
        .values('month')
        .annotate(total=Count('id'))
        .order_by('month')
    )

    this_year_data = [0] * 12

    for item in monthly_leads_qs:
        month_index = item['month'] - 1
        this_year_data[month_index] = item['total']

    last_year = current_year - 1

    monthly_last_year_qs = (
        VisitSchedule.objects.filter(
            agent=request.user,
            created_at__year=last_year
        )
        .annotate(month=ExtractMonth('created_at'))
        .values('month')
        .annotate(total=Count('id'))
        .order_by('month')
    )

    last_year_data = [0] * 12

    for item in monthly_last_year_qs:
        month_index = item['month'] - 1
        last_year_data[month_index] = item['total']

    context = {
        'assigned_properties_count': properties.count(),
        'new_leads_count': total_leads,
        'properties': properties,
        'sitevisit_count': sitevisit_count,
        'leads': leads_qs[:4],
        'current_filter': tab_filter,

        'notifications': notifications,
        'notification_count': notification_count,
        'upcoming_visits': upcoming_visits,
        'recent_notifications': recent_notifications,

        'this_year_data': this_year_data,
        'last_year_data': last_year_data,

        'new_lead_count': pending_visit_count,
        'contacted_count': visited_count,
        'follow_up_count': leads_qs.filter(
            status='Pending'
        ).count(),

        'site_visit_status_count': sitevisit_count,
        'negotiation_count': 0,
        'converted_count': visited_count,

        'total_leads_count': total_leads,
        'filter_new_count': leads_qs.filter(
            status='Assigned'
        ).count(),

        'filter_follow_up_count': leads_qs.filter(
            status='Pending'
        ).count(),

        'filter_site_visit_count': leads_qs.filter(
            site_visits__isnull=False
        ).distinct().count(),
    }

    return render(
        request,
        'agents/agent_dashboard.html',
        context
    )

#Agent Add Property View
# @login_required
# def agent_add_property_view(request):
#     if request.method == 'POST':
#         form = PropertyForm(request.POST, request.FILES)
#         if form.is_valid():
#             property_obj = form.save(commit=False)
#             property_obj.agent = request.user
#             property_obj.is_approved = False  # Admin approval pending rahega
#             property_obj.save()
            
#             # Agar AJAX request hai toh JSON response dein
#             if request.headers.get('x-requested-with') == 'XMLHttpRequest':
#                 return JsonResponse({
#                     'status': 'success', 
#                     'message': 'Property added successfully! It is pending admin approval.'
#                 })
#             return redirect('agent_properties')
#         else:
#             # Form invalid hone par errors ke sath form wapas render karein
#             if request.headers.get('x-requested-with') == 'XMLHttpRequest':
#                 return render(request, 'agents/add_property.html', {'form': form})
#     else:
#         form = PropertyForm()
    
#     context = {'form': form}
#     if request.headers.get('x-requested-with') == 'XMLHttpRequest':
#         return render(request, 'agents/add_property.html', context)
        
#     return render(request, 'agents/add_property.html', context)


@login_required
def agent_add_property_view(request):

    if request.method == 'POST':

        form = PropertyForm(request.POST, request.FILES)

        # One-by-one selected images
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

                    # Current logged-in agent
                    property_obj.agent = request.user

                    # Admin approval required
                    property_obj.is_approved = False

                    # First selected image = main property image
                    property_obj.image = images[0]

                    property_obj.save()

                    # Save all selected images
                    for image in images[1:]:

                        PropertyImage.objects.create(
                            property=property_obj,
                            image=image
                        )

                # AJAX success response
                if request.headers.get(
                    'x-requested-with'
                ) == 'XMLHttpRequest':

                    return JsonResponse({
                        'status': 'success',
                        'message': (
                            'Property added successfully! '
                            'It is pending admin approval.'
                        )
                    })

                return redirect('agent_properties')

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
                'agents/add_property.html',
                {
                    'form': form
                }
            )

    else:

        form = PropertyForm()

    return render(
        request,
        'agents/add_property.html',
        {
            'form': form
        }
    )




#Agent Properties View
@login_required
def agent_properties_view(request):
    # Sirf logged-in agent ki properties filter hongi
    properties = Property.objects.filter(agent=request.user).order_by('-created_at')
    context = {'properties': properties}
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'agents/my_properties.html', context)
        
    return render(request, 'agents/agent_dashboard.html', context)

#Agent Leads View
@login_required
def agent_leads_view(request):
    print("CURRENT LOGGED-IN USER:", request.user, request.user.id, request.user.role)
    
    schedules = VisitSchedule.objects.filter(
        agent=request.user
    ).order_by('-created_at')

    print("FOUND SCHEDULES COUNT:", schedules.count())
        
    context = {
        'schedules': schedules
    }

    return render(request, 'agents/my_leads.html', context)

#Agent Logout View
@login_required
def agent_logout_view(request):
    #logout(request)
    request.session.pop('agent_user_id', None)
    messages.success(request, 'Successfully logged out!')
    return redirect('home')

#Agents Site Visits Views
# @login_required
# def agent_site_visits_view(request):
#     visits = SiteVisit.objects.filter(agent=request.user).order_by('-created_at')
#     #enquiries = Enquiry.objects.filter(agent=request.user)
#     schedules = VisitSchedule.objects.filter(agent=request.user)
    
#     if request.method == 'POST':
#         schedule_id = request.POST.get('schedule_id')
#         location = request.POST.get('location_visited')
#         image = request.FILES.get('visit_image')
#         notes = request.POST.get('notes')

#         schedule = get_object_or_404(
#             VisitSchedule,
#             id=schedule_id,
#             agent=request.user
#         )

#         SiteVisit.objects.create(
#             agent=request.user,
#             schedule=schedule,
#             location_visited=location,
#             visit_image=image,
#             notes=notes
#         )

#         schedule.status = 'Completed'
#         schedule.save(update_fields=['status'])
        
#         if request.headers.get('x-requested-with') == 'XMLHttpRequest':
#             context = {'visits': visits, 'schedules': schedules}
#             return render(request, 'agents/site_visit_content.html', context)
            
#         return redirect('agent_site_visits')
        
#     context = {'visits': visits, 'schedules': schedules}
    
#     # Agar AJAX request hai toh sirf snippet do, warna poora dashboard layout render karo
#     if request.headers.get('x-requested-with') == 'XMLHttpRequest':
#         return render(request, 'agents/site_visit_content.html', context)
        
#     return render(request, 'agents/agent_dashboard.html', context)


# @login_required
# def agent_site_visits_view(request):
#     visits = SiteVisit.objects.filter(
#         agent=request.user
#     ).order_by('-created_at')

#     schedules = VisitSchedule.objects.filter(
#         agent=request.user
#     ).order_by('visit_date')

#     if request.method == 'POST':
#         schedule_id = request.POST.get('schedule_id')
#         location = request.POST.get('location_visited')
#         image = request.FILES.get('visit_image')
#         notes = request.POST.get('notes')

#         schedule = get_object_or_404(
#             VisitSchedule,
#             id=schedule_id,
#             agent=request.user
#         )

#         # Actual completed site visit create hoga
#         SiteVisit.objects.create(
#             agent=request.user,
#             schedule=schedule,
#             location_visited=location,
#             visit_image=image,
#             notes=notes,
#             visit_date=schedule.visit_date
#         )

#         # Future schedule ko completed mark karo
#         schedule.status = 'Completed'
#         schedule.save(update_fields=['status'])

#         # IMPORTANT:
#         # Database update ke baad fresh data dobara fetch karo
#         visits = SiteVisit.objects.filter(
#             agent=request.user
#         ).order_by('-created_at')

#         schedules = VisitSchedule.objects.filter(
#             agent=request.user
#         ).order_by('visit_date')

#         if request.headers.get('x-requested-with') == 'XMLHttpRequest':
#             context = {
#                 'visits': visits,
#                 'schedules': schedules
#             }

#             return render(
#                 request,
#                 'agents/site_visit_content.html',
#                 context
#             )

#         return redirect('agent_site_visits')

#     context = {
#         'visits': visits,
#         'schedules': schedules
#     }

#     if request.headers.get('x-requested-with') == 'XMLHttpRequest':
#         return render(
#             request,
#             'agents/site_visit_content.html',
#             context
#         )

#     return render(
#         request,
#         'agents/agent_dashboard.html',
#         context
#     )

# @login_required
# def agent_site_visits_view(request):
#     visits = SiteVisit.objects.filter(
#         agent=request.user
#     ).select_related(
#         'schedule',
#         'schedule__property'
#     ).order_by('-created_at')

#     schedules = VisitSchedule.objects.filter(
#         agent=request.user
#     ).select_related(
#         'property'
#     ).order_by('visit_date')

#     # ---------------------------------------------------------
#     # Customer ke previously used/scheduled properties
#     # prepare karna
#     # ---------------------------------------------------------
#     all_schedules = VisitSchedule.objects.filter(
#         agent=request.user
#     ).select_related('property')

#     customer_properties = {}

#     for schedule in all_schedules:

#         if not schedule.property_id:
#             continue

#         customer_key = (
#             schedule.name,
#             schedule.email or '',
#             schedule.phone
#         )

#         if customer_key not in customer_properties:
#             customer_properties[customer_key] = {}

#         customer_properties[customer_key][
#             schedule.property_id
#         ] = schedule.property

#     # Har completed visit ke saath us customer ki properties attach karo
#     for visit in visits:

#         if visit.schedule:

#             customer_key = (
#                 visit.schedule.name,
#                 visit.schedule.email or '',
#                 visit.schedule.phone
#             )

#             visit.available_properties = list(
#                 customer_properties.get(
#                     customer_key,
#                     {}
#                 ).values()
#             )

#         else:
#             visit.available_properties = []

#     # ---------------------------------------------------------
#     # Complete Site Visit Form
#     # ---------------------------------------------------------
#     if request.method == 'POST':

#         schedule_id = request.POST.get('schedule_id')
#         location = request.POST.get('location_visited')
#         image = request.FILES.get('visit_image')
#         notes = request.POST.get('notes')

#         schedule = get_object_or_404(
#             VisitSchedule,
#             id=schedule_id,
#             agent=request.user
#         )

#         # Actual completed site visit create hoga
#         SiteVisit.objects.create(
#             agent=request.user,
#             schedule=schedule,
#             location_visited=location,
#             visit_image=image,
#             notes=notes,
#             visit_date=schedule.visit_date
#         )

#         # Future schedule ko completed mark karo
#         schedule.status = 'Completed'
#         schedule.save(update_fields=['status'])

#         # -----------------------------------------------------
#         # Database update ke baad fresh data fetch
#         # -----------------------------------------------------
#         visits = SiteVisit.objects.filter(
#             agent=request.user
#         ).select_related(
#             'schedule',
#             'schedule__property'
#         ).order_by('-created_at')

#         schedules = VisitSchedule.objects.filter(
#             agent=request.user
#         ).select_related(
#             'property'
#         ).order_by('visit_date')

#         # Fresh customer-property mapping
#         all_schedules = VisitSchedule.objects.filter(
#             agent=request.user
#         ).select_related('property')

#         customer_properties = {}

#         for schedule in all_schedules:

#             if not schedule.property_id:
#                 continue

#             customer_key = (
#                 schedule.name,
#                 schedule.email or '',
#                 schedule.phone
#             )

#             if customer_key not in customer_properties:
#                 customer_properties[customer_key] = {}

#             customer_properties[customer_key][
#                 schedule.property_id
#             ] = schedule.property

#         # Har visit ke saath customer ki properties attach karo
#         for visit in visits:

#             if visit.schedule:

#                 customer_key = (
#                     visit.schedule.name,
#                     visit.schedule.email or '',
#                     visit.schedule.phone
#                 )

#                 visit.available_properties = list(
#                     customer_properties.get(
#                         customer_key,
#                         {}
#                     ).values()
#                 )

#             else:
#                 visit.available_properties = []

#         if request.headers.get('x-requested-with') == 'XMLHttpRequest':

#             context = {
#                 'visits': visits,
#                 'schedules': schedules
#             }

#             return render(
#                 request,
#                 'agents/site_visit_content.html',
#                 context
#             )

#         return redirect('agent_site_visits')

#     # ---------------------------------------------------------
#     # Normal GET request
#     # ---------------------------------------------------------
#     context = {
#         'visits': visits,
#         'schedules': schedules
#     }

#     if request.headers.get('x-requested-with') == 'XMLHttpRequest':

#         return render(
#             request,
#             'agents/site_visit_content.html',
#             context
#         )

#     return render(
#         request,
#         'agents/agent_dashboard.html',
#         context
#     )

@login_required
def agent_site_visits_view(request):
    visits = SiteVisit.objects.filter(
        agent=request.user
    ).select_related(
        'schedule',
        'schedule__property'
    ).order_by('-created_at')

    schedules = VisitSchedule.objects.filter(
        agent=request.user
    ).select_related(
        'property'
    ).order_by('visit_date')


    total_visits_count = visits.count()

    completed_visits_count = visits.count()

    upcoming_visits_count = schedules.filter(
        status__in=['Pending', 'Assigned']
    ).count()

    # ---------------------------------------------------------
    # Logged-in agent ki saari properties
    # ---------------------------------------------------------
    agent_properties = list(
        Property.objects.all().order_by('title')
    )

    # ---------------------------------------------------------
    # Customer ke previously used/scheduled properties
    # + agent ki saari properties
    # ---------------------------------------------------------
    def attach_available_properties(visits_queryset):

        all_schedules = VisitSchedule.objects.filter(
            agent=request.user
        ).select_related('property')

        customer_properties = {}

        for schedule in all_schedules:

            if not schedule.property_id:
                continue

            customer_key = (
                schedule.name.strip().lower(),
                (schedule.email or '').strip().lower(),
                schedule.phone.strip()
            )

            if customer_key not in customer_properties:
                customer_properties[customer_key] = {}

            customer_properties[customer_key][
                schedule.property_id
            ] = schedule.property

        # -----------------------------------------------------
        # Har completed visit ke saath properties attach karo
        # -----------------------------------------------------
        for visit in visits_queryset:

            if visit.schedule:

                customer_key = (
                    visit.schedule.name.strip().lower(),
                    (visit.schedule.email or '').strip().lower(),
                    visit.schedule.phone.strip()
                )

                linked_properties = list(
                    customer_properties.get(
                        customer_key,
                        {}
                    ).values()
                )

                # Customer ki linked properties
                # + agent ki saari properties
                property_map = {
                    prop.id: prop
                    for prop in linked_properties
                }

                for prop in agent_properties:
                    property_map[prop.id] = prop

                visit.available_properties = list(
                    property_map.values()
                )

            else:
                # Agar visit kisi schedule se linked nahi hai
                # tab bhi agent ki properties available rahengi
                visit.available_properties = list(
                    agent_properties
                )

        return visits_queryset

    # Initial property data attach
    visits = attach_available_properties(visits)

    # ---------------------------------------------------------
    # Complete Site Visit Form
    # ---------------------------------------------------------
    if request.method == 'POST':

        schedule_id = request.POST.get('schedule_id')
        location = request.POST.get('location_visited')
        image = request.FILES.get('visit_image')
        notes = request.POST.get('notes')

        schedule = get_object_or_404(
            VisitSchedule,
            id=schedule_id,
            agent=request.user
        )

        # Actual completed site visit create hoga
        SiteVisit.objects.create(
            agent=request.user,
            schedule=schedule,
            location_visited=location,
            visit_image=image,
            notes=notes,
            visit_date=schedule.visit_date
        )

        # Future schedule ko completed mark karo
        schedule.status = 'Completed'
        schedule.save(update_fields=['status'])

        # -----------------------------------------------------
        # Database update ke baad fresh data fetch
        # -----------------------------------------------------
        visits = SiteVisit.objects.filter(
            agent=request.user
        ).select_related(
            'schedule',
            'schedule__property'
        ).order_by('-created_at')

        schedules = VisitSchedule.objects.filter(
            agent=request.user
        ).select_related(
            'property'
        ).order_by('visit_date')

        # Fresh property data attach
        visits = attach_available_properties(visits)

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':

            context = {
                'visits': visits,
                'schedules': schedules,
                'total_visits_count': total_visits_count,
                'completed_visits_count': completed_visits_count,
                'upcoming_visits_count': upcoming_visits_count,
            }

            return render(
                request,
                'agents/site_visit_content.html',
                context
            )

        return redirect('agent_site_visits')

    # ---------------------------------------------------------
    # Normal GET request
    # ---------------------------------------------------------
    context = {
        'visits': visits,
        'schedules': schedules
    }

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':

        return render(
            request,
            'agents/site_visit_content.html',
            context
        )

    return render(
        request,
        'agents/agent_dashboard.html',
        context
    )



#Edit Site Visit View
@login_required
def agent_edit_site_visit_view(request, pk):
    visit = get_object_or_404(SiteVisit, pk=pk, agent=request.user)
    schedules = VisitSchedule.objects.filter(agent=request.user)
    
    # Fail-safe check: Header ya query parameter dono se detect karega
    is_ajax = (
        request.headers.get('x-requested-with') == 'XMLHttpRequest' or 
        request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest' or
        request.GET.get('ajax') == 'true'
    )

    if request.method == 'POST':
        visit.schedule_id = request.POST.get('schedule_id')
        visit.location_visited = request.POST.get('location_visited')
        if request.FILES.get('visit_image'):
            visit.visit_image = request.FILES.get('visit_image')
        visit.notes = request.POST.get('notes')
        visit.save()
        
        if is_ajax:
            visits = SiteVisit.objects.filter(agent=request.user).order_by('-created_at')
            return render(request, 'agents/site_visit_content.html', {'visits': visits, 'schedules': schedules})
            
        return redirect('agent_site_visits')
        
    context = {'visit': visit, 'schedules': schedules}
    
    if is_ajax:
        return render(request, 'agents/edit_site_visit.html', context)
        
    return render(request, 'agents/agent_dashboard.html', context)

#Delete Site Visit View
@login_required
def agent_delete_site_visit_view(request, pk):
    visit = get_object_or_404(SiteVisit, pk=pk, agent=request.user)
    
    if request.method == 'POST' or request.headers.get('x-requested-with') == 'XMLHttpRequest':
        visit.delete()
        
        # Delete hone ke baad updated list fetch karke partial return kar dein
        visits = SiteVisit.objects.filter(agent=request.user).order_by('-created_at')
        #enquiries = Enquiry.objects.filter(agent=request.user)
        schedules = VisitSchedule.objects.filter(agent=request.user)
        context = {'visits': visits, 'schedules': schedules}
        return render(request, 'agents/site_visit_content.html', context)
        
    return redirect('agent_site_visits')

#Agent Commission View
@login_required
def agent_commission_view(request):
    commissions = Commission.objects.filter(agent=request.user).order_by('-id')
    
    context = {
        'commissions': commissions
    }
    
    # Agar request AJAX ke through aayi hai, toh sirf snippet/template return karein
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'agents/agent_commission.html', context)

#Profile View for Agents
@login_required
def agent_own_profile_view(request):
    user = request.user
    edit_mode = request.GET.get('edit') == 'true'
    
    # Jab user profile update karne ke baad 'Save' karega
    if request.method == 'POST':
        user.full_name = request.POST.get('full_name')
        user.mobile_number = request.POST.get('mobile_number')
        user.email = request.POST.get('email')
        user.designation = request.POST.get('designation')
        user.office_address = request.POST.get('office_address')
        user.bio = request.POST.get('bio')
        
        if 'profile_image' in request.FILES:
            user.profile_image = request.FILES['profile_image']
            
        user.save()
        # Save hone ke baad wapas read-only profile par bhej denge
        return redirect('agent_own_profile')

    context = {'user_obj': user}
    
    # Sirf AJAX requests ke liye partial HTML return hoga (baaki pages safe rahenge)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if edit_mode:
            return render(request, 'agents/agent_edit_profile.html', context)
        return render(request, 'agents/agent_profile.html', context)
    
    # Agar direct URL open ho toh poora dashboard render hoga
    return render(request, 'agents/agent_dashboard.html', context)

#Change Password View for Agents
class AgentPasswordChangeView(PasswordChangeView):
    template_name = 'agents/change_password.html'
    success_url = reverse_lazy('agent_dashboard')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Password changed successfully!")
        return response


def agent_mark_ajax_read(request):
    if request.method == 'POST' or request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # Sirf logged-in agent ki unread notifications ko read mark karega
        Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        return JsonResponse({'success': True, 'message': 'All notifications marked as read.'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request.'}, status=400)



# Agent Next Site Visit View
# @login_required
# def agent_next_site_visit_view(request, pk):
#     if request.method != 'POST':
#         return JsonResponse({
#             'success': False,
#             'message': 'Invalid request method.'
#         }, status=400)

#     # Current visit sirf logged-in agent ka hi hona chahiye
#     previous_visit = get_object_or_404(
#         SiteVisit,
#         pk=pk,
#         agent=request.user
#     )

#     schedule = previous_visit.schedule

#     if not schedule:
#         return JsonResponse({
#             'success': False,
#             'message': 'This site visit is not linked with a scheduled visit.'
#         }, status=400)

#     location = request.POST.get('location_visited', '').strip()
#     visit_type = request.POST.get('visit_type', '').strip()
#     visit_purpose = request.POST.get('visit_purpose', '').strip()
#     visit_date = request.POST.get('visit_date', '').strip()
#     notes = request.POST.get('notes', '').strip()
#     image = request.FILES.get('visit_image')

#     # Required fields
#     if not location:
#         return JsonResponse({
#             'success': False,
#             'message': 'Please enter the location.'
#         }, status=400)

#     if not visit_type:
#         return JsonResponse({
#             'success': False,
#             'message': 'Please select the visit type.'
#         }, status=400)

#     if not visit_date:
#         return JsonResponse({
#             'success': False,
#             'message': 'Please select the next visit date and time.'
#         }, status=400)

#     if not image:
#         return JsonResponse({
#             'success': False,
#             'message': 'Please upload the visit photo.'
#         }, status=400)

#     # Next actual visit = NEW SiteVisit record
#     SiteVisit.objects.create(
#         agent=request.user,
#         schedule=schedule,
#         previous_visit=previous_visit,
#         location_visited=location,
#         visit_image=image,
#         notes=notes,
#         visit_type=visit_type,
#         visit_purpose=visit_purpose,
#         visit_date=visit_date,
#         status='Pending'
#     )

#     return JsonResponse({
#         'success': True,
#         'message': 'Next visit submitted successfully.'
#     })


@login_required
def agent_next_site_visit_view(request, pk):
    if request.method != 'POST':
        return JsonResponse({
            'success': False,
            'message': 'Invalid request method.'
        }, status=400)

    # Previous completed visit
    previous_visit = get_object_or_404(
        SiteVisit,
        pk=pk,
        agent=request.user
    )

    # Previous visit must have a schedule
    previous_schedule = previous_visit.schedule

    if not previous_schedule:
        return JsonResponse({
            'success': False,
            'message': 'This site visit is not linked with a scheduled visit.'
        }, status=400)

    # Get future visit data
    selected_property_id = request.POST.get('property_id', '').strip()
    visit_type = request.POST.get('visit_type', '').strip()
    visit_date = request.POST.get('visit_date', '').strip()
    visit_purpose = request.POST.get('visit_purpose', '').strip()
    message = request.POST.get('message', '').strip()

    if not selected_property_id:
        return JsonResponse({
            'success': False,
            'message': 'Please select property.'
        }, status=400)

    selected_property = get_object_or_404(
        Property,
        pk=selected_property_id
        
    )

    # Validation
    if not visit_type:
        return JsonResponse({
            'success': False,
            'message': 'Please select visit type.'
        }, status=400)

    if not visit_date:
        return JsonResponse({
            'success': False,
            'message': 'Please select next visit date and time.'
        }, status=400)

    parsed_visit_date = parse_datetime(visit_date)

    if not parsed_visit_date:
        return JsonResponse({
            'success': False,
            'message': 'Invalid visit date and time.'
        }, status=400)
    if timezone.is_naive(parsed_visit_date):
        parsed_visit_date = timezone.make_aware(
            parsed_visit_date,
            timezone.get_current_timezone()
        )

    # Create a NEW future schedule.
    # Do NOT create SiteVisit here.
    next_schedule = VisitSchedule.objects.create(
        property=selected_property,
        name=previous_schedule.name,
        email=previous_schedule.email,
        phone=previous_schedule.phone,
        visit_date=parsed_visit_date,
        message=message or visit_purpose,
        agent=request.user,
        status='Assigned'
    )

    return JsonResponse({
        'success': True,
        'message': 'Next visit scheduled successfully.',
        'schedule_id': next_schedule.id,
        'visit_date': next_schedule.visit_date.strftime('%d %b %Y, %I:%M %p'),
        'visit_type': visit_type
    })


# Agent Edit Property View
@login_required
def agent_edit_property_view(request, pk):

    # Sirf logged-in agent ki aur sirf unapproved property ko edit karne dein
    property_obj = get_object_or_404(
        Property,
        pk=pk,
        agent=request.user,
        is_approved=False
    )

    if request.method == 'POST':

        form = PropertyForm(
            request.POST,
            request.FILES,
            instance=property_obj
        )

        if form.is_valid():

            property_obj = form.save(commit=False)

            # Security: agent/approval status ko form se change nahi hone dena
            property_obj.agent = request.user
            property_obj.is_approved = False
            property_obj.save()

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'success',
                    'message': 'Property updated successfully! It is pending admin approval.'
                })

            return redirect('agent_properties')

    else:
        form = PropertyForm(instance=property_obj)

    context = {
        'form': form,
        'property': property_obj
    }

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(
            request,
            'agents/edit_property.html',
            context
        )

    return render(
        request,
        'agents/edit_property.html',
        context
    )