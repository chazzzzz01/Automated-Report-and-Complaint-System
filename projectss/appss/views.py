from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Complaint
from .model_utils import load_models
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import InformantRegistrationForm
from .models import Informant, Complaint
from django.contrib.auth import authenticate, login 
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from appss.models import Informant
from django.contrib.auth import authenticate, login





def home(request):
    return render(request,'main/home.html')



def registration_page(request):
    if request.method == 'POST':
        form = InformantRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            
            informant = form.save(commit=False)
            password = form.cleaned_data['password']
            if password:
                informant.set_password(password)
                informant.save()

                informant = authenticate(request, username=informant.username, password=password)
            if informant is not None:
                # Log the informant in automatically after registration
                login(request, informant)
                # Redirect to the login page after successful registration
                messages.success(request, 'Registration successful. You can now log in.')
                return redirect('login')
            else:
                messages.error(request, 'Password not provided.')
        else:
            messages.error(request, 'Form is not valid. Please check the information entered.')
    else:
        form = InformantRegistrationForm()

    return render(request, 'main/registration.html', {'form': form})




def create_informant(request):
    if request.method == 'POST':
        form = InformantRegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']

            # Check if the email already exists
            if Informant.objects.filter(email=email).exists():
                messages.error(request, "This email address is already in use.")
                return render(request, 'main/create_informant.html', {'form': form})
            
            # Save the form and create the informant
            user = form.save(commit=False)
            user.is_staff = form.cleaned_data.get('is_staff', False)
            user.is_superuser = form.cleaned_data.get('is_superuser', False)
            user.save()

            # Check if the created user matches one of the specific office roles
            if user.username in ['GADAdmin', 'vp_admin_finance', 'vp_academic_affairs', 'vp_students_affairs', 'legal_admin']:
                messages.success(request, f"Account created successfully for {user.username}!")
            else:
                messages.success(request, 'Account created successfully!')

            # Redirect back to the creation form to allow creating more accounts
            return redirect('create_informant')

    else:
        form = InformantRegistrationForm()

    return render(request, 'main/create_informant.html', {'form': form})



# def login_view(request):
#     if request.method == 'POST':
#         # Get the username and password from the login form
#         username = request.POST.get('login_username')
#         password = request.POST.get('login_password')

#         # Authenticate the informant using the custom Informant model
#         informant = authenticate(request, username=username, password=password)

#         if informant:
#             # Log the informant in
#             # login(request, informant)
#             # messages.success(request, 'Login successful!')
#             # Store informant ID in session to maintain login state
#             # request.session['informant_id'] = informant.id
#             # messages.success(request, 'Login successful!')

#             request.session.flush()

#             # Log the informant in by starting a fresh session and setting informant ID
#             login(request, informant)  # This also sets user info for auth middleware

#             # Store the informant ID to retrieve specific user data in views
#             request.session['informant_id'] = informant.id

#             messages.success(request, 'Login successful!')

#             # Redirect users based on \role
#             if informant.is_superuser:  # Legal Office (Superuser)
#                 if informant.username == 'legal_admin':
#                     return redirect('legal_office_page')
#             elif informant.is_staff:  # Office Admins (Staff users)
#                 if informant.username == 'GADAdmin':
#                     return redirect('gad_office_page')
#                 elif informant.username == 'vp_admin_finance':
#                     return redirect('admin_finance_page')
#                 elif informant.username == 'vp_academic_affairs':
#                     return redirect('academic_affairs_page')
#                 elif informant.username == 'vp_students_affairs':
#                     return redirect('students_affairs_page')
#             else:
#                 # If the user is a regular Informant, redirect to their page
#                 return redirect('informant_page')  # Ensure this view exists
#         else:
#             # If authentication fails, show an error message
#             messages.error(request, 'Invalid username or password.')
    
#     # Render the login page
#     return render(request, 'main/login.html')




from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import redirect, render

