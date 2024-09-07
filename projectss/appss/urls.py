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
    path('delete-complaint/<int:complaint_id>/', views.delete_complaint, name='delete_complaint'),
    path('update-status/<int:complaint_id>/', views.update_status, name='update_status'),
    path('send-complaint/<int:complaint_id>/', views.send_complaint, name='send_complaint'),
    path('send-message/', views.send_message, name='send_message'),
      path('get-messages/', views.get_messages, name='get_messages'),  # New URL pattern

]

