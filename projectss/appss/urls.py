from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('informant-page/', views.informant_page, name='informant_page'),
    path('submit-complaint/', views.submit_complaint, name='submit_complaint'),
    path('legal-office/', views.legal_office_page, name='legal_office_page'),
    path('admin-finance/', views.admin_finance_page, name='admin_finance_page'),
    path('academic-affairs/', views.academic_affairs_page, name='academic_affairs_page'),
    path('students-affairs/', views.students_affairs_page, name='students_affairs_page'),
    path('gad-office/', views.gad_office_page, name='gad_office_page'),
    # path('gad-office-status/', views.gad_office_status, name='gad_office_status'),
    # path('delete-complaint/<int:complaint_id>/', views.delete_complaint, name='delete_complaint'),
    path('delete-complaint/<int:complaint_id>/', views.delete_complaint, name='delete_complaint'),
    path('update-status/<int:complaint_id>/', views.update_status, name='update_status'),
    path('send-complaint/<int:complaint_id>/', views.send_complaint, name='send_complaint'),
    # path('send-message/', views.send_message, name='send_message'),
    # path('get-messages/', views.get_messages, name='get_messages'),  
    path('dashboard/', views.dashboard_page, name='dashboard_page'),
    path('complaint-report/', views.complaint_report, name='complaint_report'),
    # path('informant-registration/', views.informant_registration_view, name='informant_registration'),
    path('admin-page/', views.admin_page, name='admin_page'),
    path('status/', views.complaint_status, name='complaint_status'),
    path('history/', views.complaint_history, name='complaint_history'),
    # path('messages/', views.complaint_messages, name='complaint_messages'),
    path('complaint_message/<int:complaint_id>/', views.complaint_message, name='complaint_message'),
    path('profile/', views.profile_view, name='profile'),  # Profile link
    path('graphs/', views.generate_graphs, name='graphs'),
    # path('chat/<str:room_name>/', views.chat_room, name='chat_room'),
    path('update-urgency/<int:complaint_id>/', views.update_urgency, name='update_urgency'),
    path('gad-dashboard/', views.gad_dashboard, name='gad_dashboard'),
    path('admin-finance-dashboard/', views.admin_finance_dashboard, name='admin_finance_dashboard'),
    path('academic-affairs-dashboard/', views.academic_affairs_dashboard, name='academic_affairs_dashboard'),
    path('students-affairs-dashboard/', views.students_affairs_dashboard, name='students_affairs_dashboard'),

    path('register/', views.registration_page, name='registration_page'),
    path('login/', views.login_view, name='login'),
    path('login/legal/', views.legal_office_login_view, name='legal_office_login'),
    path('login/admin/', views.office_admin_login_view, name='office_admin_login'),


    path('create_informant/', views.create_informant, name='create_informant'),
    path('solved-graph/', views.history_view, name='grapg'),  # Route for the history page
    # path('generate_pdf/', views.generate_pdf, name='generate_pdf'),
    path('submit_response/', views.submit_response, name='submit_response'),
    path('delete_response/<int:response_id>/', views.delete_response, name='delete_response'),  # Add this line for delete
    path('update-office/<int:complaint_id>/', views.update_office, name='update_office'),
    path('update_type/<int:complaint_id>/', views.update_type, name='update_type'),
    path('incident-filter/', views.incident_filter, name='incident_filter'),
    path('complaint_counts/', views.complaint_counts, name='complaint_counts'),

    
    
    # Other URL patterns
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),


]