def login_view(request):
    if request.method == 'POST':
        # Get the username and password from the login form
        username = request.POST.get('login_username')
        password = request.POST.get('login_password')

        # Authenticate the informant using the custom Informant model
        informant = authenticate(request, username=username, password=password)

        if informant:
            request.session.flush()
            login(request, informant)
            request.session['informant_id'] = informant.id
            messages.success(request, 'Login successful!')

            # Redirect only to the informant page
            return redirect('informant_page')
        else:
            # If authentication fails, show an error message
            messages.error(request, 'Invalid username or password.')
    
    # Render the login page
    return render(request, 'main/login.html')



from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import redirect, render

# Legal Office Login View
def legal_office_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('login_username')
        password = request.POST.get('login_password')

        informant = authenticate(request, username=username, password=password)

        if informant:
            request.session.flush()
            login(request, informant)
            request.session['informant_id'] = informant.id
            messages.success(request, 'Login successful!')

            # Redirect only if the user is the legal office admin
            if informant.is_superuser and informant.username == 'legal_admin':
                return redirect('legal_office_page')
            else:
                messages.error(request, 'You do not have permission to access this area.')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'main/login_legal.html')

# Office Admin Login View
def office_admin_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('login_username')
        password = request.POST.get('login_password')

        informant = authenticate(request, username=username, password=password)

        if informant:
            request.session.flush()
            login(request, informant)
            request.session['informant_id'] = informant.id
            messages.success(request, 'Login successful!')

            # Redirect based on office admin roles
            if informant.is_staff:
                if informant.username == 'GADAdmin':
                    return redirect('gad_office_page')
                elif informant.username == 'vp_admin_finance':
                    return redirect('admin_finance_page')
                elif informant.username == 'vp_academic_affairs':
                    return redirect('academic_affairs_page')
                elif informant.username == 'vp_students_affairs':
                    return redirect('students_affairs_page')
            else:
                messages.error(request, 'You do not have permission to access this area.')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'main/login_offices.html')











from django.shortcuts import render
from django.contrib.auth.decorators import login_required  # Ensure only logged-in users can access the profile
from .models import Informant

@login_required
def profile_view(request):
    user = request.user
    print(user.student_id_file.url if user.student_id_file else "No student_id_file")
    print(user.employee_id_file.url if user.employee_id_file else "No employee_id_file")
    print(user.study_load_file.url if user.study_load_file else "No study_load_file")
    print(user.document_file.url if user.document_file else "No document_file")
    return render(request, 'informant/profile.html', {'user': request.user})




# # informant
# def informant_page(request):
#        # Assuming `request.user` is your custom `Informant` instance after login
#     complaints = Complaint.objects.all()
#     return render(request, 'main/informant_page.html', {'complaints': complaints})


from django.contrib import messages
from .models import Informant
from django.shortcuts import render, redirect

def authenticate_informant(username, password):
    try:
        informant = Informant.objects.get(username=username, password=password)
        return informant
    except Informant.DoesNotExist:
        return None



from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .models import Informant

@login_required
def informant_page(request):
    informant_id = request.session.get('informant_id')
    if not informant_id:
        return redirect('login')
    
    try:
        informant = Informant.objects.get(id=informant_id)
        complaints = Complaint.objects.filter(informant=informant)
        if informant.is_superuser and informant.username == 'legal_admin':
            return redirect('legal_office_page')
        if informant.is_staff:
            if informant.username == 'GADAdmin':
                return redirect('gad_office_page')
            elif informant.username == 'vp_admin_finance':
                return redirect('admin_finance_page')
            elif informant.username == 'vp_academic_affairs':
                return redirect('academic_affairs_page')
            elif informant.username == 'vp_students_affairs':
                return redirect('students_affairs_page')
            elif informant.username == 'legal_admin':
                return redirect('')
    except Informant.DoesNotExist:
        return redirect('login')
    
      # Only fetch complaints for this informant if applicable
    

    context = {
        'complaints': complaints
    }
    return render(request, 'main/informant_page.html', context)

    # # If the user is a superuser and is the legal office, redirect them
    # if request.user.is_superuser and request.user.username == 'legal_admin':
    #     # Redirect to legal office dashboard or an access denied page
    #     return redirect('legal_office_page')  # Replace with your legal office dashboard URL name

    # # Otherwise, continue to show the Informant page
    # complaints = Complaint.objects.all()
    # context = {
    #     'complaints': complaints
    # }
    # return render(request, 'main/informant_page.html', context)


