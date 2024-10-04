from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Complaint
from .model_utils import load_models
from .forms import MessageForm
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import InformantRegistrationForm
from .models import Informant, Complaint
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request,'main/home.html')




from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import InformantRegistrationForm

def registration_page(request):
    if request.method == 'POST':
        form = InformantRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the user and set the password
            user = form.save(commit=False)
            password = form.cleaned_data.get('password')  # Use .get to safely access the password
            if password:
                user.set_password(password)  # Hash the password
                user.save()

                # Redirect to the login page after successful registration
                messages.success(request, 'Registration successful. You can now log in.')
                return redirect('login')  # Adjust the URL name as needed
            else:
                messages.error(request, 'Password not provided.')
        else:
            messages.error(request, 'Form is not valid. Please check the information entered.')
    else:
        form = InformantRegistrationForm()

    return render(request, 'main/registration.html', {'form': form})



from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import redirect

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('login_username')
        password = request.POST.get('login_password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')

            # Redirect users based on role
            if user.is_superuser:  # Legal Office (Superuser)
                return redirect('legal_office_page')
            elif user.is_staff:  # Office Admins (Staff users)
                if user.username == 'GADAdmin':
                    return redirect('gad_office_page')
                elif user.username == 'vp_admin_finance':
                    return redirect('admin_finance_page')
                elif user.username == 'vp_academic_affairs':
                    return redirect('academic_affairs_page')
                elif user.username == 'vp_students_affairs':
                    return redirect('students_affairs_page')
            else:
                # If the user is an Informant, redirect to their page
                return redirect('informant_page')

        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'main/login.html')



# Profile view
def profile_view(request):
    informant = request.user  # Assumes the user is logged in
    return render(request, 'informant/profile.html', {'informant': informant})




# informant
@login_required
def informant_page(request):
    complaints = Complaint.objects.all()


    return render(request, 'main/informant_page.html', {'complaints': complaints})



















# @login_required
# def profile_view(request):
#     # Get the logged-in informant's profile (assuming user has 1-1 relation with Informant)
#     informant = get_object_or_404(Informant, username=request.user.username)
#     return render(request, 'informant/profile.html', {'informant': informant})









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
                status='Pending',
                is_sent=False
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
    reports = Complaint.objects.filter(office="VP Administration and Finance", type="report", is_sent=True)
    complaints = Complaint.objects.filter(office="VP Administration and Finance", type="complaint", is_sent=True)
    return render(request, 'main/admin_finance_page.html', {'reports': reports, 'complaints': complaints})

# Academic Affairs Office
def academic_affairs_page(request):
    reports = Complaint.objects.filter(office="VP Academic Affairs", type="report", is_sent=True)
    complaints = Complaint.objects.filter(office="VP Academic Affairs", type="complaint", is_sent=True)
    return render(request, 'main/academic_affairs_page.html', {'reports': reports, 'complaints': complaints})

# Students Affairs Office
def students_affairs_page(request):
    reports = Complaint.objects.filter(office="VP Students and External Affairs", type="report", is_sent=True)
    complaints = Complaint.objects.filter(office="VP Students and External Affairs", type="complaint", is_sent=True)
    return render(request, 'main/students_affairs_page.html', {'reports': reports, 'complaints': complaints})

# Gad Office
def gad_office_page(request):
    reports = Complaint.objects.filter(office="GAD Office", type="report", is_sent=True)
    complaints = Complaint.objects.filter(office="GAD Office", type="complaint", is_sent=True)
    return render(request, 'main/gad_office_page.html', {'reports': reports, 'complaints': complaints})



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

    

# def gad_office_status(request):
#     # Logic for status page
#     return render(request, 'main/gad_office_status.html')







from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Complaint

# View to update the urgency of a complaint
def update_urgency(request, complaint_id):
    complaint = get_object_or_404(Complaint, id=complaint_id)
    if request.method == 'POST':
        urgency = request.POST.get('urgency')
        if urgency:
            complaint.urgency = urgency
            complaint.save()
    return redirect(reverse('legal_office_page'))

# Other existing views (update_status, send_complaint, delete_complaint)...















# views.py
import matplotlib.pyplot as plt
from django.shortcuts import render
from io import BytesIO
import base64

def generate_graphs(request):
    # Example data, replace with your actual data fetching logic
    reports = [
        {'office': 'STCS', 'status': 'Solved'},
        {'office': 'SCJE', 'status': 'Solved'},
        {'office': 'SAS', 'status': 'Solved'},
        {'office': 'SME', 'status': 'Pending'},
        {'office': 'SOE', 'status': 'Solved'},
        {'office': 'SNHS', 'status': 'Solved'},
        {'office': 'LHS', 'status': 'Solved'},
        {'office': 'STED', 'status': 'Pending'},
        {'office': 'STCS', 'status': 'Solved'},
    ]

    complaints = [
        {'office': 'STCS', 'status': 'Solved'},
        {'office': 'SCJE', 'status': 'Pending'},
        {'office': 'SAS', 'status': 'Solved'},
        {'office': 'SME', 'status': 'Solved'},
        {'office': 'SOE', 'status': 'Pending'},
        {'office': 'SNHS', 'status': 'Solved'},
    ]

    # Define the school mapping
    school_mapping = {
        'STCS': 'School of Technology and Computer Science',
        'SCJE': 'School of Criminal Justice and Education',
        'SAS': 'School of Arts and Sciences',
        'SME': 'School of Management and Entrepreneurship',
        'SOE': 'School of Engineering',
        'SNHS': 'School of Nursing and Health Sciences',
        'LHS': 'Liberal Arts and Humanities',
        'STED': 'School of Teacher Education'
    }

    # Filter solved reports
    solved_reports = [report for report in reports if report['status'] == "Solved"]
    solved_complaints = [complaint for complaint in complaints if complaint['status'] == "Solved"]

    # Count occurrences for solved reports by office
    report_offices = [report['office'] for report in solved_reports]
    report_counts = [report_offices.count(office) for office in set(report_offices)]

    # Count occurrences for solved complaints by office
    complaint_offices = [complaint['office'] for complaint in solved_complaints]
    complaint_counts = [complaint_offices.count(office) for office in set(complaint_offices)]

    # Generate the reports graph
    report_labels = list(set(report_offices))
    plt.figure(figsize=(10, 5))
    plt.bar(report_labels, report_counts, color='c', alpha=0.6)
    plt.title('Solved Reports by Office')
    plt.xlabel('Offices')
    plt.ylabel('Number of Solved Reports')
    plt.xticks(rotation=45)

    # Save to a BytesIO object
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)
    report_image = base64.b64encode(buffer.read()).decode('utf-8')

    # Generate the complaints graph
    complaint_labels = list(set(complaint_offices))
    plt.figure(figsize=(10, 5))
    plt.bar(complaint_labels, complaint_counts, color='m', alpha=0.6)
    plt.title('Solved Complaints by Office')
    plt.xlabel('Offices')
    plt.ylabel('Number of Solved Complaints')
    plt.xticks(rotation=45)

    # Save to a BytesIO object
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    complaint_image = base64.b64encode(buffer.read()).decode('utf-8')

    return render(request, 'report_complaint_graphs.html', {
        'report_image': report_image,
        'complaint_image': complaint_image,
        'report_labels': report_labels,
        'complaint_labels': complaint_labels,
        'school_mapping': school_mapping,
    })





# appss/views.py

from django.shortcuts import render
from .models import Office  # Assuming you have an Office model

def chat_room(request):
    offices = Office.objects.all()  # Fetch all office instances
    return render(request, 'appss/complaint_message.html', {
        'offices': offices,
    })










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



    