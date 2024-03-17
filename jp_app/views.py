from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import *
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.shortcuts import get_object_or_404
from datetime import date
from datetime import datetime, timedelta
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.db.models import Count
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings





def clear_msg(request):
    # Clear the message from the session
    request.session.pop('msg', None)
    return JsonResponse({'status': 'success'})

def user_logout(request):
    del request.session['email']
    del request.session['user_type']
    user_type = 'None'
    return render(request, "index.html", {'user_type': user_type})

# def req_login(request):
#     alert_message = None

#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')

#         user = authenticate(request, username=email, password=password)

#         if user is not None and user.is_active:
#             # User is authenticated and active
#             login(request, user)

#             user_type = user.first_name

#             if user_type in ['AD', 'EM', 'ST', 'AP']:
#                 request.session['email'] = email
#                 request.session['user_type'] = user_type
#                 return redirect('index')
#         else:
#             alert_message = "Invalid user or inactive account"

#     # Pass the alert message to the template
#     return render(request, "login.html", {'user_type': 'None', 'alert_message': alert_message})





def req_login(request):
    alert_message = None

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if email == "admin@gmail.com" and password == "admin":
            email = "admin@gmail.com"  # Ensure consistent email for session
            user_type = 'AD'
            request.session['email'] = email
            request.session['user_type'] = user_type
            return render(request, "index.html", {'user_type': user_type, 'email': email})
       
        else:       

            try:
                user = User.objects.get(username=email)
            except User.DoesNotExist:
                alert_message = "No such account. Please register first."
                return render(request, "login.html", {'user_type': 'None', 'alert_message': alert_message})

            # Check if the provided password is correct
            user = authenticate(request, username=email, password=password)

            if user is not None:
                # User is authenticated and active
                    login(request, user)

                    user_type = user.first_name
                    status = user.last_name
                    if status=='0':
                        alert_message = "Inactive account. Please contact the administrator."
                        return render(request, "login.html", {'user_type': 'None', 'alert_message': alert_message})
                    
                    elif status=='1':
                        if user_type in ['AD', 'EM', 'ST', 'AP']:
                            request.session['email'] = email
                            request.session['user_type'] = user_type
                            return render(request, "index.html", {'user_type': user_type, 'email': email})
                    
            else:
                alert_message = "Incorrect password. Please verify and attempt again."
                return render(request, "login.html", {'user_type': 'None', 'alert_message': alert_message})

    # Pass the alert message to the template
    return render(request, "login.html", {'user_type': 'None', 'alert_message': alert_message})

    


# def req_login(request):
#     # alert_message = None

#         if request.method == 'POST':
#          email = request.POST.get('email')
#          user_type = 'AD'
#         request.session['user_type'] = user_type
#         return render(request, "index.html", {'user_type': user_type, 'email': email})
#             # return render(request, "index.html", {'user_type': user_type, 'email': email})
        

def index(request):
    #if seession is not available
    if 'email' not in request.session:
        user_type = 'None'
        return render(request, "index.html", {'user_type': user_type})
    #if session is available
    else:
        #session is available
        # request.session['email'] = email
        # request.session['user_type'] = user_type
        user_type = request.session['user_type']
        email = request.session['email']
        return render(request, "index.html", {'user_type': user_type, 'email': email})

def login_view(request):
    return render(request,"login.html")

def signin(request):
    return render(request,"signin.html")

# def select_user(request):
#     return render(request,"select_user.html")


def index1(request):
    #if seession is not available
    if 'email' not in request.session:
        user_type = 'None'
        return render(request, "index.html", {'user_type': user_type})
    #if session is available
    else:
        #session is available
        # request.session['email'] = email
        # request.session['user_type'] = user_type
        user_type = request.session['user_type']
        email = request.session['email']
        return render(request, "index.html", {'user_type': user_type, 'email': email})

def login_view(request):
    return render(request,"login.html")

def signin(request):
    return render(request,"signin.html")

# def select_user(request):
#     return render(request,"select_user.html")




# admin_page
def admin_page(request):
    load_app=Applicant.objects.count()
    load_emp=Employer.objects.count()
    load_staff=Staff.objects.count()
    load_jobs=Job.objects.count()
    load_events=Event.objects.count()
    load_applications=Job_application.objects.count()
    load_plans=Plan.objects.filter(Plan_Status=True).count()
    today = date.today()
    load_subscriptions=Payment.objects.filter(Expiry_Date__gt=today).count()
    # users_sessions
    user_type = request.session['user_type']
    return render(request,"admin.html",{'send_app':load_app,'send_emp':load_emp,'send_staff':load_staff,'send_job':load_jobs,'user_type':user_type,'send_events':load_events,'send_job_app': load_applications,'send_plans':load_plans,'send_subscriptions':load_subscriptions})


#emp_dashboard
# def emp_dashboard(request):
#     user_type = request.session['user_type']
#     load_jobs=Job.objects.filter(EM_Username=request.session['email']).count()
#     email = request.session['email']
#     employer_instance = Employer.objects.get(Emp_Username=email)
#     employer_id = employer_instance.id
#     emp_id = Employer.objects.get(id=employer_id)
#     job_ids = Job.objects.filter(Employer_id=emp_id).values_list('id', flat=True)
#     job_applications = Job_application.objects.filter(Job_ID__in=job_ids).order_by('id')
#     ratings = Review.objects.filter(Reviewee_ID=emp_id).order_by('id')
#     foreach_rating in ratings:
#         rating = rating+foreach_rating.Ratings
#     job_applications_count = Job_application.objects.filter(Job_ID__in=job_ids).count()

#     return render(request,"emp_dashboard.html",{'user_type':user_type,'send_job':load_jobs,'job_applications_count':job_applications_count})




#emp_dashboard
def emp_dashboard(request):
    user_type = request.session['user_type']
    load_jobs = Job.objects.filter(EM_Username=request.session['email']).count()
    email = request.session['email']
    employer_instance = Employer.objects.get(Emp_Username=email)
    employer_id = employer_instance.id
    emp_id = Employer.objects.get(id=employer_id)
    job_ids = Job.objects.filter(Employer_id=emp_id).values_list('id', flat=True)
    job_applications = Job_application.objects.filter(Job_ID__in=job_ids).order_by('id')
    ratings = Review.objects.filter(Reviewee_ID=emp_id).order_by('id')
    # Fix: Initialize rating before using it in the loop
    rating = 0
    
    for each_rating in ratings:
        rating += each_rating.Ratings
    
    job_applications_count = Job_application.objects.filter(Job_ID__in=job_ids).count()

    return render(request, "emp_dashboard.html", {'user_type': user_type, 'send_job': load_jobs, 'job_applications_count': job_applications_count, 'ratings': rating})

















# #vaccancies
# def vaccancies(request):
#     email = request.session.get('email', '')
#     # Load vacancies where EM_Username is equal to the email from the session
#     load_jobs = Job.objects.filter(EM_Username=email).order_by('id')
#     return render(request,"vaccancies.html",{'send_jobs':load_jobs})

def vaccancies(request):
    email = request.session.get('email', '')
    # Load vacancies where EM_Username is equal to the email from the session
    load_jobs = Job.objects.filter(EM_Username=email).order_by('id')

    # For demonstration purposes, we'll take the first job from the queryset
    if load_jobs.exists():
        job = load_jobs.first()
        job_app_count = Job_application.objects.filter(Job_ID=job).count()

        # Prepare a single item array with separate values
        single_job_data = [{
            'job_id': job.id,
            'job_title': job.Job_Title,
            'job_mode': job.Job_Mode,
            'job_location': job.Job_Location,
            'job_city': job.Job_City,
            'job_state': job.Job_State,
            'job_seats': job.Job_Seats,
            'job_time_type': job.Job_Time_Type,
            'job_duration': job.Job_Duration,
            'job_start': job.Job_Start,
            'job_end': job.Job_End,
            'min_job_days': job.Min_Job_Days,
            'job_day_type': job.Job_Day_Type,
            'job_app_end': job.Job_App_End,
            'job_description': job.Job_Description,
            'job_status': job.Job_Status,
            'job_app_count': job_app_count,
        }]
    else:
        single_job_data = []  # Empty array if no jobs are available

    return render(request, "vaccancies.html", {'job_data': single_job_data})


#view_all_jobs
def view_all_jobs(request):
    load_jobs = Job.objects.all().order_by('id')
    user_type = request.session['user_type']
    today = date.today()
    return render(request,"all_vaccancies.html",{'send_jobs':load_jobs,'user_type':user_type,'today':today})

# list all jobs in home page
# list all jobs in home page
# list all jobs in home page
def list_jobs(request):
    jobs_with_images = []

    jobs = Job.objects.filter(Job_Seats__gt=0,Job_Status=True,Job_App_End__gte=timezone.now())

    for job in jobs:
        email = job.EM_Username
        employer = Employer.objects.filter(Emp_Username=email).first()
        employer_id = employer.id
        emp_id = Employer.objects.get(id=employer_id)
        job_ids = Job.objects.filter(Employer_id=emp_id,Job_Status=True).values_list('id', flat=True)
        job_applications = Job_application.objects.filter(Job_ID__in=job_ids).order_by('id')
        ratings = Review.objects.filter(Reviewee_ID=emp_id).order_by('id')
        # Fix: Initialize rating before using it in the loop
        rating = 0
    
        for each_rating in ratings:
            rating += each_rating.Ratings

        plan = 'no_plan'

        # Check if employer exists
        if employer:
            job_with_image = {
                'id': job.id,
                'EM_Username': job.EM_Username,
                'Job_Title': job.Job_Title,
                'Job_Mode': job.Job_Mode,
                'Job_Location': job.Job_Location,
                'Job_Seats': job.Job_Seats,
                'Job_Time_Type': job.Job_Time_Type,
                'Job_Duration': job.Job_Duration,
                'Job_Start': job.Job_Start,
                'Job_End': job.Job_End,
                'Min_Job_Days': job.Min_Job_Days,
                'Job_Day_Type': job.Job_Day_Type,
                'Job_App_End': job.Job_App_End,
                'Job_Description': job.Job_Description,
                'Job_City': job.Job_City,
                'Job_State': job.Job_State,
                'Job_Status': job.Job_Status,
                'emp_image': employer.Emp_Image,  # Assuming Emp_image stores only the filename
                'ratings': rating
            }
            jobs_with_images.append(job_with_image)

    context = {
        'jobs_with_images': jobs_with_images
    }

    user_type = request.session.get('user_type', 'None')
    email = request.session.get('email', 'None')

    # Check if the user is an applicant
    if user_type == 'AP':
        applicant_id = Applicant.objects.filter(App_Username=email).values_list('id', flat=True).first()
        if applicant_id:
            today = date.today()
            payment_id = Payment.objects.filter(Applicant_ID=applicant_id,Expiry_Date__gt=today).first()
            if payment_id:
                # extract the plan id
                plan_id = payment_id.Plan_ID.id
                # extract the plan details
                plan = Plan.objects.filter(id=plan_id).first()
                plan_level = plan.Plan_Level 
                plan=plan_level   

  
    return render(request, 'jobs.html', {'user_type': user_type, 'email': email, 'jobs_with_images': jobs_with_images, 'plan': plan})