from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages

def logout_view(request):
    # Clear the user authentication and flush all session data
    logout(request)
    request.session.flush()  # Ensures full session reset
    messages.success(request, 'Logged out successfully.')
    return redirect('login')










# @login_required
# def profile_view(request):
#     # Get the logged-in informant's profile (assuming user has 1-1 relation with Informant)
#     informant = get_object_or_404(Informant, username=request.user.username)
#     return render(request, 'informant/profile.html', {'informant': informant})









def admin_page(request):
    complaints = Complaint.objects.all()

    return render(request, 'main/admin_page.html', {'complaints': complaints})




from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Complaint, Informant
from .utils import load_models

@csrf_exempt
def submit_complaint(request):
    informant_id = request.session.get('informant_id')
    if not informant_id:
        return JsonResponse({'error': 'User not logged in.'}, status=403)

    if request.method == 'POST':
        category = request.POST.get('category', '').strip()
        description = request.POST.get('description', '').strip()
         
        if not category or not description:
            return JsonResponse({'error': 'Category and Description are required.'}, status=400)


        # Check if description is provided
        if not description:
            return JsonResponse({'error': 'Description cannot be empty.'}, status=400)

        try:
            # Load the models (category_model, type_model, vectorizer)
            category_model, type_model, vectorizer = load_models()

            # Vectorize the description
            description_vec = vectorizer.transform([description])

            # Predict category and type
            predicted_category = category_model.predict(description_vec)[0]
            predicted_type = type_model.predict(description_vec)[0]

            # Retrieve the informant instance
            informant = Informant.objects.get(id=informant_id)

            # Save the complaint with the predicted category, type, and informant reference
            complaint = Complaint(
                informant=informant,              # Attach the logged-in informant to the complaint
                description=description,
                category=category,
                office=predicted_category,
                type=predicted_type,
                status='Pending',
                is_sent=False
            )
            complaint.save()

            # Return a success message to the AJAX call
            return JsonResponse({'message': 'Complaint submitted to the legal office successfully!'}, status=200)

        except Informant.DoesNotExist:
            return JsonResponse({'error': 'Informant not found.'}, status=403)

        except FileNotFoundError as e:
            # If the models could not be loaded due to file issues
            return JsonResponse({'error': f"Error loading models: {e}"}, status=500)

        except Exception as e:
            # Handle any other unforeseen exceptions
            return JsonResponse({'error': f"An unexpected error occurred: {e}"}, status=500)

    # Return an error for invalid request methods
    return JsonResponse({'error': 'Invalid request method.'}, status=400)

# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt

# @csrf_exempt
# def submit_complaint(request):
#     if request.method == 'POST':
#         description = request.POST.get('description', '').strip()

#         # Check if the description is empty
#         if not description:
#             return JsonResponse({'error': 'Description cannot be empty.'}, status=400)

#         try:
#             # Load the models
#             category_model, type_model, vectorizer = load_models()

#             # Vectorize the description
#             description_vec = vectorizer.transform([description])

#             # Predict category and type, along with similarity score
#             predicted_category = category_model.predict(description_vec)[0]
#             predicted_type = type_model.predict(description_vec)[0]
#             similarity_score = category_model.predict_proba(description_vec).max()  # Get the highest similarity score

#             # Set a similarity score threshold (for example, 0.5)
#             similarity_threshold = 0.5

#             # Check if the similarity score is below the threshold or no valid prediction made
#             if similarity_score < similarity_threshold:
#                 predicted_category = "Office not predicted"

#             # If the office is not predicted, do not send it to the legal office
#             if predicted_category == "Office not predicted":
#                 return JsonResponse({'message': 'Office not predicted. Complaint not submitted to legal office.'}, status=200)

#             # Save the complaint with the predicted office and type
#             complaint = Complaint(
#                 description=description,
#                 office=predicted_category,
#                 type=predicted_type,
#                 status='Pending',
#                 is_sent=False
#             )
#             complaint.save()

#             # Return a success message to the AJAX call
#             return JsonResponse({'message': f'Complaint submitted to legal office successfully!'}, status=200)

