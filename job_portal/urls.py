"""
URL configuration for job_portal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from jp_app import views


urlpatterns = [
        #path('url_name',views.function_name),
    #clear alert msg
    path('clear_msg/', views.clear_msg, name='clear_msg'),
    path('', views.index1),
    path('index',views.index, name='index'),
    #redirect to login page
    path('login',views.login_view),
    #req_login
    path('req_login',views.req_login),
    #logout 
    path('logout',views.user_logout),
    path('signin',views.signin),
     path('select_user', views.select_user, name='select_user'),  # Add this line
    # path('signin1',views.signin1),
    path('applicant', views.applicant_page, name='applicant_page'),  # Update with your view
    #get_app_details
    path('reg_applicant',views.reg_new_applicant),
    path('employer', views.employer_page, name='employer_page'),
    #admin_page
    path('admin_page',views.admin_page, name='admin_page'),
    # satff_page
    path('staff_page',views.staff_page),
    #applicant_list
    path('applicant_list',views.applicant_list,name='applicant'),
    # employer_reg
    path('reg_employer',views.reg_new_employer),
    # edit employer
    path('edit_emp/<int:id>',views.edit_emp),
    #update_emp
    path('edit_emp/update_emp', views.update_emp, name='update_emp'),
    #employer_list
    path('employer_list',views.employer_list,name='employer'),
    #staff_list
    path('staff_list',views.staff_list,name='staff'),
    #add_staff
    path('add_staff',views.add_staff),
    #reg_staff
    path('reg_staff',views.reg_staff),
    #emp_dasjboard
    path('emp_dashboard', views.emp_dashboard, name='emp_dashboard'),
    #job_vaccanies
    path('vaccancies',views.vaccancies),
    #add_job
    path('add_job',views.add_job),
    #reg_job
    path('reg_job',views.reg_job),
    # update_job
    # path('update_job', views.update_job),
    path('edit_job/update_job', views.update_job, name='update_job'),
    # view_all_jobs
    path('view_all_jobs',views.view_all_jobs),
    #manage_events
    path('manage_events',views.manage_events, name='manage_events'),
    #add_event
    path('add_event',views.add_event),
    #reg_event
    path('reg_event',views.reg_event),
    # list_jobs
    path('list_jobs',views.list_jobs, name='list_jobs'),
    #apply jobs
    path('apply_job',views.apply_jobs),
    #applicantions applied
    path('applications/<int:job_id>', views.view_application),
    #reject_app
    path('reject_app/<int:app_id>', views.reject_app),
    #accept_app
    path('accept_app/<int:app_id>', views.accept_app),
    # hire_app
    path('hire_app/<int:app_id>', views.hire_app),
    # disable , enable staff
    path('disable_staff/<int:staff_id>/', views.disable_staff, name='disable_staff'),
    path('enable_staff/<int:staff_id>/', views.enable_staff, name='enable_staff'),
    #interview
    path('interview', views.interview),
    #hired_app
   path('hired_app', views.hired_app),
        # applicant_page
    path('applicant_page', views.applicant_profile, name='applicant_profile'),
    # /my_applications
    path('my_applications', views.my_applications),
    # cancel_app
    path('cancel_app', views.cancel_app),
    #my_interviews
    path('my_interviews', views.my_interviews),
    #my_hirings
    path('my_hirings', views.my_hirings),
    #my_cards
    path('my_cards', views.my_cards, name='my_cards'),
    #add_card
    path('add_card', views.add_card),
    # list_plans
    path('list_plans', views.list_plans, name='list_plans'),
    # add_plan_page
    path('add_plan_page', views.add_plan_page),
    # reg_plan
    path('reg_plan', views.reg_plan),
    # list_plans
    path('list_plans', views.list_plans, name='list_plans'),
    # rate_emp
    path('rate_emp', views.rate_emp),
#    list_all_events
    path('list_all_events', views.list_all_events),
    # list_all_plans
    path('list_all_plans', views.list_all_plans),
    # subscribe
    path('subscribe', views.subscribe),
    # make_payment
    path('make_payment', views.make_payment),
    # /my_subsriptions
    path('my_subscriptions', views.my_subscriptions, name='my_subscriptions'),
    # cancel_subscription
    path('cancel_subscription', views.cancel_subscription),
    # ../list_subs
    path('list_subs', views.list_subs),
    # search_job
    path('search_job', views.search_job),
    # download_invoice
    path('download_invoice', views.download_invoice),
    # change_job_status
    path('change_job_status', views.change_job_status),
    # edit job
    path('edit_job/<int:job_id>/', views.edit_job, name='edit_job'),
   path('activate_card', views.activate_card, name='activate_card'),
    path('deactivate_card', views.deactivate_card, name='deactivate_card'),
    # emp
    path('disable_emp/<int:staff_id>/', views.disable_employee, name='disable_employee'),
    path('enable_emp/<int:staff_id>/', views.enable_employee, name='enable_employee'),
    #applicant
    path('disable_app', views.disable_applicant, name='disable_applicant'),
    path('enable_app', views.enable_applicant, name='enable_applicant'),
    #event
    path('disable_event', views.disable_event),
    path('enable_event', views.enable_event,),
    # plan
    path('disable_plan', views.disable_plan),
    path('enable_plan', views.enable_plan),
    # edit_staff
    # edit_staff/{{i.id}}
    path('edit_staff/<int:staff_id>/', views.edit_staff, name='edit_staff'),
    #update_staff
    path('update_staff', views.update_staff, name='update_staff'),
    # edit_app
    # edit_app/{{i.id}}
    path('edit_app/<int:app_id>/', views.edit_app, name='edit_app'),
    # update_applicant
    path('edit_app/update_applicant', views.update_applicant, name='update_applicant'),
    # http://127.0.0.1:8000/edit_event/
    path('edit_event/<int:event_id>/', views.edit_event, name='edit_event'),

    # /submit_job_time
    path('submit_job_time', views.submit_job_time),
    

    
]
