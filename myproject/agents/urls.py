from django.urls import path
from agents.views import agent_logout_view
from .views import AgentPasswordChangeView
from agents import views as agent_views
from . import views

urlpatterns = [
    path('dashboard/', views.agent_dashboard_view, name='agent_dashboard'),
    path('my-properties/', views.agent_properties_view, name='agent_properties'),
    path('dashboard/leads/', views.agent_leads_view, name='agent_leads'),
    path('dashboard/properties/add/', views.agent_add_property_view, name='agent_add_property'),
    #path('logout/', LogoutView.as_view(http_method_names=['get', 'post'], next_page='login'), name='logout'),
    path('site-visits/', agent_views.agent_site_visits_view, name='agent_site_visits'),
    path('site-visits/edit/<int:pk>/', agent_views.agent_edit_site_visit_view, name='agent_edit_site_visit'),
    path('site-visits/delete/<int:pk>/', agent_views.agent_delete_site_visit_view, name='agent_delete_site_visit_delete'),
    path('agent/commission/', views.agent_commission_view, name='agent_commission'),
    path('profile/', views.agent_own_profile_view, name='agent_own_profile'),
    path('logout/', agent_logout_view, name='agent_logout'),
    path('settings/change-password/', AgentPasswordChangeView.as_view(), name='agent_change_password'),
    path('mark-ajax-read/', views.agent_mark_ajax_read, name='agent_mark_ajax_read'),

    path('site-visits/next/<int:pk>/',agent_views.agent_next_site_visit_view,name='agent_next_site_visit'),

    path('dashboard/properties/edit/<int:pk>/',views.agent_edit_property_view,name='agent_edit_property'),
]