#         except FileNotFoundError as e:
#             return JsonResponse({'error': f"Error: {e}"}, status=500)

#         except Exception as e:
#             return JsonResponse({'error': f"An unexpected error occurred: {e}"}, status=500)

#     return JsonResponse({'error': 'Invalid request method.'}, status=400)


#legal Office
def legal_office_page(request):
    
    complaints = Complaint.objects.all()

    return render(request, 'main/legal_office_page.html', {'complaints': complaints})


from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Complaint  # Assuming your model is named Complaint

def update_office(request, complaint_id):
    if request.method == 'POST':
        complaint = get_object_or_404(Complaint, id=complaint_id)
        new_office = request.POST.get('office')
        if new_office:
            complaint.office = new_office
            complaint.save()
            messages.success(request, 'Office updated successfully.')
        else:
            messages.error(request, 'Please select a valid office.')
    return redirect('legal_office_page')  # Replace with the name of the view to redirect to


from django.views.decorators.http import require_POST

@require_POST
def update_type(request, complaint_id):
    complaint = get_object_or_404(Complaint, id=complaint_id)
    complaint.type = request.POST.get('type')
    complaint.save()
    return redirect(request.META.get('HTTP_REFERER', '/'))

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










from django.shortcuts import render
from .models import Complaint

def history_view(request):
    # Filter for solved reports
    solved_reports = Complaint.objects.filter(type="report", status="Solved")
    # Filter for solved complaints
    solved_complaints = Complaint.objects.filter(type="complaint", status="Solved")

    # Count solved reports by department
    report_counts = {
        'STCS': solved_reports.filter(office="STCS").count(),
        'SCJE': solved_reports.filter(office="SCJE").count(),
        'SAS': solved_reports.filter(office="SAS").count(),
        'SME': solved_reports.filter(office="SME").count(),
        'SOE': solved_reports.filter(office="SOE").count(),
        'SNHS': solved_reports.filter(office="SNHS").count(),
        'LHS': solved_reports.filter(office="LHS").count(),
        'STED': solved_reports.filter(office="STED").count(),
    }

    # Count solved complaints by department
    complaint_counts = {
        'STCS': solved_complaints.filter(office="STCS").count(),
        'SCJE': solved_complaints.filter(office="SCJE").count(),
        'SAS': solved_complaints.filter(office="SAS").count(),
        'SME': solved_complaints.filter(office="SME").count(),
        'SOE': solved_complaints.filter(office="SOE").count(),
        'SNHS': solved_complaints.filter(office="SNHS").count(),
        'LHS': solved_complaints.filter(office="LHS").count(),
        'STED': solved_complaints.filter(office="STED").count(),
    }

    context = {
        'report_counts': report_counts,
        'complaint_counts': complaint_counts,
    }

    return render(request, 'main/solved_statistic.html', context)


