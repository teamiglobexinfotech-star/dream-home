from django.db import models
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Property(models.Model):
    PROPERTY_STATUS = (
        ('Sale', 'For Sale'),
        ('Rent', 'For Rent'),
    )
    agent = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='agent_properties',
        limit_choices_to={'role': 'agent'}
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=PROPERTY_STATUS, default='Sale')
    
    # max_length hata diya gaya hai
    price = models.BigIntegerField(
        help_text="Enter price in numbers (e.g. 10000000 for 1 Crore, 5000000 for 50 Lakhs)"
    )
    
    location = models.CharField(max_length=200)
    city = models.CharField(max_length=100, default='Lucknow')
    bedrooms = models.IntegerField(default=0)
    bathrooms = models.IntegerField(default=0)
    area = models.DecimalField(max_digits=8, decimal_places=2)
    featured = models.BooleanField(default=False)
    image = models.ImageField(upload_to='properties/')
    created_at = models.DateTimeField(auto_now_add=True)

    is_approved = models.BooleanField(default=True, help_text="Admin approval required to display publicly")

    def __str__(self):
        return self.title

    # Frontend display ke liye automatic text conversion (1 Crore, 50 Lakh, etc.)
    @property
    def formatted_price(self):
        val = self.price
        if not val:
            return "0"
            
        if val >= 10000000:
            cr = val / 10000000
            return f"{cr:.2f}".rstrip('0').rstrip('.') + " Crore"
        elif val >= 100000:
            lakh = val / 100000
            return f"{lakh:.2f}".rstrip('0').rstrip('.') + " Lakh"
        elif val >= 1000:
            k = val / 1000
            return f"{k:.2f}".rstrip('0').rstrip('.') + " Thousand"
        else:
            return str(val)


class PropertyImage(models.Model):
    property = models.ForeignKey(Property, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='property_gallery/')

    def __str__(self):
        return f"Image for {self.property.title}"

#Enquiry Form

class Enquiry(models.Model):
    # agent = models.ForeignKey(
    #     settings.AUTH_USER_MODEL, 
    #     on_delete=models.SET_NULL, 
    #     null=True, 
    #     blank=True, 
    #     limit_choices_to={'role': 'agent'}, 
    #     related_name='assigned_leads'
    # )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='enquiries')
    property = models.ForeignKey('Property',on_delete=models.SET_NULL,null=True,blank=True,related_name='enquiries')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    subject = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )
    property_type = models.CharField(
        max_length=100, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    #visit_date = models.DateTimeField(blank=True, null=True)  # Visit ki date aur time ke liye
    #is_visited = models.BooleanField(default=False)          # Check karne ke liye ki visit ho gayi ya nahi

    STATUS_CHOICES = (
        ('Unread', 'Unread'),
        ('Read', 'Read'),
        ('Replied', 'Replied'),
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Unread'
    )

    created_at = models.DateTimeField(auto_now_add=True)  # Auto timestamp

    def __str__(self):
        return f'{self.name} - {self.phone}'

# Project Page
class Project(models.Model):
    CATEGORY_CHOICES = (
        ('ongoing', 'Ongoing Projects'),
        ('upcoming', 'Upcoming Projects'),
        ('completed', 'Completed Projects'),
    )

    title = models.CharField(max_length=200)
    location = models.CharField(max_length=150)
    description = models.TextField()
    image = models.ImageField(upload_to='projects/')
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=20)
    amenities = models.CharField(max_length=255, help_text="Comma separated (e.g., Club House, Gym)")
    status_text = models.CharField(max_length=50)
    possession_or_completion = models.CharField(max_length=50)

    def __str__(self):
        return self.title

    def get_amenities_list(self):
        return [a.strip() for a in self.amenities.split(',')]

# Agents Page

