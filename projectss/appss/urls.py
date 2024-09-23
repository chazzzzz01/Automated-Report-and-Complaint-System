from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('informant-page/', views.informant_page, name='informant_page'),
    path('submit-complaint/', views.submit_complaint, name='submit_complaint'),
    path('legal-office/', views.legal_office_page, name='legal_office_page'),
    path('admin-finance/', views.admin_finance_page, name='admin_finance_page'),
    path('academic-affairs/', views.academic_affairs_page, name='academic_affairs_page'),
    path('students-affairs/', views.students_affairs_page, name='students_affairs_page'),
    path('gad-office/', views.gad_office_page, name='gad_office_page'),
    path('gad-office-status/', views.gad_office_status, name='gad_office_status'),
    # path('delete-complaint/<int:complaint_id>/', views.delete_complaint, name='delete_complaint'),
    path('delete-complaint/<int:complaint_id>/', views.delete_complaint, name='delete_complaint'),
    path('update-status/<int:complaint_id>/', views.update_status, name='update_status'),
    path('send-complaint/<int:complaint_id>/', views.send_complaint, name='send_complaint'),
    path('send-message/', views.send_message, name='send_message'),
    path('get-messages/', views.get_messages, name='get_messages'),  # New URL pattern
    path('dashboard/', views.dashboard_page, name='dashboard_page'),
    # path('informant-registration/', views.informant_registration_view, name='informant_registration'),
    path('admin-page/', views.admin_page, name='admin_page'),
    path('status/', views.complaint_status, name='complaint_status'),
    path('history/', views.complaint_history, name='complaint_history'),
    path('messages/', views.complaint_messages, name='complaint_messages'),
    
    path('register/', views.registration_page, name='registration_page'),
   
]
