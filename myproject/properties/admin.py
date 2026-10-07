from django.contrib import admin
from .models import Category, Property, PropertyImage, Enquiry
from .models import Project
from .models import Agent
from .models import BlogCategory, BlogPost, BlogTag
from .models import Booking

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

# Multiple images ke liye inline admin
class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 4  # Ek saath 4 images add karne ke slots dega

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'status', 'price', 'location', 'featured')
    list_filter = ('status', 'category', 'city', 'featured')
    search_fields = ('title', 'location', 'city')
    
    # Yeh line multiple images ko property ke andar show karegi
    inlines = [PropertyImageInline]

# Project Page

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'location', 'possession_or_completion')
    list_filter = ('category', 'location')
    search_fields = ('title', 'location')

# --- Enquiry & Contact Admin Registrations ---
@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'property_type', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'email', 'phone', 'property_type')

# @admin.register(ContactMessage)
# class ContactMessageAdmin(admin.ModelAdmin):
#     list_display = ('full_name', 'mobile_number', 'email', 'subject', 'created_at')
#     list_filter = ('created_at',)
#     search_fields = ('full_name', 'email', 'subject', 'mobile_number')

#Agent Page


@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'phone', 'assigned_properties_count')




# --- Blog Admin Registrations ---

@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(BlogTag)
class BlogTagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'content')
    filter_horizontal = ('tags',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'property', 'status', 'created_at') # Agar koi aur fields hain toh wo bhi dal sakte hain
    search_fields = ('user__username', 'property__title')