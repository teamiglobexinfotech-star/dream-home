import re
from django.shortcuts import render,redirect
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.contrib import messages
from properties.models import Property, Category
from customers.models import Notification
from properties.models import Enquiry
from properties.models import Project
from properties.models import Agent
from properties.models import BlogPost, BlogCategory, BlogTag
from properties.forms import ContactForm, VisitScheduleForm
from properties.models import Booking
from properties.models import SavedProperty

# Create your views here.


def home(request):
    # 1. Base Queryset (Saari properties)
    properties_query = Property.objects.filter(is_approved=True).order_by('-created_at')
    # 2. Form se GET Parameters Read Karein
    status = request.GET.get('status')
    location = request.GET.get('location')
    category_id = request.GET.get('category')

    is_searched = False

    # 3. Status Filter (Buy / Rent / Sale)
    if status:
        if status in ['Buy', 'Sale']:
            properties_query = properties_query.filter(status__iexact='Sale')
        elif status == 'Rent':
            properties_query = properties_query.filter(status__iexact='Rent')
        is_searched = True

    # 4. Location Filter (City / Address Search)
    if location:
        properties_query = properties_query.filter(
            Q(location__icontains=location) | Q(city__icontains=location)
        )
        is_searched = True

    # 5. Category Filter
    if category_id:
        properties_query = properties_query.filter(category_id=category_id)
        is_searched = True

    # 6. Display Logic: Search hone par matching properties, varna default Featured
    if is_searched:
        featured_properties = properties_query
    else:
        featured_properties = properties_query.filter(featured=True)[:4]

    categories = Category.objects.all()
    agents = Agent.objects.all()[:4]
    projects = Project.objects.all()[:4]
    blogs = BlogPost.objects.all().order_by('-created_at')[:4]
    form = VisitScheduleForm()

    context = {
        'featured_properties': featured_properties,
        'categories': categories,
        'agents': agents,
        'projects': projects,
        'blogs': blogs,
        'selected_status': status,
        'selected_location': location,
        'selected_category': category_id,
        'is_searched': is_searched,
        'form': form,
        
        
    }

    # Aapka exact template path 'website/home.html'
    return render(request, 'website/home.html', context)


def about(request):
    return render(request, 'website/about.html')

# Helper Function: Text ko Number me badalne ke liye
def parse_price_text(price_str):
    if not price_str:
        return None
    
    price_str = str(price_str).lower().strip()
    
    try:
        # Lakh / Lakhs / Lac conversion
        if 'lakh' in price_str or 'lac' in price_str or 'l' in price_str:
            num = float(re.findall(r"[-+]?\d*\.\d+|\d+", price_str)[0])
            return int(num * 100000)

        # Crore / Cr conversion
        elif 'crore' in price_str or 'cr' in price_str:
            num = float(re.findall(r"[-+]?\d*\.\d+|\d+", price_str)[0])
            return int(num * 10000000)

        # Normal Digits (e.g., 10000000)
        else:
            numbers = re.findall(r"\d+", price_str)
            if numbers:
                return int(numbers[0])
    except Exception:
        return None
    return None


def property_list_view(request):
    properties = Property.objects.filter(is_approved=True)
    all_categories = Category.objects.all()

    # 1. Main Search Bar (Location / Title)
    search_query = request.GET.get('search', '').strip()
    if search_query:
        properties = properties.filter(
            Q(title__icontains=search_query) |
            Q(location__icontains=search_query) |
            Q(city__icontains=search_query)
        )

    # 2. Category Filter (Checkboxes)
    category_ids = request.GET.getlist('category_filter')
    valid_cat_ids = [int(cid) for cid in category_ids if cid.isdigit()]
    if valid_cat_ids:
        properties = properties.filter(category_id__in=valid_cat_ids)

    # 3. Status Filter (Sale / Rent)
    status = request.GET.get('status', 'all').strip()
    if status and status != 'all':
        properties = properties.filter(status__iexact=status)

    # 4. Bedrooms Filter (BHK)
    bedrooms = request.GET.get('bedrooms', '').strip()
    if bedrooms and bedrooms.isdigit():
        properties = properties.filter(bedrooms=int(bedrooms))

    # 5. Price Text Range Parsing
    min_price_raw = request.GET.get('min_price', '').strip()
    max_price_raw = request.GET.get('max_price', '').strip()

    min_val = parse_price_text(min_price_raw)
    max_val = parse_price_text(max_price_raw)

    if min_val is not None:
        properties = properties.filter(price__gte=min_val)

    if max_val is not None:
        properties = properties.filter(price__lte=max_val)


    booked_property_ids = Booking.objects.filter(
        status__in=['Confirmed', 'Completed']
    ).values_list('property_id', flat=True)

    saved_property_ids = []

    if request.user.is_authenticated:
        saved_property_ids = SavedProperty.objects.filter(
            user=request.user
        ).values_list('property_id', flat=True)

    context = {
        'properties': properties,
        'all_categories': all_categories,
        'selected_categories': valid_cat_ids,
        'booked_property_ids': booked_property_ids,
        'saved_property_ids': saved_property_ids,
    }
    return render(request, 'website/properties.html', context)

# --- Enquiry Form Handling ---
def submit_enquiry(request):
    if request.method == "POST":
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        property_type = request.POST.get('property_type')
        property_id = request.POST.get('property_id')
        #visit_date = request.POST.get('visit_date')
        message = request.POST.get('message')

        

        if name and phone:
            # Check karein ki user login hai ya nahi
            current_user = request.user if request.user.is_authenticated else None

            selected_property = None

            if property_id and property_id.isdigit():
                selected_property = Property.objects.filter(
                    id=property_id
                ).first()

        
            Enquiry.objects.create(
                user=current_user,       # Agar login hoga toh user save hoga, warna NULL rahega
                property=selected_property,
                name=name,
                phone=phone,
                email=email,
                property_type=property_type,
                #visit_date=visit_date if visit_date else None,
                message=message
            )

            messages.success(
                request, 
                f"Thank you, {name}! Your enquiry has been submitted successfully. Our team will contact you shortly."
            )
        else:
            messages.error(
                request, 
                "Please fill in all required fields (Name and Phone Number)."
            )

        return redirect('home')

    return redirect('home')