class Agent(models.Model):
    
    
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100, default="Property Consultant")
    experience = models.CharField(max_length=50, help_text="e.g., 6+ Years")
    phone = models.CharField(max_length=20)
    email = models.EmailField()

    # Additional Agent Details
    father_name = models.CharField(max_length=100, blank=True, null=True)

    aadhaar_document = models.FileField(
        upload_to='agent_documents/',
        blank=True,
        null=True
    )

    pan_document = models.FileField(
        upload_to='agent_documents/',
        blank=True,
        null=True
    )

    # Agent Status
    is_active = models.BooleanField(default=True)

    image = models.ImageField(upload_to='agents/')
    assigned_properties_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# Blogs Page Models

class BlogCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class BlogTag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(BlogCategory, on_delete=models.CASCADE, related_name='blogposts')
    tags = models.ManyToManyField(BlogTag, blank=True)
    image = models.ImageField(upload_to='blog_images/')
    excerpt = models.TextField(max_length=300)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# Contact Us

# class ContactMessage(models.Model):
#     full_name = models.CharField(max_length=100)
#     mobile_number = models.CharField(max_length=15)
#     email = models.EmailField()
#     subject = models.CharField(max_length=200)
#     message = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.full_name} - {self.subject}"

#Payment Model
class Payment(models.Model):
    PAYMENT_STATUS_CHOICES = (
        ('Completed', 'Completed'),
        ('Pending', 'Pending'),
        ('Failed', 'Failed'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='payments')
    property = models.ForeignKey('Property', on_delete=models.SET_NULL, null=True, blank=True)
    customer_name = models.CharField(max_length=100)
    amount = models.BigIntegerField()
    payment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='Pending')
    transaction_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.customer_name} - {self.amount} ({self.status})"

#Saved Property Model
class SavedProperty(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='saved_properties')
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} saved {self.property.title}"

# Booking Model
class Booking(models.Model):

    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )

    DEALER_CHOICES = (
        ('Yes', 'Yes'),
        ('No', 'No'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    property = models.ForeignKey(Property, on_delete=models.CASCADE)

    customer_name = models.CharField(
        max_length=100,
        default=''
    )

    mobile_number = models.CharField(
        max_length=15,
        default=''
    )

    customer_email = models.EmailField(
        default=''
    )

    booking_date = models.DateField(
        null=True,
        blank=True
    )

    message = models.TextField(
        blank=True,
        null=True
    )

    is_property_dealer = models.CharField(
        max_length=3,
        choices=DEALER_CHOICES,
        default='No'
    )

    status = models.CharField(max_length=50,choices=STATUS_CHOICES,default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} booked {self.property.title}"

# Site Visit Model
class SiteVisit(models.Model):
    agent = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'role': 'agent'})
    #enquiry = models.ForeignKey(Enquiry, on_delete=models.CASCADE, related_name='site_visits')
    schedule = models.ForeignKey('VisitSchedule',on_delete=models.CASCADE,related_name='site_visits',null=True,blank=True)
    location_visited = models.CharField(max_length=255)
    visit_image = models.ImageField(upload_to='site_visits/')
    notes = models.TextField(blank=True, null=True)

    # NEW: previous actual site visit
    previous_visit = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='next_visits'
    )

    visit_type = models.CharField(
        max_length=30,
        choices=(
            ('Revisit', 'Revisit'),
            ('Discussion', 'Discussion'),
            ('Final Visit', 'Final Visit'),
        ),
        blank=True,
        null=True
    )
    visit_purpose = models.TextField(
        blank=True,
        null=True
    )
    visit_date = models.DateTimeField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    # === Yeh naya column isi table me jud jayega ===
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"Visit for {self.schedule.name if self.schedule else 'Old Visit'} by {self.agent.email}"

class Commission(models.Model):
    # Yahan User ki jagah settings.AUTH_USER_MODEL use karenge
    agent = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    deal_title = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status_choices = (
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
    )
    status = models.CharField(max_length=20, choices=status_choices, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Commission - ₹{self.amount}"


class VisitSchedule(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Assigned', 'Assigned'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )

    property = models.ForeignKey('Property', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=15)
    visit_date = models.DateTimeField()
    message = models.TextField(blank=True, null=True)
    
    # Admin yahan agent assign karega
    agent = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        limit_choices_to={'role': 'agent'}, 
        related_name='scheduled_visits'
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.visit_date.date()}"