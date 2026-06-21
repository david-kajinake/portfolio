from django.shortcuts import render , redirect , get_object_or_404
from django.http import HttpResponse
from . models import Project , Technology , Contacter , Message , Service , MyPhoneNumber , MyEmail , CustomQuestion
from utils import email_service
import os
from django.contrib import messages

# Create your views here.
def home(request):
    return render(request , "portfolio/index.html")

def services(request):
    services = Service.objects.all()
    return render(request , "portfolio/services.html" ,
    {
        "services": services
    }
    )

def projects(request):
    projects = Project.objects.all()
    return render(request , "portfolio/projects.html",{
        "projects": projects, 
    })

def project_detail(request , project_id):
    project = get_object_or_404(Project , id = project_id)
    other_projects = Project.objects.exclude(id = project.id)
    return render(request, "portfolio/project-detail.html",{
        "project": project , 
        "other_projects": other_projects
    })


def resume(request):
    return render(request , "portfolio/resume.html")

def contact(request):
    if request.method == "POST":
        contact_name = request.POST.get("name")
        contact_email = request.POST.get("email")
        contact_message = request.POST.get("message")
        
        #Create a Contacter instance in the DB
        #Check whether the email doesn't exist in the DB 
        try:
            contacter = get_object_or_404( Contacter , email = contact_email )
            message = Message.objects.create(
                contacter = contacter ,
                content = contact_message
            )
        except Exception as e:
            contacter = Contacter.objects.create(
                name = contact_name ,
                email = contact_email
            )
            message = Message.objects.create(
                contacter = contacter ,
                content = contact_message
            )

      #SEND EMAIL TO THE CONTACTER
        try:   
            email_service.send_email( 
                                     email_type= "contact_auto_reply" ,  
                                     receiver_email = contact_email , 
                                     receiver_name = contact_name ,
                                       
                                     )
    
            messages.info(request , "Your message has been received. Check your email's inbox for further details.")
        except Exception as e:
            messages.error(request , f"Email not sent. Please try again")
            return
        #SEND EMAIL TO THE DEVELOPER
        try:
            email_service.notify_developer(
                                        email_type="contact_auto_reply" ,
                                        visitor_name= contact_name , 
                                        visitor_email_address= contact_email ,
                                        visitor_message= contact_message , 
                                        )
            return redirect("contact")
        
        except Exception as e:
            return redirect("contact")


    #If the redirection is comming from submitted form
    return render(request , "portfolio/contact.html",{
        #"latest_message": latest_message , 
       # "messages_exists": messages_exists
    })

def faqs(request):
    if request.method == "POST":
        user_email = request.POST.get("user-email")
        question_content = request.POST.get("custom-question")

        custom_question = CustomQuestion.objects.create(
            user_email = user_email , 
            question = question_content , 
        )
        #Email the user and the Developer
        try:
            predicted_sender_name = user_email.split("@")[0]
            email_service.send_email( 
                                    email_type= "faq_auto_reply" , 
                                    receiver_email= user_email , 
                                    receiver_name= predicted_sender_name ,             
                                    )
            messages.info(request, f"Your Inquiry was successsfully sent. Check your email's inbox for further details")
        except Exception as e:
            messages.error(request, "Message not sent. Please try again")
            return redirect("faqs")
        
        email_service.notify_developer( 
                                       email_type= "faq_auto_reply" , 
                                       visitor_name= predicted_sender_name , 
                                       visitor_email_address= user_email , 
                                       visitor_message= question_content ,
                                       )
        return redirect("faqs")

    return render(request , "portfolio/faqs.html")  