from django.core.exceptions import ObjectDoesNotExist
# Dashboard
def dashboard_page(request):
    try:
        # Check if the logged-in user has an associated office
        user_office = request.user.office
    except ObjectDoesNotExist:
        # Handle the case where there is no associated office for the informant
        user_office = None

    if user_office:
        # Fetch complaints only if the user has an associated office
        new_complaints = Complaint.objects.filter(office=user_office, is_new=True).exists()
    else:
        new_complaints = False  # Default value if there's no office

    context = {
        'new_complaints': new_complaints,
        # Other context data for reports/complaints
    }

    # Admin and Finance Office
    admin_finance_reports = Complaint.objects.filter(office="VP Administration and Finance", type="report")
    admin_finance_complaints = Complaint.objects.filter(office="VP Administration and Finance", type="complaint")
    admin_finance_solved_reports = admin_finance_reports.filter(status="Solved")
    admin_finance_solved_complaints = admin_finance_complaints.filter(status="Solved")
    admin_finance_pending_reports = admin_finance_reports.filter(status="Pending")
    admin_finance_pending_complaints = admin_finance_complaints.filter(status="Pending")
    admin_finance_inprogress_reports = admin_finance_reports.filter(status="In Progress")
    admin_finance_inprogress_complaints = admin_finance_complaints.filter(status="In Progress")

    # Academic Affairs Office
    academic_affairs_reports = Complaint.objects.filter(office="VP Academic Affairs", type="report")
    academic_affairs_complaints = Complaint.objects.filter(office="VP Academic Affairs", type="complaint")
    academic_affairs_solved_reports = academic_affairs_reports.filter(status="Solved")
    academic_affairs_solved_complaints = academic_affairs_complaints.filter(status="Solved")
    academic_affairs_pending_reports = academic_affairs_reports.filter(status="Pending")
    academic_affairs_pending_complaints = academic_affairs_complaints.filter(status="Pending")
    academic_affairs_inprogress_reports = academic_affairs_reports.filter(status="In Progress")
    academic_affairs_inprogress_complaints = academic_affairs_complaints.filter(status="In Progress")

    # Students Affairs Office
    students_affairs_reports = Complaint.objects.filter(office="VP Students and External Affairs", type="report")
    students_affairs_complaints = Complaint.objects.filter(office="VP Students and External Affairs", type="complaint")
    students_affairs_solved_reports = students_affairs_reports.filter(status="Solved")
    students_affairs_solved_complaints = students_affairs_complaints.filter(status="Solved")
    students_affairs_pending_reports = students_affairs_reports.filter(status="Pending")
    students_affairs_pending_complaints = students_affairs_complaints.filter(status="Pending")
    students_affairs_inprogress_reports = students_affairs_reports.filter(status="In Progress")
    students_affairs_inprogress_complaints = students_affairs_complaints.filter(status="In Progress")

    # GAD Office
    gad_office_reports = Complaint.objects.filter(office="GAD Office", type="report")
    gad_office_complaints = Complaint.objects.filter(office="GAD Office", type="complaint")
    gad_office_solved_reports = gad_office_reports.filter(status="Solved")
    gad_office_solved_complaints = gad_office_complaints.filter(status="Solved")
    gad_office_pending_reports = gad_office_reports.filter(status="Pending")
    gad_office_pending_complaints = gad_office_complaints.filter(status="Pending")
    gad_office_inprogress_reports = gad_office_reports.filter(status="In Progress")
    gad_office_inprogress_complaints = gad_office_complaints.filter(status="In Progress")

    # Legal Office - Aggregate data from the four offices
    legal_office_reports = Complaint.objects.filter(
        office__in=["VP Administration and Finance", "VP Academic Affairs", "VP Students and External Affairs", "GAD Office"], 
        type="report"
    )
    legal_office_complaints = Complaint.objects.filter(
        office__in=["VP Administration and Finance", "VP Academic Affairs", "VP Students and External Affairs", "GAD Office"], 
        type="complaint"
    )
    legal_office_solved_reports = legal_office_reports.filter(status="Solved")
    legal_office_solved_complaints = legal_office_complaints.filter(status="Solved")
    legal_office_pending_reports = legal_office_reports.filter(status="Pending")
    legal_office_pending_complaints = legal_office_complaints.filter(status="Pending")
    legal_office_inprogress_reports = legal_office_reports.filter(status="In Progress")
    legal_office_inprogress_complaints = legal_office_complaints.filter(status="In Progress")

    return render(request, 'main/dashboard_page.html', {
        # Admin and Finance Office Data
        'admin_finance_reports': admin_finance_reports.count(),
        'admin_finance_complaints': admin_finance_complaints.count(),
        'admin_finance_solved_reports': admin_finance_solved_reports.count(),
        'admin_finance_solved_complaints': admin_finance_solved_complaints.count(),
        'admin_finance_pending_reports': admin_finance_pending_reports.count(),
        'admin_finance_pending_complaints': admin_finance_pending_complaints.count(),
        'admin_finance_inprogress_reports': admin_finance_inprogress_reports.count(),
        'admin_finance_inprogress_complaints': admin_finance_inprogress_complaints.count(),

        # Academic Affairs Office Data
        'academic_affairs_reports': academic_affairs_reports.count(),
        'academic_affairs_complaints': academic_affairs_complaints.count(),
        'academic_affairs_solved_reports': academic_affairs_solved_reports.count(),
        'academic_affairs_solved_complaints': academic_affairs_solved_complaints.count(),
        'academic_affairs_pending_reports': academic_affairs_pending_reports.count(),
        'academic_affairs_pending_complaints': academic_affairs_pending_complaints.count(),
        'academic_affairs_inprogress_reports': academic_affairs_inprogress_reports.count(),
        'academic_affairs_inprogress_complaints': academic_affairs_inprogress_complaints.count(),

        # Students Affairs Office Data
        'students_affairs_reports': students_affairs_reports.count(),
        'students_affairs_complaints': students_affairs_complaints.count(),
        'students_affairs_solved_reports': students_affairs_solved_reports.count(),
        'students_affairs_solved_complaints': students_affairs_solved_complaints.count(),
        'students_affairs_pending_reports': students_affairs_pending_reports.count(),
        'students_affairs_pending_complaints': students_affairs_pending_complaints.count(),
        'students_affairs_inprogress_reports': students_affairs_inprogress_reports.count(),
        'students_affairs_inprogress_complaints': students_affairs_inprogress_complaints.count(),

        # GAD Office Data
        'gad_office_reports': gad_office_reports.count(),
        'gad_office_complaints': gad_office_complaints.count(),
        'gad_office_solved_reports': gad_office_solved_reports.count(),
        'gad_office_solved_complaints': gad_office_solved_complaints.count(),
        'gad_office_pending_reports': gad_office_pending_reports.count(),
        'gad_office_pending_complaints': gad_office_pending_complaints.count(),
        'gad_office_inprogress_reports': gad_office_inprogress_reports.count(),
        'gad_office_inprogress_complaints': gad_office_inprogress_complaints.count(),

        # Legal Office (Aggregate of all four offices)
        'legal_office_reports': legal_office_reports.count(),
        'legal_office_complaints': legal_office_complaints.count(),
        'legal_office_solved_reports': legal_office_solved_reports.count(),
        'legal_office_solved_complaints': legal_office_solved_complaints.count(),
        'legal_office_pending_reports': legal_office_pending_reports.count(),
        'legal_office_pending_complaints': legal_office_pending_complaints.count(),
        'legal_office_inprogress_reports': legal_office_inprogress_reports.count(),
        'legal_office_inprogress_complaints': legal_office_inprogress_complaints.count(),
    })