# Projects Page

def projects_view(request):
    ongoing_projects = Project.objects.filter(category='ongoing')
    upcoming_projects = Project.objects.filter(category='upcoming')
    completed_projects = Project.objects.filter(category='completed')

    context = {
        'ongoing_projects': ongoing_projects,
        'upcoming_projects': upcoming_projects,
        'completed_projects': completed_projects,
    }
    return render(request, 'website/projects.html', context)

# Agents Page
def agents_view(request):
    query = request.GET.get('q', '')
    sort_by = request.GET.get('sort', 'newest')

    # 1. Search Filtering
    if query:
        agent_list = Agent.objects.filter(
            Q(name__icontains=query) | Q(role__icontains=query)
            
        ).filter(is_active=True)
    else:
        agent_list = Agent.objects.filter(is_active=True)

    # Convert queryset to list to sort by extracted experience number
    agent_list = list(agent_list)

    def extract_experience(agent):
        # Experience field (jaise "8+ Years" ya "6 Years") me se number nikalna
        match = re.search(r'\d+', agent.experience)
        return int(match.group()) if match else 0

    # 2. Sorting Logic
    if sort_by == 'exp_high':
        # High to Low Experience (Sabse zyada experience wala pehle)
        agent_list.sort(key=extract_experience, reverse=True)
    elif sort_by == 'exp_low':
        # Low to High Experience (Sabse kam experience wala pehle)
        agent_list.sort(key=extract_experience)
    elif sort_by == 'oldest':
        agent_list.sort(key=lambda x: x.id)
    else:  # Default: Newest First
        agent_list.sort(key=lambda x: x.id, reverse=True)
    
    # 3. Pagination
    paginator = Paginator(agent_list, 8) 
    page_number = request.GET.get('page')
    agents = paginator.get_page(page_number)
    
    current_page = agents.number
    per_page = paginator.per_page
    total_agents = paginator.count
    
    if total_agents > 0:
        start_index = (current_page - 1) * per_page + 1
        end_index = min(current_page * per_page, total_agents)
        showing_text = f"Showing {start_index}-{end_index} of {total_agents} Agents"
    else:
        showing_text = "Showing 0 Agents"

    context = {
        'agents': agents,
        'showing_text': showing_text,
        'query': query,
        'sort_by': sort_by,
    }
    return render(request, 'website/agents.html', context)



# Blogs Page 
def blogs_view(request):
    query = request.GET.get('q', '')
    category_slug = request.GET.get('category', '')

    # Base queryset
    blogs_list = BlogPost.objects.all().order_by('-created_at')

    # Search filter
    if query:
        blogs_list = blogs_list.filter(
            Q(title__icontains=query) | Q(excerpt__icontains=query)
        )

    # Category filter
    if category_slug and category_slug != 'All':
        blogs_list = blogs_list.filter(category__name__iexact=category_slug)

    # Pagination
    paginator = Paginator(blogs_list, 9)
    page_number = request.GET.get('page')
    blogs = paginator.get_page(page_number)

    # Sidebar Data
    categories = BlogCategory.objects.annotate(blog_count=Count('blogposts'))
    recent_posts = BlogPost.objects.all().order_by('-created_at')[:4]
    popular_tags = BlogTag.objects.all()

    # Showing text calculation
    current_page = blogs.number
    per_page = paginator.per_page
    total_blogs = paginator.count
    
    if total_blogs > 0:
        start_index = (current_page - 1) * per_page + 1
        end_index = min(current_page * per_page, total_blogs)
        showing_text = f"Showing {start_index}-{end_index} of {total_blogs} Blogs"
    else:
        showing_text = "Showing 0 Blogs"

    context = {
        'blogs': blogs,
        'categories': categories,
        'recent_posts': recent_posts,
        'popular_tags': popular_tags,
        'showing_text': showing_text,
        'query': query,
        'selected_category': category_slug,
    }
    return render(request, 'website/blogs.html', context)

#Contact Us Page
def contact_view(request):

    if request.method == 'POST':

        form = ContactForm(request.POST)

        if form.is_valid():

            Enquiry.objects.create(
                user=request.user if request.user.is_authenticated else None,
                name=form.cleaned_data['full_name'],
                phone=form.cleaned_data['mobile_number'],
                email=form.cleaned_data['email'],
                subject=form.cleaned_data['subject'],
                message=form.cleaned_data['message']
            )

            messages.success(
                request,
                'Your message has been sent successfully!',
                extra_tags='contact'
            )

            return redirect('contact')

    else:

        form = ContactForm()

    return render(
        request,
        'website/contact.html',
        {'form': form}
    )

from django.contrib.auth import get_user_model

# Custom user model ko dynamically fetch karega
User = get_user_model() 



def submit_visit_schedule(request):
    if request.method == "POST":
        form = VisitScheduleForm(request.POST)
        if form.is_valid():
            form.save()
            Notification.objects.create(
                title="New Site Visit",
                message="A new site visit has been scheduled."
            )
            messages.success(request, "Your site visit has been scheduled successfully!")
            return redirect(request.META.get('HTTP_REFERER', 'home'))
    return redirect('home')



from django.http import JsonResponse

def health_check(request):
    return JsonResponse({
        "status": "healthy",
        "message": "Dream Home is running"
    })