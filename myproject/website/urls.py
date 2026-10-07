from django.urls import path
from . import views
from properties import views as property_views
from .views import submit_visit_schedule


urlpatterns = [
    path('', views.home, name='home'),
     path("about/", views.about, name="about"),
     path('properties/', views.property_list_view, name='properties'),
     path('submit-enquiry/', views.submit_enquiry, name='submit_enquiry'),
    path('projects/', views.projects_view, name='projects'),
    path('agents/', views.agents_view, name='agents'),
    path('blogs/', views.blogs_view, name='blogs'),
    path('contact/', views.contact_view, name='contact'),
    path('schedule-visit/', submit_visit_schedule, name='submit_visit_schedule'),

    # Admin URLs
    path('admin/properties/', property_views.admin_property_list, name='admin_property_list'),
    path('admin/properties/add/', property_views.add_property, name='add_property'),
    path('admin/properties/edit/<int:pk>/', property_views.edit_property, name='edit_property'),
    path('admin/properties/delete/<int:pk>/', property_views.delete_property, name='delete_property'),



     
    
  
]