from django.shortcuts import render
from .models import Complaint

# Admin and Finance Office Dashboard
def admin_finance_dashboard(request):
    reports = Complaint.objects.filter(office="VP Administration and Finance", type="report", is_sent=True)
    complaints = Complaint.objects.filter(office="VP Administration and Finance", type="complaint", is_sent=True)

    context = {
        'reports': reports.count(),
        'complaints': complaints.count(),
        'solved_reports': reports.filter(status="Solved").count(),
        'solved_complaints': complaints.filter(status="Solved").count(),
        'pending_reports': reports.filter(status="Pending").count(),
        'pending_complaints': complaints.filter(status="Pending").count(),
        'inprogress_reports': reports.filter(status="In Progress").count(),
        'inprogress_complaints': complaints.filter(status="In Progress").count(),
    }
    return render(request, 'offices/admin_finance_dashboard.html', context)

# Academic Affairs Office Dashboard
def academic_affairs_dashboard(request):
    reports = Complaint.objects.filter(office="VP Academic Affairs", type="report", is_sent=True)
    complaints = Complaint.objects.filter(office="VP Academic Affairs", type="complaint", is_sent=True)

    context = {
        'reports': reports.count(),
        'complaints': complaints.count(),
        'solved_reports': reports.filter(status="Solved").count(),
        'solved_complaints': complaints.filter(status="Solved").count(),
        'pending_reports': reports.filter(status="Pending").count(),
        'pending_complaints': complaints.filter(status="Pending").count(),
        'inprogress_reports': reports.filter(status="In Progress").count(),
        'inprogress_complaints': complaints.filter(status="In Progress").count(),
    }
    return render(request, 'offices/academic_affairs_dashboard.html', context)