def manage_events(request):
    load_events = Event.objects.all().order_by('id')
    user_type = request.session['user_type']
    return render(request,"list_events.html",{'send_events':load_events,'user_type':user_type})

def add_event(request):
    user_type = request.session['user_type']
    email = request.session['email']
    return render(request,"add_event.html",{'user_type':user_type,'email':email})


def reg_event(request):
    if request.method == 'POST':
        event_title = request.POST.get('event_title')
        event_organizer = request.POST.get('event_organizer')
        event_venue = request.POST.get('event_venue')
        event_street = request.POST.get('event_street')
        event_dist = request.POST.get('event_dist')
        event_state = request.POST.get('event_state')
        event_email = request.POST.get('event_email')
        event_phone = request.POST.get('event_phone')
        event_date = request.POST.get('date')
        event_time = request.POST.get('time')
        staff_email = request.POST.get('staff_email')
        event_description = request.POST.get('event_description')
        event = Event.objects.create(
            Staff_ID=Staff.objects.get(Staff_Username=staff_email),
            Staff_Username=staff_email,
            Event_Title=event_title,
            Event_Organizer=event_organizer,
            Event_Venue=event_venue,
            Event_Street=event_street,
            Event_Dist=event_dist,
            Event_State=event_state,
            Event_Email=event_email,
            Event_Phone=event_phone,
            Event_Date=event_date,
            Event_Time=event_time,
            Event_Description=event_description,
            Event_Status=True
        )
        event.save()
        request.session['msg'] = "Event added successfully"
        return render(request, "admin.html")


# staff_page
def staff_page(request):
    return render(request,"staff.html")

# add_staff
def add_staff(request):
     return render(request,"add_staff.html")



def select_user(request):
    if request.method == 'POST':
        user_type = request.POST.get('category')
        if user_type == '1':
            return redirect('applicant_page')  # Redirect to applicant page
        elif user_type == '2':
            return redirect('employer_page')  


def employer_page(request):
    return render(request,"employer_signin.html")

def applicant_page(request):
    return render(request,"applicant_signin.html")



 

def staff_list(request):
    # load_staff from user table with first_name = 'ST'
    load_staff_users = User.objects.filter(first_name='ST').order_by('id')
    
    array = []
    
    for staff_user in load_staff_users:
        staff_username = staff_user.username
        
        
        # Use filter instead of get to handle potential multiple results
        load_staff_detail = Staff.objects.filter(Staff_Username=staff_username).first()
        
        if load_staff_detail:
            staff_details = {
                'id': load_staff_detail.id,
                'Staff_Username': load_staff_detail.Staff_Username,
                'Staff_Fname': load_staff_detail.Staff_Fname,
                'Staff_Lname': load_staff_detail.Staff_Lname,
                'Staff_Phone': load_staff_detail.Staff_Phone,
                'Staff_DOB': load_staff_detail.Staff_DOB,
                'Staff_Hname': load_staff_detail.Staff_Hname,
                'Staff_Gender': load_staff_detail.Staff_Gender,
                'Staff_Street': load_staff_detail.Staff_Street,
                'Staff_Dist': load_staff_detail.Staff_Dist,
                'Staff_Pin': load_staff_detail.Staff_Pin,
                'Staff_Date': load_staff_detail.Staff_Date,
                'is_active': staff_user.last_name,
            }
            array.append(staff_details)

    user_type = request.session.get('user_type', None)
    return render(request, "staff_list.html", {'send_list': array, 'user_type': user_type})


#     # Retrieve staff excluding the one with id=2
#     load_staff = Staff.objects.exclude(id=1).order_by('id')
#     # Fetch user_type from the session
#     user_type = request.session['user_type']
#     # Create a list to store staff details along with is_active value
#     staff_with_is_active = []
#     # Fetch all details of each staff member along with is_active value
#     for staff_member in load_staff:
#         staff_details = {
#             'id': staff_member.id,
#             'Staff_Username': staff_member.Staff_Username,
#             'Staff_Fname': staff_member.Staff_Fname,
#             'Staff_Lname': staff_member.Staff_Lname,
#             'Staff_Phone': staff_member.Staff_Phone,
#             'Staff_DOB': staff_member.Staff_DOB,
#             'Staff_Hname': staff_member.Staff_Hname,
#             'Staff_Gender': staff_member.Staff_Gender,
#             'Staff_Street': staff_member.Staff_Street,
#             'Staff_Dist': staff_member.Staff_Dist,
#             'Staff_Pin': staff_member.Staff_Pin,
#             'Staff_Date': staff_member.Staff_Date,
#             'is_active': staff_member.uid.last_name,
#         }
#         staff_with_is_active.append(staff_details)

#     return render(request, "staff_list.html", {'send_list': staff_with_is_active, 'user_type': user_type})



def reg_new_applicant(request):
    if request.method == 'POST':
        firstName = request.POST.get('firstName')
        lastName = request.POST.get('lastName')
        email = request.POST.get('email')
        phoneNumber = request.POST.get('phoneNumber')
        gender = request.POST.get('gender')
        dob = request.POST.get('dob')
        education = request.POST.get('education')
        employment = request.POST.get('employment')
        linkedin = request.POST.get('linkedin')
        street = request.POST.get('street')
        profilephoto = request.FILES['profilePhoto']
        resume= request.FILES['resume']
        houseName = request.POST.get('houseName')
        district = request.POST.get('district')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
        passwordright = request.POST.get('passwordright')
        passwordleft = request.POST.get('passwordleft')

        fs=FileSystemStorage()
        filename=fs.save(profilephoto.name,profilephoto)
        filename=fs.save(resume.name,resume)

        # if email already exists return to same page
        if User.objects.filter(username=email).exists():
            messages.info(request, "Email already exists")
            return redirect('applicant_page')

        if passwordright != passwordleft:
            messages.info(request, 'Password doesn\'t match')

            return render(request,"applicant_page")
        u=User.objects.create_user(username=email,password=passwordleft,first_name='AP',last_name=1)
        u.save()

        applicant = Applicant.objects.create(uid=u,App_Username=email,App_Fname=firstName,App_Lname=lastName,App_Phone=phoneNumber,
            App_DOB=dob,App_Education=education,App_Emp_Status=employment,
            App_LinkedIn=linkedin,App_Image=profilephoto,App_Hname=houseName,App_Gender=gender,
            App_Street=street,App_Dist=district,App_Pin=pincode,App_Date=timezone.now(),App_Resume=resume,
            App_Status=True
        )
        applicant.save()

        request.session['email'] = email
        request.session['user_type'] = 'AP'
    
        # request.session['msg']= "Applicant registered successfully"
    messages.success(request, "Applicant Registered Successfully")
    return redirect('index')






def reg_new_employer(request):
    if request.method == 'POST':
        firmName = request.POST.get('firmName')
        email = request.POST.get('email')
        firm_logo = request.FILES['logo']
        phoneNumber = request.POST.get('phoneNumber')
        street = request.POST.get('street')
        district = request.POST.get('district')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
        passwordright = request.POST.get('passwordright')
        passwordleft = request.POST.get('passwordleft')
        fs = FileSystemStorage()
        filename = fs.save(firm_logo.name, firm_logo) 
        # if email already exists return error
        if User.objects.filter(username=email).exists():
            messages.info(request, "Email already exists")
            return render(request, "login.html")

        if passwordright != passwordleft:
            messages.info(request, 'Password doesn\'t match')
            return render(request,"index.html")     
        u=User.objects.create_user(username=email,password=passwordleft,first_name='EM',last_name=1)
        u.save()

        employer = Employer.objects.create(uid=u,Emp_Username=email,Emp_Firm=firmName,Emp_Image=firm_logo,Emp_Phone=phoneNumber,
            Emp_Street=street,Emp_Dist=district,Emp_State=state,Emp_Pin=pincode,Emp_Date=timezone.now(),Emp_Status=True
        )
        employer.save()
        # request.session['msg']= "Employer registered successfully"
        messages.success(request, "Employer Registered Successfully")
        #set session
        user_type = 'EM'
        request.session['email'] = email
        request.session['user_type'] = user_type
        return render(request, "index.html", {'user_type': user_type, 'email': email})

def edit_emp(request,id):
    emp=Employer.objects.get(id=id)
    return render(request,"edit_emp.html",{'send_data':emp})

