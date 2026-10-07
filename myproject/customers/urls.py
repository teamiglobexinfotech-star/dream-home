from django.urls import path
from customers.views import  toggle_save_property, book_property
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    #path('forgot-password/', views.forgot_password_view, name='forgot_password'),
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),
    path('verify-otp/', views.verify_otp_view, name='verify_otp'),
    path('reset-password/', views.reset_password_view, name='reset_password'),

    path('agent/add/', views.add_agent_view, name='add_agent'),
    path('agent/edit/<int:pk>/', views.edit_agent_view, name='edit_agent'),
    path('agent/delete/<int:pk>/', views.delete_agent_view, name='delete_agent'),
    path('customer-dashboard/', views.customer_dashboard_view, name='customer_dashboard'),
    path('save-property/<int:property_id>/', toggle_save_property, name='toggle_save_property'),
    #path('dashboard/saved-properties/', saved_properties_view, name='saved_properties'),
    path('ajax/saved-properties/', views.ajax_all_saved_properties, name='ajax_all_saved_properties'),
    path('book-property/<int:property_id>/', book_property, name='book_property'),
    path('api/my-bookings/', views.ajax_my_bookings, name='ajax_my_bookings'),
    path('api/my-enquiries/', views.ajax_my_enquiries, name='ajax_my_enquiries'),
    path('api/my-site-visits/', views.ajax_my_site_visits, name='ajax_my_site_visits'),
    path('customer/support/', views.customer_support_view, name='customer_support'),
    path('dashboard/profile/', views.customer_profile, name='customer_profile'),
    path('dashboard/profile/edit/', views.ajax_customer_profile_edit, name='ajax_customer_profile_edit'),
    path('change-password/', views.change_password, name='change_password'),
    #path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('logout/', views.customer_logout_view, name='logout'),
    path('ajax/customer-notifications/', views.fetch_customer_notifications_ajax, name='fetch_customer_notifications_ajax'),
    path('ajax/mark-notification-read/', views.mark_customer_ajax_read, name='mark_customer_ajax_read'),
    path('popup-login/', views.popup_login_view, name='popup_login'),
    path('site-visits-page/',views.customer_site_visits_page,name='customer_site_visits_page'),

]