# Students Affairs Office Dashboard
def students_affairs_dashboard(request):
    reports = Complaint.objects.filter(office="VP Students and External Affairs", type="report", is_sent=True)
    complaints = Complaint.objects.filter(office="VP Students and External Affairs", type="complaint", is_sent=True)

    context = {
        'reports': reports.count(),
        'complaints': complaints.count(),
        'solved_reports': reports.filter(status="Solved").count(),
        'solved_complaints': complaints.filter(status="Solved").count(),
        'pending_reports': reports.filter(status="Pending").count(),
        'pending_complaints': complaints.filter(status="Pending").count(),
        'inprogress_reports': reports.filter(status="In Progress").count(),
        'inprogress_complaints': complaints.filter(status="In Progress").count(),
    }
    return render(request, 'offices/students_affairs_dashboard.html', context)

# GAD Office Dashboard
def gad_dashboard(request):
    reports = Complaint.objects.filter(office="GAD Office", type="report", is_sent=True)
    complaints = Complaint.objects.filter(office="GAD Office", type="complaint", is_sent=True)

    # Filter for complaints that contain "sexual harassment" in the description
    sensitive_complaints = complaints.filter(description__icontains="sexual harassment")
    sensitive_complaints_count = sensitive_complaints.count()

    # For debugging: Log details about the sensitive complaints
    print("Sensitive Complaints Count:", sensitive_complaints_count)
    for complaint in sensitive_complaints:
        print("Complaint ID:", complaint.id, "Description:", complaint.description)

    context = {
        'reports': reports.count(),
        'complaints': complaints.count(),
        'solved_reports': reports.filter(status="Solved").count(),
        'solved_complaints': complaints.filter(status="Solved").count(),
        'pending_reports': reports.filter(status="Pending").count(),
        'pending_complaints': complaints.filter(status="Pending").count(),
        'inprogress_reports': reports.filter(status="In Progress").count(),
        'inprogress_complaints': complaints.filter(status="In Progress").count(),
        'sensitive_complaints_count': sensitive_complaints_count,   # Add sensitive complaints count

        
    }
    return render(request, 'offices/gad_dashboard.html', context)




    

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

            # Generate and save the updated PDF after updating urgency
            pdf_content = complaint.generate_pdf()
            complaint.pdf_file.save(f"complaint_{complaint.id}_description.pdf", pdf_content)
    
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
        {'office': 'LHS', 'status': 'Solved'},
        {'office': 'STED', 'status': 'Pending'},
        {'office': 'STCS', 'status': 'Solved'},
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







from django.shortcuts import render
from django.db.models import Count
from .models import Complaint, Informant  # Import necessary models
import json

def solved_reports_complaints_view(request):
    # Get the logged-in user's department
    user_department = request.user.get_department_display if request.user.is_authenticated else None

    # Check if the department exists; otherwise, show an empty response or redirect as needed
    if not user_department:
        return render(request, 'offices/gad_history.html', {'error': 'No department found for the user.'})

    # Get solved reports and complaints only for the user's department
    solved_reports_count = Complaint.objects.filter(
        office=user_department, type='report', status='Solved'
    ).count()
    solved_complaints_count = Complaint.objects.filter(
        office=user_department, type='complaint', status='Solved'
    ).count()

    # Prepare context data
    context = {
        'departments_json': json.dumps([user_department]),  # Single department
        'solved_reports_json': json.dumps([solved_reports_count]),
        'solved_complaints_json': json.dumps([solved_complaints_count]),
    }
    return render(request, 'offices/gad_history.html', context)



# # appss/views.py

# from django.shortcuts import render
# from .models import Office  # Assuming you have an Office model

# def chat_room(request):
#     offices = Office.objects.all()  # Fetch all office instances
#     return render(request, 'appss/complaint_message.html', {
#         'offices': offices,
#     })










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




from django.shortcuts import render, redirect, get_object_or_404
from .models import Complaint, Response
from reportlab.pdfgen import canvas
from io import BytesIO

