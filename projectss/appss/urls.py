from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('submit/', views.submit_complaint, name='submit_complaint'),
    path('informant/', views.informant_page, name='informant_page'),
    path('legal-office/', views.legal_office_page, name='legal_office_page'),
    
    # path('update-office/<int:complaint_id>/', views.update_office, name='update_office'),
    path('update-status/<int:complaint_id>/', views.update_status, name='update_status'),
    path('send/<int:complaint_id>/', views.send_complaint, name='send_complaint'),
    path('delete/<int:complaint_id>/', views.delete_complaint, name='delete_complaint'),
    path('admin-finance/', views.admin_finance_page, name='admin_finance_page'),
    path('academic-affairs/', views.academic_affairs_page, name='academic_affairs_page'),
    path('students-affairs/', views.students_affairs_page, name='students_affairs_page'),
    path('gad-office/', views.gad_office_page, name='gad_office_page'),
    
]
