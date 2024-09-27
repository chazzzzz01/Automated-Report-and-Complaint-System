from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Complaint
from .model_utils import load_models
from .forms import MessageForm
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import InformantRegistrationForm
from .models import Informant
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request,'main/home.html')

from django.shortcuts import render, redirect
from .forms import InformantRegistrationForm

# registration view
def registration_page(request):
    if request.method == 'POST':
        form = InformantRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('informant_page')  # redirect to login after successful registration
    else:
        form = InformantRegistrationForm()
    
    return render(request, 'main/registration.html', {'form': form})
















from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Office

def login_view(request):
    if request.method == 'POST':
        username = request.POST['login_username']
        password = request.POST['login_password']
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Check if the user is associated with an office
            if hasattr(user, 'office'):
                office = user.office

                # Redirect based on the office name
                if office.office_name == 'GAD Office':
                    return redirect('gad_office_page')
                elif office.office_name == 'VP Administration and Finance':
                    return redirect('admin_finance_page')
                elif office.office_name == 'VP Academic Affairs':
                    return redirect('academic_affairs_page')
                elif office.office_name == 'VP Students and External Affairs':
                    return redirect('students_affairs_page')
                else:
                    messages.error(request, "Office role not recognized")
            else:
                # Handle other roles such as informant, main admin, etc.
                if hasattr(user, 'role'):
                    if user.role == 'informant':
                        return redirect('informant_page')
                    elif user.role == 'main_admin':
                        return redirect('main_admin_page')
                    elif user.role == 'office_admin':
                        return redirect('office_admin_page')
                    else:
                        messages.error(request, "User role not recognized")
                else:
                    messages.error(request, "User role not found")
        else:
            messages.error(request, "Invalid credentials")
    
    return render(request, 'main/login.html')








# informant
def informant_page(request):
    complaints = Complaint.objects.all()

    return render(request, 'main/informant_page.html', {'complaints': complaints})



















# @login_required
# def profile_view(request):
#     # Get the logged-in informant's profile (assuming user has 1-1 relation with Informant)
#     informant = get_object_or_404(Informant, username=request.user.username)
#     return render(request, 'informant/profile.html', {'informant': informant})


def profile_view(request):
    complaints = Complaint.objects.all()
    return render(request, 'main/profile.html')
    
def admin_page(request):
    complaints = Complaint.objects.all()

    return render(request, 'main/admin_page.html', {'complaints': complaints})

#lodging
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

#legal Office
def legal_office_page(request):
    
    complaints = Complaint.objects.all()

    return render(request, 'main/legal_office_page.html', {'complaints': complaints})




def complaint_status(request):
    # Pending complaints
    complaints = Complaint.objects.filter(status='Solved')
    return render(request, 'informant/complaint_status.html', {'complaints': complaints})

def complaint_history(request):
    # Solved complaints
    complaints = Complaint.objects.filter(status='Solved')
    return render(request, 'informant/complaint_history.html', {'complaints': complaints})


#still in process
def complaint_messages(request):
    #used to handle messages or chats 
    # For now, it just renders the messages page
    return render(request, 'informant/complaint_message.html')



# Updating Status
def update_status(request, complaint_id):
    complaint = get_object_or_404(Complaint, id=complaint_id)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        complaint.status = new_status
        complaint.save()

      
        redirect_url = request.POST.get('redirect_url', 'legal_office_page')
        return redirect(redirect_url)

    return redirect('legal_office_page')



# def delete_complaint(request, complaint_id):
    
#     complaint = get_object_or_404(Complaint, id=complaint_id)
#     complaint.delete()
#     return redirect('legal_office_page')



#delete features in table
def delete_complaint(request, complaint_id):
    complaint = get_object_or_404(Complaint, id=complaint_id)
    complaint.delete()
   
    return redirect(request.META.get('HTTP_REFERER', 'legal_office_page'))

#send feature
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

# Administration and Finance Office
def admin_finance_page(request):
    reports = Complaint.objects.filter(office="VP Administration and Finance", type="report")
    complaints = Complaint.objects.filter(office="VP Administration and Finance", type="complaint")
    return render(request, 'main/admin_finance_page.html', {'reports': reports, 'complaints': complaints})

# Academic Affairs Office
def academic_affairs_page(request):
    reports = Complaint.objects.filter(office="VP Academic Affairs", type="report")
    complaints = Complaint.objects.filter(office="VP Academic Affairs", type="complaint")
    return render(request, 'main/academic_affairs_page.html', {'reports': reports, 'complaints': complaints})

# Students Affairs Office
def students_affairs_page(request):
    reports = Complaint.objects.filter(office="VP Students and External Affairs", type="report")
    complaints = Complaint.objects.filter(office="VP Students and External Affairs", type="complaint")
    return render(request, 'main/students_affairs_page.html', {'reports': reports, 'complaints': complaints})

# Gad Office
def gad_office_page(request):
    reports = Complaint.objects.filter(office="GAD Office", type="report")
    complaints = Complaint.objects.filter(office="GAD Office", type="complaint")
    return render(request, 'main/gad_office_page.html', {'reports': reports, 'complaints': complaints})


# def gad_office_status(request):
#     # Logic for status page
#     return render(request, 'main/gad_office_status.html')




# Dashboard
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

    





















# from django.shortcuts import render, redirect
# from django.http import JsonResponse
# from .models import Complaint, Message
# from .forms import MessageForm

# def send_message(request):
#     if request.method == 'POST':
#         form = MessageForm(request.POST)
#         if form.is_valid():
#             message = form.save(commit=False)
#             message.office = request.POST.get('office')  # Office is specified in the form
#             message.save()
#             return JsonResponse({'status': 'success', 'message': message.content})
#     return JsonResponse({'status': 'error', 'message': 'Message not sent'})



# from django.http import JsonResponse
# from .models import Message

# def get_messages(request):
#     office = request.GET.get('office')
#     messages = Message.objects.filter(office=office).values('content', 'sent')
#     return JsonResponse({'messages': list(messages)})



    