def submit_response(request):
    if request.method == 'POST':
        complaint_id = request.POST.get('complaint_id')
        complaint_id = request.POST.get('complaint_id')
        letter_content = request.POST.get('letter_content')

        # Fetch the complaint object
        complaint = get_object_or_404(Complaint, id=complaint_id)

        # Generate PDF for the response
        response_pdf = generate_pdf(letter_content)

        # Create a new Response object
        response = Response(complaint=complaint, letter_content=letter_content)
        response.response_pdf.save(f"response_{complaint_id}_{response.id}.pdf", response_pdf)
        response.save()

        # Redirect to the complaint message page
        return redirect('complaint_message', complaint_id=complaint.id)

def generate_pdf(content):
    buffer = BytesIO()
    p = canvas.Canvas(buffer)

    # Add content to PDF
    p.drawString(100, 750, "Office Response Letter")
    p.drawString(100, 730, content)

    p.showPage()
    p.save()

    buffer.seek(0)
    return buffer

def complaint_message(request, complaint_id):
    complaint = get_object_or_404(Complaint, id=complaint_id)
    responses = complaint.responses.all()  # Fetch all responses for this complaint
    return render(request, 'informant/complaint_message.html', {'complaint': complaint, 'responses': responses})



from django.shortcuts import redirect, get_object_or_404
from .models import Response  # Adjust based on your actual model

def delete_response(request, response_id):
    if request.method == 'POST':
        response = get_object_or_404(Response, id=response_id)  # Assuming you have a Response model
        complaint_id = response.complaint.id  # Get the associated complaint ID
        response.delete()  # Delete the response
        return redirect('complaint_message', complaint_id=complaint_id)  # Redirect back to the complaint message





from django.shortcuts import render
from .models import Complaint

def solved_cases_by_department(request):
    # List of departments to display data for
    departments = ['STCS', 'SCJE', 'SAS', 'SME', 'SOE', 'SNHS', 'LHS', 'STED']
    solved_data = {
        'departments': departments,
        'solvedComplaints': []
    }

    # Query the count of solved complaints for each department
    for dept in departments:
        solved_complaints_count = Complaint.objects.filter(department=dept, status='solved').count()
        solved_data['solvedComplaints'].append(solved_complaints_count)

    # Render the template with the solved complaints data
    return render(request, 'offices/gad_history.html', {'solved_data': solved_data})





from django.shortcuts import render
from .models import Complaint

# View to report complaints matching the keywords
def complaint_report(request):
    # Get the count of complaints with keywords
    complaints_count = Complaint.count_complaints_with_keywords()

    # Optionally, you could also display the complaints themselves
    complaints = Complaint.objects.filter(
        message__icontains__any=Complaint.keywords
    )

    # Pass the count and the complaints to the template
    context = {
        'complaints_count': complaints_count,
        'complaints': complaints  # List of complaints containing the keywords
    }
    return render(request, 'main/complaint_report.html', context)




from django.http import JsonResponse
from django.shortcuts import render
from .models import Complaint  # Ensure Complaint is imported
from .forms import Incident

def incident_filter(request):
    return render(request, 'legal/legal_history.html')



def complaint_counts(request):
    office = request.GET.get('office')
    department = request.GET.get('department')

    # Filter complaints based on office and department if provided
    complaints = Complaint.objects.all()
    if office:
        complaints = complaints.filter(office=office)
    if department:
        complaints = complaints.filter(informant__department=department)  # Ensure informant__department is correct

    # Count the reports and complaints
    reports_count = complaints.filter(type='report').count()
    complaints_count = complaints.filter(type='complaint').count()

    # Count complaints based on specific categories
    category_counts = {}
    categories = [
    'Sexual Harassment', 'Sexual Assault', 'Bullying', 'Discrimination', 
    'Abuse', 'Violence', 'Gender Equality', 'Defamation', 'Rape', 
    'Scholarship Issues', 'Late Fees', 'Financial Aid', 'Staff Payment Issues', 'Billing Errors', 
    'Tardiness', 'Always Late', 'Favoritism', 'Always Absent', 'Unfair Grading', 'Unprofessional Behavior', 
    'Student Misconduct', 'Student Welfare', 'Student Engagement', 'Student Rights'
]

    for category in categories:
        category_count = complaints.filter(category=category).count()
        category_counts[category] = category_count

    # Return the counts as JSON response
    return JsonResponse({
        'reports': reports_count,
        'complaints': complaints_count,
        'category_counts': category_counts
    })
