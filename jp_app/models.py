from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Applicant(models.Model):
    uid = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    App_Username = models.CharField(max_length=150,default='georgeksaji14@gmail.com')
    App_Fname = models.CharField(max_length=10)
    App_Lname = models.CharField(max_length=10)
    App_Phone = models.CharField(max_length=20)
    App_DOB = models.DateField()
    App_Education = models.CharField(max_length=30)
    App_Emp_Status = models.CharField(max_length=25)
    App_LinkedIn = models.CharField(max_length=200, blank=True, null=True)
    App_Image = models.CharField(max_length=200)
    App_Hname = models.CharField(max_length=20)
    App_Gender = models.CharField(max_length=10)
    App_Street = models.CharField(max_length=200)
    App_Dist = models.CharField(max_length=30)
    App_Pin = models.IntegerField()
    App_Date = models.DateField(default=timezone.now)
    App_Resume = models.CharField(max_length=100)
    App_Status = models.BooleanField(default=True)


class Employer(models.Model):
    uid = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    Emp_Username = models.CharField(max_length=150,default='lulu@gmail.com')
    Emp_Firm = models.CharField(max_length=150)
    Emp_Phone = models.CharField(max_length=10)
    Emp_Street = models.CharField(max_length=150)
    Emp_Dist = models.CharField(max_length=30)
    Emp_State = models.CharField(max_length=25, default='Kerala')
    Emp_Pin = models.IntegerField()
    Emp_Image = models.CharField(max_length=200)
    Emp_Date = models.DateField(default=timezone.now)
    Emp_Status = models.BooleanField(default=True)

class Staff(models.Model):
    uid = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    Staff_Username=models.CharField(max_length=150,default='jeffrey@gmail.com')
    Staff_Fname = models.CharField(max_length=20)
    Staff_Lname = models.CharField(max_length=20)
    Staff_Phone = models.CharField(max_length=20)
    Staff_DOB = models.DateField()
    Staff_Hname = models.CharField(max_length=30)
    Staff_Gender = models.CharField(max_length=10)
    Staff_Street = models.CharField(max_length=20)
    Staff_Dist = models.CharField(max_length=25)
    Staff_Pin = models.IntegerField()
    Staff_Date = models.DateField(default=timezone.now)
    Staff_Status = models.BooleanField(default=True)

class Job(models.Model):
    Employer_id = models.ForeignKey(Employer, on_delete=models.CASCADE, null=True)
    EM_Username =models.CharField(max_length=150,default='lulu@gmail.com')
    Job_Title = models.CharField(max_length=150)
    Job_Mode = models.CharField(max_length=15)
    Job_Location = models.CharField(max_length=150, blank=True, null=True)
    Job_Seats = models.IntegerField(default=0)
    Job_Time_Type = models.CharField(max_length=15)
    Job_Duration = models.IntegerField()
    Job_Start = models.TimeField(blank=True, null=True)
    Job_End = models.TimeField(blank=True, null=True)
    Min_Job_Days = models.IntegerField()
    Job_Day_Type = models.CharField(max_length=20)
    Job_App_End = models.DateField()
    Job_Description = models.CharField(max_length=1000)
    Job_City = models.CharField(max_length=20,default='Kochi')
    Job_State = models.CharField(max_length=20,default='Kerala')
    Job_Status = models.BooleanField(default=True)

class Job_application(models.Model):
    Job_ID = models.ForeignKey(Job, on_delete=models.CASCADE, null=True)  
    Job_Applicant_ID = models.ForeignKey(Applicant, on_delete=models.CASCADE, null=True)
    Job_App_Date = models.DateField(default=timezone.now)
    Job_App_Status = models.CharField(max_length=15, default='Applied')
    Job_App_Interview_Date = models.DateField(blank=True, null=True)
    Job_App_Interview_Time = models.TimeField(blank=True, null=True)
    Job_App_Meeting_Link = models.CharField(max_length=200, blank=True, null=True)
    Job_App_Description = models.CharField(max_length=100, blank=True, null=True)

    # applicant can review employer
class Review(models.Model):
    Reviewer_ID = models.ForeignKey(Applicant, on_delete=models.CASCADE, null=True)
    Reviewee_ID = models.ForeignKey(Employer, on_delete=models.CASCADE, null=True)
    Ratings = models.DecimalField(max_digits=2, decimal_places=1)
    Review_Date = models.DateField(default=timezone.now)
    Description = models.CharField(max_length=100, blank=True, null=True)
    Application_id = models.ForeignKey(Job_application, on_delete=models.CASCADE, null=True)

class Plan(models.Model):
    Staff_ID = models.ForeignKey(Staff, on_delete=models.CASCADE, null=True)
    Plan_Title = models.CharField(max_length=20)
    Plan_Duration = models.CharField(max_length=8)
    Plan_Description = models.CharField(max_length=250)
    Date = models.DateField(default=timezone.now)
    Price = models.IntegerField()
    Plan_Status = models.BooleanField(default=True)
    Plan_Level = models.CharField(default='Basic', max_length=15)
    
class Pay_Card(models.Model):
    Card_Holder_Name = models.CharField(max_length=20)
    Applicant_ID = models.ForeignKey(Applicant, on_delete=models.CASCADE, null=True)
    Card_No = models.DecimalField(max_digits=16, decimal_places=0, unique=True)
    Exp_Date = models.DateField()
    Card_Status = models.IntegerField(default=1)

class Payment(models.Model):
    Plan_ID = models.ForeignKey(Plan, on_delete=models.CASCADE, null=True)
    Applicant_ID = models.ForeignKey(Applicant, on_delete=models.CASCADE, null=True)
    Card_ID = models.ForeignKey(Pay_Card, on_delete=models.CASCADE, null=True)
    Payment_Date = models.DateField(default=timezone.now)
    Expiry_Date = models.DateField(default=timezone.now)
    Total_Price = models.DecimalField(max_digits=10, decimal_places=2)

    
class Event(models.Model):
    Staff_ID = models.ForeignKey(Staff, on_delete=models.CASCADE, null=True)
    Staff_Username = models.CharField(max_length=150,default='admin@gmail.com')
    Event_Title = models.CharField(max_length=20)
    Event_Organizer = models.CharField(max_length=20)
    Event_Venue = models.CharField(max_length=150)
    Event_Street = models.CharField(max_length=20)
    Event_Dist = models.CharField(max_length=25)
    Event_State = models.CharField(max_length=25)
    Event_Email = models.CharField(max_length=25)
    Event_Phone = models.DecimalField(max_digits=10, decimal_places=0)
    Event_Date = models.DateField()
    Event_Time = models.TimeField()
    Event_Description = models.CharField(max_length=150)
    Event_Status = models.BooleanField(default=True)


class Chat(models.Model):
    Chat_ID = models.CharField(max_length=7, primary_key=True)
    App_ID = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='chats_as_applicant')
    EM_ID = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='chats_as_employer')
    Chat_Date = models.DateField(default=timezone.now)
    Chat_Time = models.TimeField(default=timezone.now)
    Sender_status = models.BooleanField(default=True)
    # 0 for employer, 1 for applicant
    Chat_Matter = models.CharField(max_length=200)



