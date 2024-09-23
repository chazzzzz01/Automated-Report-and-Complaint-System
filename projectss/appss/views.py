from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Complaint
from .model_utils import load_models
from .forms import ComplaintReportForm, MessageForm
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import InformantRegistrationForm
from .models import Informant

def home(request):
    return render(request,'main/home.html')


def registration_page(request):
    if request.method == 'POST':
        form = InformantRegistrationForm(request.POST)
        if form.is_valid():
            form.save()  # Save the form data to the database
            return redirect('home')  # Redirect to home page or another after successful registration
    else:
        form = InformantRegistrationForm()
    return render(request, 'main/registration.html', {'form': form})


def informant_page(request):
    complaints = Complaint.objects.all()

    return render(request, 'main/informant_page.html', {'complaints': complaints})


def admin_page(request):
    complaints = Complaint.objects.all()

    return render(request, 'main/admin_page.html', {'complaints': complaints})


# def submit_complaint(request):
#     if request.method == 'POST':
#         description = request.POST.get('description')

#         try:
#             category_model, type_model, vectorizer = load_models()
#             description_vec = vectorizer.transform([description])
#             predicted_category = category_model.predict(description_vec)[0]
#             predicted_type = type_model.predict(description_vec)[0]

#             complaint = Complaint(
#                 description=description,
#                 office=predicted_category,
#                 type=predicted_type,
#                 status='Pending'
#             )
#             complaint.save()

#             return redirect('legal_office_page')

#         except FileNotFoundError as e:
#             return HttpResponse(f"Error: {e}", status=500)

#         except Exception as e:
#             return HttpResponse(f"An unexpected error occurred: {e}", status=500)

#     return render(request, 'main/submit_complaint.html')



@csrf_exempt
def submit_complaint(request):
    if request.method == 'POST':
        description = request.POST.get('description')

        try:
            # Load the models
            category_model, type_model, vectorizer = load_models()
            
            # Vectorize the description
            description_vec = vectorizer.transform([description])
            
            # Predict category and type
            predicted_category = category_model.predict(description_vec)[0]
            predicted_type = type_model.predict(description_vec)[0]

            # Save the complaint as pending in the legal office
            complaint = Complaint(
                description=description,
                office= predicted_category, 
                type=predicted_type,
                status='Pending'
            )
            complaint.save()

            # Return a success message to the AJAX call
            return JsonResponse({'message': 'Complaint submitted to the legal office successfully!'}, status=200)

        except FileNotFoundError as e:
            return JsonResponse({'error': f"Error: {e}"}, status=500)

        except Exception as e:
            return JsonResponse({'error': f"An unexpected error occurred: {e}"}, status=500)

    return JsonResponse({'error': 'Invalid request method.'}, status=400)


def legal_office_page(request):
    
    complaints = Complaint.objects.all()

    return render(request, 'main/legal_office_page.html', {'complaints': complaints})




def complaint_status(request):
    # Retrieve unresolved complaints
    complaints = Complaint.objects.filter(status='Solved')
    return render(request, 'informant/complaint_status.html', {'complaints': complaints})

def complaint_history(request):
    # Retrieve solved complaints
    complaints = Complaint.objects.filter(status='Solved')
    return render(request, 'informant/complaint_history.html', {'complaints': complaints})

def complaint_messages(request):
    # This view might be used to handle messages or chats if necessary
    # For now, it just renders the messages page
    return render(request, 'informant/complaint_message.html')




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



# def delete_complaint(request, complaint_id):
    
#     complaint = get_object_or_404(Complaint, id=complaint_id)
#     complaint.delete()
#     return redirect('legal_office_page')


from django.shortcuts import get_object_or_404, redirect

def delete_complaint(request, complaint_id):
    complaint = get_object_or_404(Complaint, id=complaint_id)
    complaint.delete()
    # Redirect back to the referring page
    return redirect(request.META.get('HTTP_REFERER', 'legal_office_page'))


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





def dashboard_page(request):
    reports = Complaint.objects.filter(type="report")
    complaints = Complaint.objects.filter(type="complaint")
    solved_reports = reports.filter(status="Solved")
    solved_complaints = complaints.filter(status="Solved")
    pending_reports = reports.filter(status="Pending")
    pending_complaints = complaints.filter(status="Pending")
    inprogress_reports = reports.filter(status="In Progress")
    inprogress_complaints = complaints.filter(status="In Progress")

    return render(request, 'main/dashboard_page.html', {
        'total_reports': reports.count(),
        'total_complaints': complaints.count(),
        'solved_reports': solved_reports.count(),
        'solved_complaints': solved_complaints.count(),
        'pending_reports': pending_reports.count(),
        'pending_complaints': pending_complaints.count(),
        'inprogress_reports': inprogress_reports.count(),
        'inprogress_complaints': inprogress_complaints.count(),
    
        
    }
    )

    

















from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Complaint, Message
from .forms import MessageForm

def send_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.office = request.POST.get('office')  # Office is specified in the form
            message.save()
            return JsonResponse({'status': 'success', 'message': message.content})
    return JsonResponse({'status': 'error', 'message': 'Message not sent'})



from django.http import JsonResponse
from .models import Message

def get_messages(request):
    office = request.GET.get('office')
    messages = Message.objects.filter(office=office).values('content', 'sent')
    return JsonResponse({'messages': list(messages)})



    