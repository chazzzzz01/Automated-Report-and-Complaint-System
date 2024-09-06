from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Complaint
from .model_utils import load_models

def home(request):
    return render(request,'main/home.html')

def informant_page(request):
    complaints = Complaint.objects.all()
    return render(request, 'main/informant_page.html', {'complaints': complaints})

def submit_complaint(request):
    if request.method == 'POST':
        description = request.POST.get('description')

        try:
            category_model, type_model, vectorizer = load_models()
            description_vec = vectorizer.transform([description])
            predicted_category = category_model.predict(description_vec)[0]
            predicted_type = type_model.predict(description_vec)[0]

            complaint = Complaint(
                description=description,
                office=predicted_category,
                type=predicted_type,
                status='Pending'
            )
            complaint.save()

            return redirect('legal_office_page')

        except FileNotFoundError as e:
            return HttpResponse(f"Error: {e}", status=500)

        except Exception as e:
            return HttpResponse(f"An unexpected error occurred: {e}", status=500)

    return render(request, 'main/submit_complaint.html')

def legal_office_page(request):
    
    complaints = Complaint.objects.all()

    return render(request, 'main/legal_office_page.html', {'complaints': complaints})


def update_status(request, complaint_id):
    complaint = get_object_or_404(Complaint, id=complaint_id)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        complaint.status = new_status
        complaint.save()

        # Redirect back to the current office page
        redirect_url = request.POST.get('redirect_url', 'legal_office_page')
        return redirect(redirect_url)

    return redirect('legal_office_page')



# # def update_office(request, complaint_id):
# #     complaint = get_object_or_404(Complaint, id=complaint_id)

# #     if request.method == 'POST':
# #         new_office = request.POST.get('office')
# #         if new_office in dict(Complaint.OFFICE_CHOICES):
# #             complaint.office = new_office
# #             complaint.save()

# #     return redirect('legal_office_page')

# #  <td> THIS IS FOR LEGAL_OFFICE_PAGE.HTML TEMAPLATE FOR UPDATE OFFICE
# #                     <form action="{% url 'update_office' complaint.id %}" method="post">
# #                         {% csrf_token %}
# #                         <select name="office">
# #                             <option value="Admin and Finance" {% if complaint.office == "Admin and Finance" %}selected{% endif %}>Admin and Finance</option>
# #                             <option value="VP Academic Affairs" {% if complaint.office == "VP Academic Affairs" %}selected{% endif %}>VP Academic Affairs</option>
# #                             <option value="VP Students and External Affairs" {% if complaint.office == "VP Students and External Affairs" %}selected{% endif %}>VP Students and External Affairs</option>
# #                             <option value="GAD Office" {% if complaint.office == "GAD Office" %}selected{% endif %}>GAD Office</option>
# #                         </select>
# #                         <button type="submit">Update</button>
# #                     </form>
# #                 </td>


def delete_complaint(request, complaint_id):
    # complaint = get_object_or_404(Complaint, id=complaint_id)
    # office = complaint.office  # Capture the office from the complaint
    # complaint.delete()

    # office_redirect_map = {
    #     'VP Administration and Finance': 'admin_finance_page',
    #     'VP Academic Affairs': 'academic_affairs_page',
    #     'VP Students and External Affairs': 'students_affairs_page',
    #     'GAD Office': 'gad_office_page',
    #     'Legal Office': 'legal_office_page',
    # }

    # office_page = office_redirect_map.get(office, 'legal_office_page')
    # return redirect(office_page)
    complaint = get_object_or_404(Complaint, id=complaint_id)
    complaint.delete()
    return redirect('legal_office_page')

def send_complaint(request, complaint_id):
    complaint = get_object_or_404(Complaint, id=complaint_id)
    
    if complaint.is_sent:
        return redirect('legal_office_page')
    
    try:
        complaint.is_sent = True
        complaint.save()

        office_redirect_map = {
            'VP Administration and Finance': 'admin_finance_page',
            'VP Academic Affairs': 'academic_affairs_page',
            'VP Students and External Affairs': 'students_affairs_page',
            'GAD Office': 'gad_office_page',
            'Legal Office': 'legal_office_page',
        }

        office_page = office_redirect_map.get(complaint.office, 'legal_office_page')
        return redirect(office_page)

    except Exception as e:
        return HttpResponse(f"An error occurred while sending the complaint: {e}", status=500)

def admin_finance_page(request):
    reports = Complaint.objects.filter(office="VP Administration and Finance", type="report")
    complaints = Complaint.objects.filter(office="VP Administration and Finance", type="complaint")
    return render(request, 'main/admin_finance_page.html', {'reports': reports, 'complaints': complaints})

def academic_affairs_page(request):
    reports = Complaint.objects.filter(office="VP Academic Affairs", type="report")
    complaints = Complaint.objects.filter(office="VP Academic Affairs", type="complaint")
    return render(request, 'main/academic_affairs_page.html', {'reports': reports, 'complaints': complaints})

def students_affairs_page(request):
    reports = Complaint.objects.filter(office="VP Students and External Affairs", type="report")
    complaints = Complaint.objects.filter(office="VP Students and External Affairs", type="complaint")
    return render(request, 'main/students_affairs_page.html', {'reports': reports, 'complaints': complaints})

def gad_office_page(request):
    reports = Complaint.objects.filter(office="GAD Office", type="report")
    complaints = Complaint.objects.filter(office="GAD Office", type="complaint")
    return render(request, 'main/gad_office_page.html', {'reports': reports, 'complaints': complaints})

def gad_office_status(request):
    # Logic for status page
    return render(request, 'main/gad_office_status.html')












