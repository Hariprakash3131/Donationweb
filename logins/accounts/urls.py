from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('my-activities/', views.my_activities, name='my_activities'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('contact-admin/', views.contact_admin_dashboard, name='contact_admin_dashboard'),
    path('contact-admin/delete/<int:message_id>/', views.delete_contact_message, name='delete_contact_message'),
    
    path('scholarship/apply/', views.scholarship_form, name='scholarship_form'),
    path('scholarship/success/', views.success_page, name='success_page'),
    
    path('donation/', views.donation_form, name='donation_form'),
    path('payment/<int:donation_id>/', views.payment, name='payment'),
    path('payment-success/<int:donation_id>/', views.payment_success, name='payment_success'),
    
    # Admin dashboard URLs
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-dashboard/update-status/', views.update_application_status, name='update_application_status'),
    path('admin-dashboard/delete-application/<int:application_id>/', views.delete_application, name='delete_application'),
]