def update_emp(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        firmName = request.POST.get('firmName')
        phoneNumber = request.POST.get('phoneNumber')
        street = request.POST.get('street')
        district = request.POST.get('district')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')

        if 'logo' in request.FILES and request.FILES['logo']:
            # If a new logo is provided, save it
            firm_logo = request.FILES['logo']
            fs = FileSystemStorage()
            filename = fs.save(firm_logo.name, firm_logo)
            Employer.objects.filter(id=id).update(Emp_Firm=firmName,Emp_Image=firm_logo,Emp_Phone=phoneNumber,Emp_Street=street,Emp_Dist=district,Emp_State=state,Emp_Pin=pincode)
        
        else:
            # If no new logo is provided, update the other fields
            Employer.objects.filter(id=id).update(Emp_Firm=firmName,Emp_Phone=phoneNumber,Emp_Street=street,Emp_Dist=district,Emp_State=state,Emp_Pin=pincode)
        
        messages.success(request, "Employer Updated Successfully")
        return redirect('employer')


def reg_staff(request):
    if request.method == 'POST':
        firstName = request.POST.get('firstName')
        lastName = request.POST.get('lastName')
        email = request.POST.get('email')
        phoneNumber = request.POST.get('phoneNumber')
        gender = request.POST.get('gender')
        dob = request.POST.get('dob')
        houseName = request.POST.get('houseName')
        street = request.POST.get('street')
        district = request.POST.get('district')
        pincode = request.POST.get('pincode')
        passwordright = request.POST.get('passwordright')
        passwordleft = request.POST.get('passwordleft')

        # if email already exists return error
        if User.objects.filter(username=email).exists():
            messages.info(request, "Email already exists")
            return render(request, "login.html")

        if passwordright != passwordleft:
            messages.info(request,"Password doesn't match")
            return render(request,"index.html")
        u=User.objects.create_user(username=email,password=passwordleft,first_name='ST',last_name=1)    
        u.save()

        staff = Staff.objects.create(uid=u,Staff_Username=email,Staff_Fname=firstName,Staff_Lname=lastName,Staff_Phone=phoneNumber,
            Staff_DOB=dob,Staff_Gender=gender,Staff_Hname=houseName,Staff_Street=street,Staff_Dist=district,Staff_Pin=pincode,Staff_Date=timezone.now(),Staff_Status=True
        )
        staff.save()
    
        request.session['msg']= "Staff registered successfully"
        messages.success(request, "Staff Registered Successfully")
        return render(request,"admin.html")

def add_job(request):
    return render(request,"add_vaccancy.html")


def reg_job(request):
    if request.method == 'POST':
        jobTitle = request.POST.get('firstName')
        location = request.POST.get('location')
        timing = request.POST.get('timing')
        commencement = request.POST.get('commencement')
        workdays = request.POST.get('workdays')
        deadline = request.POST.get('deadline')
        description = request.POST.get('description')
        mode = request.POST.get('mode')
        vaccancies = request.POST.get('vaccancies')
        worktime = request.POST.get('worktime')
        completion = request.POST.get('completion')
        workdaytype = request.POST.get('workdaytype')
        city = request.POST.get('city')
        state= request.POST.get('state')

        if request.session['user_type'] == 'EM':
            email = request.session['email']
            # Rest of your code remains the same
            employer_instance = Employer.objects.get(Emp_Username=email)
            employer_id = employer_instance.id
            emp_id = Employer.objects.get(id=employer_id)

            job = Job.objects.create(
            Employer_id=emp_id,
            EM_Username=email,
            Job_Title=jobTitle,
            Job_Mode=mode,
            Job_Location=location,
            Job_Seats=vaccancies,
            Job_Time_Type=timing,
            Job_Duration=worktime,
            Job_Start=commencement,
            Job_End=completion,
            Min_Job_Days=workdays,
            Job_Day_Type=workdaytype,
            Job_App_End=deadline,
            Job_City=city,
            Job_State=state,
            Job_Description=description,
            Job_Status=True
            )
            job.save()
            
            messages.success(request, "Job Updated Successfully")
            return redirect('emp_dashboard')
        else:
            request.session['msg'] = "You are not authorized to add a job"
            return render(request, "vaccancies.html")



# apply jobs
def apply_jobs(request):    
    if request.method == 'POST':
        job_ID = request.POST.get('job_id')
        email = request.session['email']
        
        applicant_instance = Applicant.objects.get(App_Username=email)
        applicant_id = applicant_instance.id
        app_id = Applicant.objects.get(id=applicant_id)

        job_instance = Job.objects.get(id=job_ID)
        job_id1 = job_instance.id
        job_id2 = Job.objects.get(id=job_id1)

        # check if the applicant has already applied for the job
        job_application = Job_application.objects.filter(Job_ID=job_id2, Job_Applicant_ID=app_id).first()
        if job_application:
            # request.session['job_msg'] = "Sorry! You have already applied for this job."
            messages.success(request, "Sorry! You have already applied for this job.")
            # return render(request, "jobs.html", {'user_type': 'AP', 'email': email})
            return redirect('list_jobs')
        else:
            job_application = Job_application.objects.create(
                Job_ID=job_id2,
                Job_Applicant_ID=app_id,
                Job_App_Date=timezone.now(),
                Job_App_Status='Applied'
            )
            job_application.save()
            # request.session['job_msg'] = "Job applied successfully."
            messages.success(request, "Job applied successfully.")
            return redirect('list_jobs')
            # return render(request, "jobs.html", {'user_type': 'AP', 'email': email})
    else:
        return render(request, "index.html", {'user_type': 'AP', 'email': email})
    

def calculate_age(birthdate):
    today = date.today()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    return age



def view_application(request, job_id):
    job_applications = Job_application.objects.filter(Job_ID=job_id,Job_App_Status='Applied').order_by('id')   
    # Extract a list of Job_Applicant_IDs
    job_applicant_ids = [application.Job_Applicant_ID.id for application in job_applications]    
    user_type = request.session['user_type']   
    # Use job_applicant_ids directly without filtering by 'id__in'
    applicants = Applicant.objects.filter(id__in=job_applicant_ids).order_by('id')
    
    for applicant in applicants:
        applicant.age = calculate_age(applicant.App_DOB)
        # Retrieve the corresponding Job_application table ID
        job_application_id = Job_application.objects.filter(Job_ID=job_id, Job_Applicant_ID=applicant).values_list('id', flat=True).first()
        # Store the Job_application table ID in a new attribute
        applicant.job_application_id = job_application_id

    return render(request, "applications.html", {'send_data': applicants, 'user_type': user_type})

def interview(request):
    # Retrieve the Employer id where EM_Username is the session email
    session_email = request.session['email']
    employer_id = Employer.objects.filter(Emp_Username=session_email).values_list('id', flat=True).first()

    # Find all job ids listed in Jobs table where Employer_id matches the fetched employer_id
    job_ids = Job.objects.filter(Employer_id=employer_id).values_list('id', flat=True)

    # Find all job applications with Job_App_Status='Accepted' and Job_ID in the list of job_ids
    job_applications = Job_application.objects.filter(Job_App_Status='Accepted', Job_ID__in=job_ids).order_by('id')

    # Extract a list of Job_Applicant_IDs
    job_applicant_ids = [application.Job_Applicant_ID.id for application in job_applications]

    # Use job_applicant_ids directly without filtering by 'id__in'
    applicants = Applicant.objects.filter(id__in=job_applicant_ids).order_by('id')

    send_data = []

    for application in job_applications:
        # Retrieve the corresponding Applicant
        applicant = application.Job_Applicant_ID
        applicant.age = calculate_age(applicant.App_DOB)
        applicant_id = applicant.id
        title = application.Job_ID.Job_Title
        

        # Include the specified details in 'send_data' list
        send_data.append({
            'FName': applicant.App_Fname,
            'LName': applicant.App_Lname,
            'Profile': applicant.App_Image,
            'Phone': applicant.App_Phone,
            'Age': applicant.App_DOB,
            'Gender': applicant.App_Gender,
            'Education': applicant.App_Education,
            'Employment_Status': applicant.App_Emp_Status,
            'Linkedin': applicant.App_LinkedIn,
            'Hname': applicant.App_Hname,
            'Street': applicant.App_Street,
            'Dist': applicant.App_Dist,
            'Pin': applicant.App_Pin,
            'Resume': applicant.App_Resume,  # Assuming App_Resume is a FileField
            
            'Job_App_Date': application.Job_App_Date,  # Add Job_Application fields
            'Job_App_Status': application.Job_App_Status,
            'Job_App_Interview_Date': application.Job_App_Interview_Date,
            'Job_App_Interview_Time': application.Job_App_Interview_Time,
            'Job_App_Meeting_Link': application.Job_App_Meeting_Link,
            'Job_App_Description': application.Job_App_Description,
            'Job_App_Id': application.id,  # Add Job_Application ID
            'test2': title,
            'test1': applicant_id
        })

    user_type = request.session['user_type']
    return render(request, "interview.html", {'send_data': send_data, 'user_type': user_type})












def reject_app(request,app_id):
    job_application = get_object_or_404(Job_application, id=app_id)
    # Update Job_App_Status to 'Rejected'
    job_application.Job_App_Status = 'Rejected'
    job_application.save()
    
    
    return redirect('emp_dashboard')

def accept_app(request,app_id):

    if request.method == 'POST':
        int_date = request.POST.get('date')
        int_time = request.POST.get('time')
        int_link = request.POST.get('link')
    job_application = get_object_or_404(Job_application, id=app_id)
    # Update Job_App_Status to 'Accepted'
    job_application.Job_App_Interview_Date = int_date
    job_application.Job_App_Interview_Time = int_time
    job_application.Job_App_Meeting_Link = int_link
    job_application.Job_App_Status = 'Accepted'
    job_application.save()

    return redirect('emp_dashboard')

# def hire_app(request,app_id):

#     if request.method == 'POST':
#         remarks = request.POST.get('remarks')
#     job_application = get_object_or_404(Job_application, id=app_id)
    
#     # Update Job_App_Status to 'Hired'
#     job_application.Job_App_Status = 'Hired'
#     job_application.Job_App_Description = remarks
#     job_application.save()

#     return redirect('emp_dashboard')

def hire_app(request, app_id):

    if request.method == 'POST':
        remarks = request.POST.get('remarks')

        # Get the Job application
        job_application = get_object_or_404(Job_application, id=app_id)

        # Update Job_App_Status to 'Hired'
        job_application.Job_App_Status = 'Hired'
        job_application.Job_App_Description = remarks
        job_application.save()

        # Get the related Job
        job = job_application.Job_ID

        # Reduce the number of Job_Seats by one
        job.Job_Seats -= 1
        job.save()
        
        messages.success(request, "Hired Applicant Successfully")
        return redirect('emp_dashboard')


# def hire_app(request, app_id):

#     if request.method == 'POST':
#         remarks = request.POST.get('remarks')

#         # Get the Job application
#         job_application = get_object_or_404(Job_application, id=app_id)
#         job_id = job_application.Job_ID
#         job = get_object_or_404(Job, id=job_id)

#         # Update Job_App_Status to 'Hired'
#         job_application.Job_App_Status = 'Hired'
#         job_application.Job_App_Description = remarks
#         job_application.save()

#         # Get the related Job
#         job_seats=job.Job_Seats
#         if job_seats>0:
#             job.Job_Seats -= 1
#             job.save()
#         else:
#             request.session['msg'] = "No seats available"
#             return redirect('emp_dashboard')





# path('disable_staff/<int:staff_id>/', views.disable_staff, name='disable_staff'),
#     path('enable_staff/<int:staff_id>/', views.enable_staff, name='enable_staff'),
#  enable staff
def enable_staff(request, staff_id):
    staff = get_object_or_404(Staff, id=staff_id)
    email = staff.Staff_Username
    user_staff = get_object_or_404(User, username=email)  # Access the id attribute
    user_staff.last_name = 1  # Set is_active to True to enable the account
    user_staff.save()
    messages.success(request, "Staff enabled successfully")
    return redirect('staff')



def disable_staff(request, staff_id):
    staff = get_object_or_404(Staff, id=staff_id)
    email = staff.Staff_Username
    user_staff = get_object_or_404(User, username=email)  # Access the id attribute
    user_staff.last_name = 0  # Set is_active to True to enable the account

    user_staff.save()

    
    messages.success(request, "Staff disabled successfully")
    return redirect('staff')




def enable_employee(request, staff_id):
    staff = get_object_or_404(Employer, id=staff_id)
    email = staff.Emp_Username
    user_staff = get_object_or_404(User, username=email)  # Access the id attribute
    user_staff.last_name = 1  # Set is_active to True to enable the account
    user_staff.save()
    messages.success(request, "Employer enabled successfully")
    return redirect('employer')



def disable_employee(request, staff_id):
    staff = get_object_or_404(Employer, id=staff_id)
    email = staff.Emp_Username
    user_staff = get_object_or_404(User, username=email)  # Access the id attribute
    user_staff.last_name = 0  # Set is_active to True to enable the account

    user_staff.save()

    
    messages.success(request, "Employer disabled successfully")
    return redirect('employer')










# applicant_profile
def applicant_profile(request):
    email = request.session['email']
    applicant = Applicant.objects.get(App_Username=email)
    request.session['card_msg'] = None
    job_applications = Job_application.objects.filter(Job_Applicant_ID=applicant, Job_App_Status='Accepted').count()
    return render(request,"applicant_profile.html",{'send_data':applicant,'job_applications_number':job_applications})


def my_applications(request):
    email = request.session['email']
    applicant = Applicant.objects.get(App_Username=email)

    # Retrieve job applications for the specific applicant with the 'Applied' status
    job_applications = Job_application.objects.filter(Job_Applicant_ID=applicant, Job_App_Status='Applied').order_by('id')

    # Retrieve corresponding jobs for the job applications with employer names
    send_data = []
    for job_app in job_applications:
        job = job_app.Job_ID
        #get_object
        # employer = Employer.objects.get(id=job.Employer_id)
        employer = job.Employer_id  # Assuming Employer_ID is a ForeignKey field

        # get_object value


        job_data = {
            'Employer_Name': employer.Emp_Firm,
            'Employer_Image': employer.Emp_Image, 
            'Job_Title': job.Job_Title,
            'Job_Mode': job.Job_Mode,
            'Job_Location': job.Job_Location,
            'Job_Seats': job.Job_Seats,
            'Job_Time_Type': job.Job_Time_Type,
            'Job_Duration': job.Job_Duration,
            'Job_Start': job.Job_Start,
            'Job_End': job.Job_End,
            'Min_Job_Days': job.Min_Job_Days,   
            'Job_Day_Type': job.Job_Day_Type,
            'Job_App_End': job.Job_App_End, 
            'Job_Description': job.Job_Description,
            'Job_City': job.Job_City,
            'Job_State': job.Job_State,
            'Job_Status': job.Job_Status,
            'Job_ID': job.id,
        }
        send_data.append(job_data)

    return render(request, "profile_applications.html", {'send_data': send_data})


# cancel_app
def cancel_app(request):
    if request.method == 'POST':
        app_id = request.POST.get('cancel')
        job = get_object_or_404(Job, id=app_id)
        # select * from job_application where id=app_id
        email = request.session['email']
        applicant_id = get_object_or_404(Applicant, App_Username=email)
        job_application = Job_application.objects.filter(Job_Applicant_ID=applicant_id,Job_ID=job).first()
        job_application.Job_App_Status = 'Cancelled'
        job_application.save()
        messages.success(request, "Application Cancelled Successfully")
        return redirect('applicant_profile')


def my_interviews(request):
    email = request.session['email']
    applicant = Applicant.objects.get(App_Username=email)
    applicant_id = applicant.id

    # Retrieve job applications for the specific applicant with the 'Applied' status
    job_applications = Job_application.objects.filter(Job_Applicant_ID=applicant, Job_App_Status='Accepted').order_by('id')


    # Retrieve corresponding jobs for the job applications with employer names
    send_data = []
    for job_app in job_applications:
        job = job_app.Job_ID
    #     Job_App_Interview_Date = models.DateField(blank=True, null=True)
    # Job_App_Interview_Time = models.TimeField(blank=True, null=True)
    # Job_App_Meeting_Link = models.CharField(max_length=200, blank=True, null=True)
    # Job_App_Description = models.CharField(max_length=100, blank=True, null=True)
        job_inter_date = job_app.Job_App_Interview_Date
        job_inter_time = job_app.Job_App_Interview_Time
        job_inter_link = job_app.Job_App_Meeting_Link
        job_inter_desc = job_app.Job_App_Description

        #get_object
        # employer = Employer.objects.get(id=job.Employer_id)
        employer = job.Employer_id  # Assuming Employer_ID is a ForeignKey field

        # get_object value


        job_data = {
            'Job_App_Interview_Date': job_inter_date,
            'Job_App_Interview_Time': job_inter_time,
            'Job_App_Meeting_Link': job_inter_link,
            'Job_App_Description': job_inter_desc,
            'Employer_Name': employer.Emp_Firm,
            'Employer_id': employer.id,  # Add Employer ID
            'Applicant_id' : applicant_id,
            'Employer_Image': employer.Emp_Image, 
            'Job_Title': job.Job_Title,
            'Job_Mode': job.Job_Mode,
            'Job_Location': job.Job_Location,
            'Job_Seats': job.Job_Seats,
            'Job_Time_Type': job.Job_Time_Type,
            'Job_Duration': job.Job_Duration,
            'Job_Start': job.Job_Start,
            'Job_End': job.Job_End,
            'Min_Job_Days': job.Min_Job_Days,   
            'Job_Day_Type': job.Job_Day_Type,
            'Job_App_End': job.Job_App_End, 
            'Job_Description': job.Job_Description,
            'Job_City': job.Job_City,
            'Job_State': job.Job_State,
            'Job_Status': job.Job_Status,
            'Job_ID': job.id,
        }
        send_data.append(job_data)

    return render(request, "profile_interviews.html", {'send_data': send_data})






def get_review_count(job_application_id):
    return Review.objects.filter(Application_id=job_application_id).count()





def my_hirings(request):
    email = request.session['email']
    applicant = Applicant.objects.get(App_Username=email)

    # Retrieve job applications for the specific applicant with the 'Applied' status
    job_applications = Job_application.objects.filter(Job_Applicant_ID=applicant, Job_App_Status='Hired').order_by('id')


    # Retrieve corresponding jobs for the job applications with employer names
    send_data = []
    for job_app in job_applications:
        job = job_app.Job_ID
        job_inter_date = job_app.Job_App_Interview_Date
        job_inter_time = job_app.Job_App_Interview_Time
        job_inter_link = job_app.Job_App_Meeting_Link
        job_inter_desc = job_app.Job_App_Description
        employer = job.Employer_id  # Assuming Employer_ID is a ForeignKey field

        # select * from job_application where Application ID = job_app.Job_Applicant_ID
        reviews = get_review_count(job_app.id)
       


        # get_object value
        job_data = {
            'Review_Count': reviews,
            'Job_Application_ID': job_app.id,
            'Job_App_Interview_Date': job_inter_date,
            'Job_App_Interview_Time': job_inter_time,
            'Job_App_Meeting_Link': job_inter_link,
            'Job_App_Description': job_inter_desc,
            'Employer_Name': employer.Emp_Firm,
            'Employer_ID': employer.id,  # Add Employer ID
            'Employer_Image': employer.Emp_Image, 
            'Job_Title': job.Job_Title,
            'Job_Mode': job.Job_Mode,
            'Job_Location': job.Job_Location,
            'Job_Seats': job.Job_Seats,
            'Job_Time_Type': job.Job_Time_Type,
            'Job_Duration': job.Job_Duration,
            'Job_Start': job.Job_Start,
            'Job_End': job.Job_End,
            'Min_Job_Days': job.Min_Job_Days,   
            'Job_Day_Type': job.Job_Day_Type,
            'Job_App_End': job.Job_App_End, 
            'Job_Description': job.Job_Description,
            'Job_City': job.Job_City,
            'Job_State': job.Job_State,
            'Job_Status': job.Job_Status,
            'Job_ID': job.id,
        }
        send_data.append(job_data)

    return render(request, "profile_hired.html", {'send_data': send_data})

def my_cards(request):
    email = request.session['email']
    applicant = Applicant.objects.get(App_Username=email)

    #   select  Card_Holder_Name,   Card_No, Exp_Date from card
    #   where Applicant_ID = applicant.id
    applicant_instance = Applicant.objects.get(App_Username=email)
    applicant_id = applicant_instance.id
    app_id = Applicant.objects.get(id=applicant_id)
    today = date.today()
    cards = Pay_Card.objects.filter(Applicant_ID=app_id,Exp_Date__gt=today).order_by('id')
    return render(request,"profile_cards.html",{'send_data':cards})


def add_card(request):
    if request.method == 'POST':
        card_number = request.POST.get('card-number')
        card_holder_name = request.POST.get('card-holder-name')
        expiry_date = request.POST.get('expiry-date')
        email = request.session['email']

        # Get the applicant using the email
        applicant_instance = Applicant.objects.get(App_Username=email)

        # Create a Card object using the correct field names
        card = Pay_Card.objects.create(
            Card_Holder_Name=card_holder_name,
            Applicant_ID=applicant_instance,
            Card_No=card_number,
            Exp_Date=expiry_date
        )

        # Save the card object
        card.save()

        request.session['card_msg'] = "Card added successfully"
        return render(request, "applicant_profile.html", {'user_type': 'AP', 'email': email})
    return render(request,"add_card.html")

# activate_card
def activate_card(request):
    if request.method == 'POST':
        card_id = request.POST.get('card_id')
        card = get_object_or_404(Pay_Card, id=card_id)
        card.Card_Status = 1
        card.save()
        messages.success(request, "Card activated successfully")
        return redirect('my_cards')

# deactivate_card
def deactivate_card(request):
    if request.method == 'POST':
        card_id = request.POST.get('card_id')
        card = get_object_or_404(Pay_Card, id=card_id)
        card.Card_Status = 0
        card.save()
        messages.success(request, "Card deactivated successfully")
        return redirect('my_cards')


def list_plans(request):
    email = request.session['email']    
    plans = Plan.objects.all().order_by('id').filter(Plan_Status=True)
    return render(request,"list_plans.html",{'send_data':plans,'email':email})
       
def add_plan_page(request):
    email = request.session['email']
    return render(request,"add_plan.html",{'email':email})

def reg_plan(request):
    if request.method == 'POST':
        plan_title = request.POST.get('title')
        plan_duration = request.POST.get('duration')
        plan_description = request.POST.get('description')
        plan_level = request.POST.get('level')
        price = request.POST.get('cost')

        staff_email = request.session['email']

        staff_instance = Staff.objects.get(Staff_Username=staff_email)

        plan = Plan.objects.create(
            Staff_ID=staff_instance,
            Plan_Title=plan_title,
            Plan_Duration=plan_duration,
            Plan_Description=plan_description,
            Date=timezone.now(),
            Price=price,
            Plan_Level=plan_level,
            Plan_Status=True
        )
        plan.save()

        request.session['msg'] = "Plan added successfully"
        return redirect('list_plans')
    
# list_plans
# list_plans
def list_plans(request):
    plans = []
    email = request.session['email']    

    # Use values() to fetch specific fields
    all_plans = Plan.objects.order_by('id').values(
        'id',
        'Plan_Title',
        'Plan_Duration',
        'Plan_Description',
        'Date',
        'Price',
        'Plan_Status',
        'Plan_Level',
        'Staff_ID'
    )

    for plan in all_plans:
        plans.append(plan)

    return render(request, "list_plans.html", {'send_data': plans, 'email': email})

#rate_emp

def rate_emp(request):
    if request.method == 'POST':
        emp_id = request.POST.get('emp_id')
        rating = request.POST.get('rating')
        email = request.session['email']
        Job_application_id = request.POST.get('job_app_id')

        # select object from Job_application where id = Job_application_id
        job_application = Job_application.objects.get(id=Job_application_id)



        applicant_instance = Applicant.objects.get(App_Username=email)
        applicant_id = applicant_instance.id
        app_id = Applicant.objects.get(id=applicant_id)

        employer_instance = Employer.objects.get(id=emp_id)
        employer_id = employer_instance.id
        emp_id = Employer.objects.get(id=employer_id)

        rating = Review.objects.create(
   
            Reviewer_ID=app_id,
            Reviewee_ID=emp_id,
            Ratings=rating,
            Application_id = job_application,
            Review_Date=timezone.now()
        )
        rating.save()
        messages.success(request, "Rating added successfully")
        return redirect('applicant_profile')
    
# list_events
from django.shortcuts import get_object_or_404

def list_all_events(request):
    events = Event.objects.filter(Event_Date__gte=date.today(),Event_Status=True).order_by('id')
    user_type = request.session.get('user_type', 'None')
    email = request.session.get('email', 'None')
    if user_type != 'AP':
        return render(request, 'all_events.html', {'user_type': user_type, 'email': email, 'send_events': events})
    else:
        applicant = Applicant.objects.get(App_Username=email)
        app_id = applicant.id
        today = date.today()
        payments = Payment.objects.filter(Applicant_ID=app_id, Expiry_Date__gte=today).order_by('-id')
        
        if payments.exists():
            plan_id = payments.first().Plan_ID_id  # Note: Access the foreign key ID directly
            plan = get_object_or_404(Plan, id=plan_id)
            plan_type = plan.Plan_Level
            return render(request, 'all_events.html', {'user_type': user_type, 'email': email, 'send_events': events, 'plan_level': plan_type})
        else:
            return render(request, 'all_events.html', {'user_type': user_type, 'email': email})

    
    # return render(request, 'all_events.html', {'user_type': user_type, 'email': email, 'send_events':events})

# list_all_plans
def list_all_plans(request):
    plans = Plan.objects.all().order_by('Price').filter(Plan_Status=True)
    user_type = request.session.get('user_type', 'None')
    email = request.session.get('email', 'None')
    return render(request, 'view_all_plans.html', {'user_type': user_type, 'email': email, 'send_data':plans})


# subscribe
def subscribe(request):
    if request.method == 'POST':
        email = request.session['email']
        user_type = request.session['user_type']
        applicant = Applicant.objects.get(App_Username=email)
        app_id = applicant.id
        today = date.today()
        #current plans
        payments = Payment.objects.filter(Applicant_ID=app_id, Expiry_Date__gte=today).order_by('-id')
        # if there exists atleast one Row
        if payments.exists():
            proceed = False
        else:
            proceed = True
        id = request.POST.get('id')#plan id
        plan = Plan.objects.get(id=id)
        tax=1
        total = plan.Price + ((plan.Price * tax)/100)
        # applicant = Applicant.objects.get(App_Username=email)
        # app_id = applicant.id
        today = date.today()
        cards = Pay_Card.objects.filter(Applicant_ID=app_id,Card_Status=1,Exp_Date__gt=today).order_by('id')
        return render(request, 'payment.html', {'plan': plan, 'applicant': applicant, 'user_type': user_type, 'email': email, 'total': total, 'cards': cards, 'proceed': proceed})
        
        
# make_paymentfrom datetime import timedelta

def make_payment(request):
    if request.method == 'POST':
        email = request.session['email']
        user_type = request.session['user_type']
        plan_id = request.POST.get('plan_id')
        card_id = request.POST.get('card_id')
        plan_duration = int(request.POST.get('plan_duration'))  # Convert to integer
    
        plan = Plan.objects.get(id=plan_id)
        card = Pay_Card.objects.get(id=card_id)
        total = request.POST.get('total')
        applicant = Applicant.objects.get(App_Username=email)

        # Calculate expiry date by adding plan_duration months to the current date
        expiry_date = timezone.now() + timedelta(days=30 * plan_duration)

        payment = Payment.objects.create(
            Plan_ID=plan,
            Applicant_ID=applicant,
            Card_ID=card,
            Payment_Date=timezone.now(),
            Total_Price=total,
            Expiry_Date=expiry_date  # Assign calculated expiry date
        )
        payment.save()

        
        # Send email to the user
        # subject = 'Plan Payment Complete'
        # message = f'Thank you for your payment. Your plan is now active.'
        # from_email = settings.DEFAULT_FROM_EMAIL  # Use your default email address
        # recipient_list = [email]

        # send_mail(subject, message, from_email, recipient_list)



        messages.success(request, "Payment successful")
        return redirect('my_subscriptions')


# my_subsriptions
def my_subscriptions(request):
    data_current = []  # Fix: Initialize the list
    data_expired = []  # Fix: Initialize the list
    email = request.session['email']
    user_type = request.session['user_type']
    applicant = Applicant.objects.get(App_Username=email)
    app_id = applicant.id
    today = date.today()
    #current plans
    payments = Payment.objects.filter(Applicant_ID=app_id, Expiry_Date__gte=today).order_by('-id')
 
    for payment in payments:
        purchase_date = payment.Payment_Date
        expiry_date = payment.Expiry_Date
        plan_id = payment.Plan_ID
        payment_id = payment.id
        plan = get_object_or_404(Plan, id=plan_id.id)  # Fix: Use the ID of the Plan object
        plan_title = plan.Plan_Title
        plan_level = plan.Plan_Level
        total_price = payment.Total_Price
        
        data_current.append({
            'id': payment_id,
            'purchase_date': purchase_date,
            'expiry_date': expiry_date,
            'plan_title': plan_title,
            'plan_level': plan_level,
            'total_price': total_price
        })
    
    #expired plans
    expired_payments = Payment.objects.filter(Applicant_ID=app_id, Expiry_Date__lt=today).order_by('-id')

    for payment in expired_payments:
        purchase_date = payment.Payment_Date
        expiry_date = payment.Expiry_Date
        plan_id = payment.Plan_ID
        plan = get_object_or_404(Plan, id=plan_id.id)  # Fix: Use the ID of the Plan object
        plan_title = plan.Plan_Title
        plan_level = plan.Plan_Level
        total_price = payment.Total_Price
        payment_id = payment.id
        data_expired.append({
            'id': payment_id,
            'purchase_date': purchase_date,
            'expiry_date': expiry_date,
            'plan_title': plan_title,
            'plan_level': plan_level,
            'total_price': total_price
        })
    

    
    return render(request, 'profile_subscriptions.html', {'user_type': user_type, 'email': email, 'data_c': data_current, 'data_e': data_expired})



    # path('cancel_subscription),
def cancel_subscription(request):
    if request.method == 'POST':
        payment_id = request.POST.get('p_id')
        payment = get_object_or_404(Payment, id=payment_id)
        yesterday = date.today() - timedelta(days=1)
        new_expiry_date = yesterday  # Set the expiry date to yesterday to cancel the subscription
        payment.Expiry_Date = new_expiry_date
        payment.save()
        messages.success(request, "Subscription cancelled successfully")
        return redirect('my_subscriptions')
    

# list_subs
# def list_subs(request):
#     email = request.session['email']
#     user_type = request.session['user_type']

#     today = date.today()
#     #current plans
#     payments = Payment.objects.filter(Expiry_Date__gte=today).order_by('-id')
#     data_current = []  # Fix: Initialize the list
#     for payment in payments:
#         purchase_date = payment.Payment_Date
#         expiry_date = payment.Expiry_Date
#         plan_id = payment.Plan_ID
#         applicant_id = payment.Applicant_ID
#         applicant_instance = Applicant.objects.get(id=applicant_id.id)
#         app_fname = applicant_instance.App_Fname
#         app_lname = applicant_instance.App_Lname
#         plan = get_object_or_404(Plan, id=plan_id.id)  # Fix: Use the ID of the Plan object
#         plan_title = plan.Plan_Title
#         plan_level = plan.Plan_Level
#         total_price = payment.Total_Price
#         data_current.append({
#             'applicant_id': applicant_id,
#             'app_fname': app_fname,
#             'app_lname': app_lname,
#             'purchase_date': purchase_date,
#             'expiry_date': expiry_date,
#             'plan_title': plan_title,
#             'plan_level': plan_level,
#             'total_price': total_price
#         })
#     #expired plans
#     expired_payments = Payment.objects.filter(Expiry_Date__lt=today).order_by('-id')
#     data_expired = []  # Fix: Initialize the list
#     for payment in expired_payments:
#         purchase_date = payment.Payment_Date
#         expiry_date = payment.Expiry_Date
#         plan_id = payment.Plan_IDapplicant_id = payment.Applicant_ID
#         applicant_instance = Applicant.objects.get(id=applicant_id.id)
#         app_fname = applicant_instance.App_Fname
#         app_lname = applicant_instance.App_Lname
#         plan = get_object_or_404(Plan, id=plan_id.id)  # Fix: Use the ID of the Plan object
#         plan_title = plan.Plan_Title
#         plan_level = plan.Plan_Level
#         total_price = payment.Total_Price
#         data_expired.append({
#              'applicant_id': applicant_id,
#             'app_fname': app_fname,
#             'app_lname': app_lname,
#             'purchase_date': purchase_date,
#             'expiry_date': expiry_date,
#             'plan_title': plan_title,
#             'plan_level': plan_level,
#             'total_price': total_price
#         })
#     return render(request, 'list_subs.html', {'user_type': user_type, 'email': email, 'data_c': data_current, 'data_e': data_expired})
    
def list_subs(request):
    email = request.session['email']
    user_type = request.session['user_type']

    today = date.today()

    def process_payment(payment):
        purchase_date = payment.Payment_Date
        expiry_date = payment.Expiry_Date
        plan_id = payment.Plan_ID
        applicant_id = payment.Applicant_ID
        app_id=applicant_id.id
        applicant_instance = Applicant.objects.get(id=applicant_id.id)
        app_fname = applicant_instance.App_Fname
        app_lname = applicant_instance.App_Lname
        plan = get_object_or_404(Plan, id=plan_id.id)
        plan_title = plan.Plan_Title
        plan_level = plan.Plan_Level
        total_price = payment.Total_Price

        return {
            'applicant_id': app_id,
            'app_fname': app_fname,
            'app_lname': app_lname,
            'purchase_date': purchase_date,
            'expiry_date': expiry_date,
            'plan_title': plan_title,
            'plan_level': plan_level,
            'total_price': total_price
        }

    # Current plans
    payments_current = Payment.objects.filter(Expiry_Date__gte=today).order_by('-id')
    data_current = [process_payment(payment) for payment in payments_current]

    # Expired plans
    payments_expired = Payment.objects.filter(Expiry_Date__lt=today).order_by('-id')
    data_expired = [process_payment(payment) for payment in payments_expired]

    return render(request, 'list_subs.html', {'user_type': user_type, 'email': email, 'data_c': data_current, 'data_e': data_expired})


# views.chat_app
# def chat_app(request):
#     if request.method == 'POST':
#         id = request.POST.get('applicant')
#         emp_id = request.POST.get('employer')
#         applicant = Applicant.objects.get(id=id)  # Use 'id' instead of 'App_ID'
#         app_id = applicant.id
#         employer = Employer.objects.get(id=emp_id)
#         employer_id = employer.id
#         chats = Chat.objects.filter(App_ID=app_id, EM_ID=employer_id).order_by('id')
        
#         Message = []
#         if chats.exists():
#             for msg in chats:
#                 chat_id = msg.id
#                 chat_matter = msg.Chat_Matter
#                 sender_status = msg.Sender_status

#                 Message.append({
#                     'chat_id': chat_id,
#                     'chat_matter': chat_matter,
#                     'sender_status': sender_status
#                 })
#         return render(request, 'chat_profile.html', {'send_data': Message, 'applicant': app_id, 'employer': employer_id})
    

def hired_app(request):
    # Retrieve the Employer id where EM_Username is the session email
    session_email = request.session['email']
    employer_id = Employer.objects.filter(Emp_Username=session_email).values_list('id', flat=True).first()

    # Find all job ids listed in Jobs table where Employer_id matches the fetched employer_id
    job_ids = Job.objects.filter(Employer_id=employer_id).values_list('id', flat=True)

    # Find all job applications with Job_App_Status='Accepted' and Job_ID in the list of job_ids
    job_applications = Job_application.objects.filter(Job_App_Status='Hired', Job_ID__in=job_ids).order_by('id')

    # Extract a list of Job_Applicant_IDs
    job_applicant_ids = [application.Job_Applicant_ID.id for application in job_applications]

    # Use job_applicant_ids directly without filtering by 'id__in'
    applicants = Applicant.objects.filter(id__in=job_applicant_ids).order_by('id')

    send_data = []

    for application in job_applications:
        # Retrieve the corresponding Applicant
        applicant = application.Job_Applicant_ID
        applicant.age = calculate_age(applicant.App_DOB)
        applicant_id = applicant.id
        title = application.Job_ID.Job_Title
        


        # Include the specified details in 'send_data' list
        send_data.append({
            'FName': applicant.App_Fname,
            'LName': applicant.App_Lname,
            'Profile': applicant.App_Image,
            'Phone': applicant.App_Phone,
            'Age': applicant.App_DOB,
            'Gender': applicant.App_Gender,
            'Education': applicant.App_Education,
            'Employment_Status': applicant.App_Emp_Status,
            'Linkedin': applicant.App_LinkedIn,
            'Hname': applicant.App_Hname,
            'Street': applicant.App_Street,
            'Dist': applicant.App_Dist,
            'Pin': applicant.App_Pin,
            'Resume': applicant.App_Resume,  # Assuming App_Resume is a FileField
            'Job_App_Date': application.Job_App_Date,  # Add Job_Application fields
            'Job_App_Status': application.Job_App_Status,
            'Job_App_Interview_Date': application.Job_App_Interview_Date,
            'Job_App_Interview_Time': application.Job_App_Interview_Time,
            'Job_App_Meeting_Link': application.Job_App_Meeting_Link,
            'Job_App_Description': application.Job_App_Description,
            'Job_App_Id': application.id,  # Add Job_Application ID
            'test1' : applicant_id,
            'test2' : title
            
        })

    user_type = request.session['user_type']
    return render(request, "hired.html", {'send_data': send_data, 'user_type': user_type})



# search_job
def search_job(request):
    if request.method == 'POST':
        search = request.POST.get('search')

        jobs_with_images = []  # Initialize the list

        jobs = Job.objects.filter(
            Q(Job_Title__icontains=search) |
            Q(Job_Mode__icontains=search) |
            Q(Job_Location__icontains=search) |
            Q(Job_Time_Type__icontains=search) |
            Q(Job_Duration__icontains=search) |
            Q(Job_Day_Type__icontains=search) |
            Q(Job_Description__icontains=search) |
            Q(Job_City__icontains=search) |
            Q(Job_State__icontains=search),
            Job_Status=True,Job_App_End__gte=timezone.now()
        ).order_by('id')

        for job in jobs:
            email = job.EM_Username
            employer = Employer.objects.filter(Emp_Username=email).first()
            employer_id = employer.id
            emp_id = Employer.objects.get(id=employer_id)
            
            job_ids = jobs = Job.objects.filter(
                Q(Job_Title__icontains=search) |
                Q(Job_Mode__icontains=search) |
                Q(Job_Location__icontains=search) |
                Q(Job_Time_Type__icontains=search) |
                Q(Job_Duration__icontains=search) |
                Q(Job_Day_Type__icontains=search) |
                Q(Job_Description__icontains=search) |
                Q(Job_City__icontains=search) |
                Q(Job_State__icontains=search),
                Job_Status=True
            ).values_list('id', flat=True)

            job_applications = Job_application.objects.filter(Job_ID__in=job_ids).order_by('id')
            ratings = Review.objects.filter(Reviewee_ID=emp_id).order_by('id')

            plan = 'no_plan'
            # Fix: Initialize rating before using it in the loop
            rating = 0
        
            for each_rating in ratings:
                rating += each_rating.Ratings

            # Check if employer exists
            if employer:
                job_with_image = {
                    'id': job.id,
                    'EM_Username': job.EM_Username,
                    'Job_Title': job.Job_Title,
                    'Job_Mode': job.Job_Mode,
                    'Job_Location': job.Job_Location,
                    'Job_Seats': job.Job_Seats,
                    'Job_Time_Type': job.Job_Time_Type,
                    'Job_Duration': job.Job_Duration,
                    'Job_Start': job.Job_Start,
                    'Job_End': job.Job_End,
                    'Min_Job_Days': job.Min_Job_Days,
                    'Job_Day_Type': job.Job_Day_Type,
                    'Job_App_End': job.Job_App_End,
                    'Job_Description': job.Job_Description,
                    'Job_City': job.Job_City,
                    'Job_State': job.Job_State,
                    'Job_Status': job.Job_Status,
                    'emp_image': employer.Emp_Image,  # Assuming Emp_image stores only the filename
                    'ratings': rating
                }
                jobs_with_images.append(job_with_image)

        context = {
            'jobs_with_images': jobs_with_images
        }

        user_type = request.session.get('user_type', 'None')
        email = request.session.get('email', 'None')

        if user_type == 'AP':
            applicant_id = Applicant.objects.filter(App_Username=email).values_list('id', flat=True).first()
            if applicant_id:
                today = date.today()
                payment_id = Payment.objects.filter(Applicant_ID=applicant_id,Expiry_Date__gt=today).first()
                if payment_id:
                    # extract the plan id
                    plan_id = payment_id.Plan_ID.id
                    # extract the plan details
                    plan = Plan.objects.filter(id=plan_id).first()
                    plan_level = plan.Plan_Level 
                    plan=plan_level
  
        return render(request, 'jobs.html', {'user_type': user_type, 'email': email, 'jobs_with_images': jobs_with_images, 'plan': plan})
    
# submit_job_time
    # search with job time
def submit_job_time(request):
    if request.method == 'POST':
        commencement = request.POST.get('commencementTime')
        end = request.POST.get('endTime')
        jobs_with_images = []  # Initialize the list

        jobs = Job.objects.filter(
            Q(Job_Start__gte=commencement) &
            Q(Job_End__lte=end),
            Job_Status=True
        ).order_by('id')

        for job in jobs:
            email = job.EM_Username
            employer = Employer.objects.filter(Emp_Username=email).first()
            employer_id = employer.id
            emp_id = Employer.objects.get(id=employer_id)

            job_ids = Job.objects.filter(
                Q(Job_Start__gte=commencement) &
                Q(Job_End__lte=end),
                Job_Status=True
            ).values_list('id', flat=True)

            job_applications = Job_application.objects.filter(Job_ID__in=job_ids).order_by('id')
            ratings = Review.objects.filter(Reviewee_ID=emp_id).order_by('id')
            plan= 'no_plan'
            # Fix: Initialize rating before using it in the loop
            rating = 0

            for each_rating in ratings:
                rating += each_rating.Ratings

            # Check if employer exists
            if employer:
                job_with_image = {
                    'id': job.id,
                    'EM_Username': job.EM_Username,
                    'Job_Title': job.Job_Title,
                    'Job_Mode': job.Job_Mode,
                    'Job_Location': job.Job_Location,
                    'Job_Seats': job.Job_Seats,
                    'Job_Time_Type': job.Job_Time_Type,
                    'Job_Duration': job.Job_Duration,
                    'Job_Start': job.Job_Start,
                    'Job_End': job.Job_End,
                    'Min_Job_Days': job.Min_Job_Days,
                    'Job_Day_Type': job.Job_Day_Type,
                    'Job_App_End': job.Job_App_End,
                    'Job_Description': job.Job_Description,
                    'Job_City': job.Job_City,
                    'Job_State': job.Job_State,
                    'Job_Status': job.Job_Status,
                    'emp_image': employer.Emp_Image,  # Assuming Emp_image stores only the filename
                    'ratings': rating
                }
                jobs_with_images.append(job_with_image)

        context = {
            'jobs_with_images': jobs_with_images
        }

        user_type = request.session.get('user_type', 'None')
        email = request.session.get('email', 'None')

        if user_type == 'AP':
            applicant_id = Applicant.objects.filter(App_Username=email).values_list('id', flat=True).first()
            if applicant_id:
                today = date.today()
                payment_id = Payment.objects.filter(Applicant_ID=applicant_id,Expiry_Date__gt=today).first()
                if payment_id:
                    # extract the plan id
                    plan_id = payment_id.Plan_ID.id
                    # extract the plan details
                    plan = Plan.objects.filter(id=plan_id).first()
                    plan_level = plan.Plan_Level 
                    plan=plan_level

        return render(request, 'jobs.html', {'user_type': user_type, 'email': email, 'jobs_with_images': jobs_with_images})

    
# download_invoice
def download_invoice(request):
    if request.method == 'POST':
        payment_id = request.POST.get('p_id')
        details = []
        payment = get_object_or_404(Payment, id=payment_id)
        Date_of_payment = payment.Payment_Date  
        Expiry_Date = payment.Expiry_Date
        Total_Price = payment.Total_Price
        applicant = payment.Applicant_ID
        plan = payment.Plan_ID
        # card = payment.Card_ID
        applicant_details = get_object_or_404(Applicant, id=applicant.id)
        plan_details = get_object_or_404(Plan, id=plan.id)


        today = date.today() 

        details.append({
            'Date_of_payment': Date_of_payment,
            'Expiry_Date': Expiry_Date,
            'Total_Price': Total_Price,
            'Applicant_Fname': applicant_details.App_Fname,
            'Applicant_Lname': applicant_details.App_Lname,
            'Plan_Title': plan_details.Plan_Title,
            'Plan_Level' : plan_details.Plan_Level,
            'Plan_Duration': plan_details.Plan_Duration,
            'Price': plan_details.Price,
            'App_Username' : applicant_details.App_Username,
            'App_Hname' : applicant_details.App_Hname,
            'App_Street' : applicant_details.App_Street,
            'App_Dist' : applicant_details.App_Dist,
            'App_Pin' : applicant_details.App_Pin,
            'App_Phone' : applicant_details.App_Phone,
            'Today' : today
        })


        return render(request, 'receipt.html', {'details':details})
        

# change_job_status
def change_job_status(request):
    if request.method == 'POST':
        job_id = request.POST.get('cancel')
        status = request.POST.get('status')
        job = get_object_or_404(Job, id=job_id)
        if status == '0':
            job.Job_Status = True
        elif status == '1':
            job.Job_Status = False
        job.save()
        return redirect('emp_dashboard')
# edit job
def edit_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    return render(request, 'edit_job.html', {'job': job})

# update_job
def update_job(request):
    if request.method == 'POST':
        # Retrieve data from the form
        job_id = request.POST.get('job_id')
        jobTitle = request.POST.get('firstName')
        location = request.POST.get('location')
        timing = request.POST.get('timing')
        commencement = request.POST.get('commencement')
        workdays = request.POST.get('workdays')
        deadline = request.POST.get('deadline')
        description = request.POST.get('description')
        mode = request.POST.get('mode')
        vaccancies = request.POST.get('vaccancies')
        worktime = request.POST.get('worktime')
        completion = request.POST.get('completion')
        workdaytype = request.POST.get('workdaytype')
        city = request.POST.get('city')
        state = request.POST.get('state')

        # Update the job with new data
        job = get_object_or_404(Job, id=job_id)
        job.Job_Title = jobTitle
        job.Job_Location = location
        job.Job_Time_Type = timing
        job.Job_Start = commencement
        job.Min_Job_Days = workdays
        job.Job_App_End = deadline
        job.Job_Description = description
        job.Job_Mode = mode
        job.Job_Seats = vaccancies
        job.Job_Duration = worktime
        job.Job_End = completion
        job.Job_Day_Type = workdaytype
        job.Job_City = city
        job.Job_State = state

        # Save the updated job
        job.save()

        # Optionally, you can add a success message or redirect to a different page
        
        messages.success(request, "Job Updated Successfully")
        return redirect('emp_dashboard')

    else:
        # Handle the case where the request method is not POST
        return HttpResponseBadRequest("Invalid request method")






def enable_applicant(request):
    if request.method == 'POST':
        staff_id = request.POST.get('login')
        staff = get_object_or_404(Applicant, id=staff_id)
        email = staff.App_Username
        user_staff = get_object_or_404(User, username=email)  # Access the id attribute
        user_staff.last_name = 1  # Set is_active to True to enable the account
        user_staff.save()
        messages.success(request, "Applicant enabled successfully")
        return redirect('applicant')



def disable_applicant(request):
    if request.method == 'POST':
        staff_id = request.POST.get('login')
        staff = get_object_or_404(Applicant, id=staff_id)
        email = staff.App_Username
        user_staff = get_object_or_404(User, username=email)  # Access the id attribute
        user_staff.last_name = 0  # Set is_active to True to enable the account

        user_staff.save()

        
        messages.success(request, "Applicant disabled successfully")
        return redirect('applicant')



# employer_list
def employer_list(request):
    # load_staff from user table with first_name = 'ST'
    load_staff_users = User.objects.filter(first_name='EM').order_by('id')
    
    array = []
    
    for staff_user in load_staff_users:
        staff_username = staff_user.username
        # Use filter instead of get to handle potential multiple results
        load_staff_detail = Employer.objects.filter(Emp_Username=staff_username).first()
        
        if load_staff_detail:
            staff_details = {
                'id': load_staff_detail.id,
                'Emp_Username': load_staff_detail.Emp_Username,
                'Emp_Firm': load_staff_detail.Emp_Firm,
                'Emp_Phone': load_staff_detail.Emp_Phone,
                'Emp_Street': load_staff_detail.Emp_Street,
                'Emp_Dist': load_staff_detail.Emp_Dist,
                'Emp_State': load_staff_detail.Emp_State,
                'Emp_Pin': load_staff_detail.Emp_Pin,
                'Emp_Image': load_staff_detail.Emp_Image,
                'Emp_Date': load_staff_detail.Emp_Date,
                'is_active': staff_user.last_name,
            }
            array.append(staff_details)

    user_type = request.session.get('user_type', None)
    return render(request, "employer_list.html", {'send_list': array, 'user_type': user_type})



def applicant_list(request):
    # load_staff from user table with first_name = 'ST'
    load_staff_users = User.objects.filter(first_name='AP').order_by('id')
    
    array = []
    
    for staff_user in load_staff_users:
        staff_username = staff_user.username
        # Use filter instead of get to handle potential multiple results
        load_staff_detail = Applicant.objects.filter(App_Username=staff_username).first()
        
        if load_staff_detail:
            staff_details = {
                'id': load_staff_detail.id,
                'App_Username': load_staff_detail.App_Username,
                'App_Fname': load_staff_detail.App_Fname,
                'App_Lname': load_staff_detail.App_Lname,
                'App_Phone': load_staff_detail.App_Phone,
                'App_DOB': load_staff_detail.App_DOB,
                'App_Education': load_staff_detail.App_Education,
                'App_Emp_Status': load_staff_detail.App_Emp_Status,
                'App_LinkedIn': load_staff_detail.App_LinkedIn,
                'App_Image': load_staff_detail.App_Image,
                'App_Hname': load_staff_detail.App_Hname,
                'App_Gender' : load_staff_detail.App_Gender,
                'App_Street' : load_staff_detail.App_Street,
                'App_Dist' : load_staff_detail.App_Dist,
                'App_Pin' : load_staff_detail.App_Pin,
                'App_Date' : load_staff_detail.App_Date,
                'App_Resume' : load_staff_detail.App_Resume,
                'is_active': staff_user.last_name,
            }
            array.append(staff_details)

    user_type = request.session.get('user_type', None)
    return render(request, "applicant_list.html", {'send_list': array, 'user_type': user_type})


def enable_event(request):
    if request.method == 'POST':
        staff_id = request.POST.get('login')
        staff = get_object_or_404(Event, id=staff_id)
        staff.Event_Status = True  # Set Event_Status to True to enable the account
        staff.save()
        messages.success(request, "Event enabled successfully")
        return redirect('manage_events')

def disable_event(request):
    if request.method == 'POST':
        staff_id = request.POST.get('login')
        staff = get_object_or_404(Event, id=staff_id)
        staff.Event_Status = False  # Set Event_Status to False to disable the account
        staff.save()
        messages.success(request, "Event disabled successfully")
        return redirect('manage_events')
    
def enable_plan(request):
    if request.method == 'POST':
        staff_id = request.POST.get('login')
        staff = get_object_or_404(Plan, id=staff_id)
        staff.Plan_Status = True  # Set Event_Status to True to enable the account
        staff.save()
        messages.success(request, "Plan enabled successfully")
        return redirect('list_plans')

def disable_plan(request):
    if request.method == 'POST':
        staff_id = request.POST.get('login')
        staff = get_object_or_404(Plan, id=staff_id)
        staff.Plan_Status = False  # Set Event_Status to False to disable the account
        staff.save()
        messages.success(request, "Plan disabled successfully")
        return redirect('list_plans')
    
# edit_staff
def edit_staff(request, staff_id):
    staff = get_object_or_404(Staff, id=staff_id)
    return render(request, 'edit_staff.html', {'staff': staff})



# update_job
def update_staff(request):
    if request.method == 'POST':
        # Retrieve data from the form

        id = request.POST.get('id')
        firstName = request.POST.get('firstName')
        lastName = request.POST.get('lastName')
        phoneNumber = request.POST.get('phoneNumber')
        gender = request.POST.get('gender')
        dob = request.POST.get('dob')
        houseName = request.POST.get('houseName')
        street = request.POST.get('street')
        district = request.POST.get('district')
        pincode = request.POST.get('pincode')



        staff = get_object_or_404(Staff, id=id)
        staff.Staff_Fname = firstName
        staff.Staff_Lname = lastName
        staff.Staff_Phone = phoneNumber
        staff.Staff_Gender = gender
        staff.Staff_DOB = dob
        staff.Staff_Hname = houseName
        staff.Staff_Street = street
        staff.Staff_Dist = district
        staff.Staff_Pin = pincode
        staff.save()
    
        messages.success(request, "Staff Updated Successfully")
        return redirect('staff')


        

    else:
        # Handle the case where the request method is not POST
        return HttpResponseBadRequest("Invalid request method")

# edit_app
def edit_app(request, app_id):
    app = get_object_or_404(Applicant, id=app_id)
    return render(request, 'edit_app.html', {'app': app})



        # Retrieve data from the form
#         <form action="update_applicant" enctype="multipart/form-data" method="POST">
#         {% csrf_token %}
#         <div class="registration-form">
#             <div class="registration-form-left">
#                 <!-- Other fields... -->
#                <intput type="hidden" name="id" value="{{ app.App_ID }}">
#                 <label for="firstName">Applicant name</label>
#                 <input type="text" id="firstName" name="firstName" placeholder="First name" required maxlength="10" value="{{ app.App_Fname }}">
                
#                 <label for="gender">Gender</label>
#                 <select id="gender" name="gender" required>
#                     <option value="" disabled selected hidden>Select gender</option>
#                     <option value="Male" {% if app.App_Gender == 'Male' %}selected{% endif %}>Male</option>
#                     <option value="Female" {% if app.App_Gender == 'Female' %}selected{% endif %}>Female</option>
#                     <option value="Others" {% if app.App_Gender == 'Others' %}selected{% endif %}>Other</option>
#                 </select>
    
#                 <label for="education">Educational qualification</label>
#                 <select id="education" name="education" required>
#                     <option value="" disabled selected hidden>Select qualification</option>
#                     <option value="10th" {% if app.App_Education == '10th' %}selected{% endif %}>10th</option>
#                     <option value="12th" {% if app.App_Education == '12th' %}selected{% endif %}>12th</option>
#                     <option value="Graduate" {% if app.App_Education == 'Graduate' %}selected{% endif %}>Graduate</option>
#                     <option value="Post Graduate" {% if app.App_Education == 'Post Graduate' %}selected{% endif %}>Post Graduate</option>
#                     <option value="Others" {% if app.App_Education == 'Others' %}selected{% endif %}>Others</option>
#                 </select>
    
#                 <label for="linkedin">Linkedin URL</label>
#                 <input type="text" id="linkedin" name="linkedin" placeholder="Linkedin URL" required maxlength="100" value="{{ app.App_LinkedIn }}">
    
#                 <label for="profilePhoto">Profile photo</label>
#                 <input type="file" id="profilePhoto" name="profilePhoto" required>
                
#                 <label for="address">Street</label>
#                 <input type="text" id="address" name="street" placeholder="Street" required maxlength="15" value="{{ app.App_Street }}">
    
#                 <label for="pincode">Pincode</label>
#                 <input type="text" id="pincode" name="pincode" placeholder="Enter 6 digit pincode" pattern="[0-9]{6}" required title="Enter a valid pincode" value="{{ app.App_Pin }}">
               
#                 <!-- <label for="phoneNumber">Phone number</label>
#                 <input type="tel" id="phoneNumber" name="phoneNumber" placeholder="Enter a 10 digit phone number" pattern="[0-9]{10}" required title="Enter a valid phone number" value="{{ app.App_Phone }}">
#      -->
#             </div>
    
#             <div class="registration-form-right">
#                 <!-- Other fields... -->
    
#                 <label for="lastName">Last name</label>
#                 <input type="text" id="lastName" name="lastName" placeholder="Last name" maxlength="10" value="{{ app.App_Lname }}">
      
#                 <!-- date of birth -->
# <label for="dob">Date of birth</label>
# <input type="date" id="dob" name="dob" required value="{{ app.App_DOB|date:'Y-m-d' }}">

    
#                 <label for="employment">Employment status</label>
#                 <select id="employment" name="employment" required>
#                     <option value="" disabled selected hidden>Select employment status</option>
#                     <option value="Employed" {% if app.App_Emp_Status == 'Employed' %}selected{% endif %}>Employed</option>
#                     <option value="Unemployed" {% if app.App_Emp_Status == 'Unemployed' %}selected{% endif %}>Unemployed</option>
#                     <option value="Student" {% if app.App_Emp_Status == 'Student' %}selected{% endif %}>Student</option>
#                     <option value="Others" {% if app.App_Emp_Status == 'Others' %}selected{% endif %}>Others</option>
#                 </select>
    
#                 <label for="resume">Resume</label>
#                 <input type="file" id="resume" name="resume" required>
    
#                 <label for="houseName">House name</label>
#                 <input type="text" id="houseName" name="houseName" placeholder="House, apartment, suit, etc." required maxlength="20" value="{{ app.App_Hname }}">
              
#                 <label for="district">District</label>
#                 <input type="text" id="district" name="district" placeholder="District" required maxlength="18" value="{{ app.App_Dist }}">
    
#                 <label for="phoneNumber">Phone number</label>
#                 <input type="tel" id="phoneNumber" name="phoneNumber" placeholder="Enter a 10 digit phone number" pattern="[0-9]{10}" required title="Enter a valid phone number" value="{{ app.App_Phone }}">
       
#             </div>
#           </div>
#             <button type="submit" name="submit">Update</button>


# update_applicant
def update_applicant(request):
    if request.method == 'POST':
        # Retrieve data from the form
        id = request.POST.get('id')
        firstName = request.POST.get('firstName')
        lastName = request.POST.get('lastName')
        phoneNumber = request.POST.get('phoneNumber')
        education = request.POST.get('education')
        employment = request.POST.get('employment')
        linkedin = request.POST.get('linkedin')
        street = request.POST.get('street')
        pincode = request.POST.get('pincode')
        dob = request.POST.get('dob')
        houseName = request.POST.get('houseName')
        district = request.POST.get('district')

        #  if 'logo' in request.FILES and request.FILES['logo']:
        #     # If a new logo is provided, save it
        #     firm_logo = request.FILES['logo']
        #     fs = FileSystemStorage()
        #     filename = fs.save(firm_logo.name, firm_logo)
        #     Employer.objects.filter(id=id).update(Emp_Firm=firmName,Emp_Image=firm_logo,Emp_Phone=phoneNumber,Emp_Street=street,Emp_Dist=district,Emp_State=state,Emp_Pin=pincode)
       

        if 'profilePhoto' in request.FILES and request.FILES['profilePhoto']:
            # If a new profile photo is provided, save it
            profile_photo = request.FILES['profilePhoto']
            fs = FileSystemStorage()
            filename = fs.save(profile_photo.name, profile_photo)
            Applicant.objects.filter(id=id).update(App_Image=profile_photo)
            # messages.success(request, "Applicant Updated Successfully")

        if 'resume' in request.FILES and request.FILES['resume']:
            # If a new resume is provided, save it
            resume = request.FILES['resume']
            fs = FileSystemStorage()
            filename = fs.save(resume.name, resume)
            Applicant.objects.filter(id=id).update(App_Resume=resume)

        
    Applicant.objects.filter(id=id).update(App_Fname=firstName,App_Lname=lastName,App_Phone=phoneNumber,App_Education=education,App_Emp_Status=employment,App_LinkedIn=linkedin,App_Street=street,App_Dist=district,App_Pin=pincode,App_DOB=dob,App_Hname=houseName)
    messages.success(request, "Applicant Updated Successfully")

    return redirect('applicant')
    
# edit_event
def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'edit_event.html', {'event': event})
        

