import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage

"""
emails come in various types: 
*faq_auto_reply , 
*contact_auto_reply email , 
*developer_manual_repy email
"""

def send_email( 
            email_type ,
            receiver_email , 
            receiver_name , 
            sender_name = "David Kajinake Schenezare" , 
            sender_email = "folkwinx@gmail.com" , 
            code = "pfma duds szop rxwe" , 
            manually_typed_message = None
            ):
    email = MIMEMultipart()
    email["From"] = sender_name
    email["To"] = receiver_name
    if email_type == "contact_auto_reply":
        email ["Subject"] = "E-MAIL SUCCESSFULLY RECEIVED"
        message = f"""
Hello {receiver_name} , Thank you for contacting me. Your message was successfully received , i will get back to you shortly. Thank you
"""
    
    elif email_type == "faq_auto_reply":
        email["Subject"] = "YOUR INQUIRY SUCCESSFULLY RECEIVED"
        message = f"""
Hello {receiver_name} , Thank you for inquiring from me ,i will shortly inform you when a reply for this inquiry is available. thank you
"""
        
    text_message = MIMEText(message , "plain")
    email.attach(text_message)
    letter = email.as_string()
    server = smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()
    attempts = 0
    while attempts < 5 :
        try:
            server.login(sender_email,code)
            break
        except Exception as e:
             print(f"Error connecting to the server {e}\nRetrying.....")
             attempts +=1
    try: 
        server.sendmail( sender_email , receiver_email , letter )
        server.quit()
    except Exception as e:
         
         print(f"Error occured trying to send an email: {e}")
         
    return{
        "contacter_email": receiver_email , 
        "contacter_name": receiver_name , 
        "contacter_message": message
    }

def notify_developer(
        visitor_name , 
        visitor_email_address ,
        visitor_message ,
        email_type ,
        self_email = "folkwinx@gmail.com",
        code ="pfma duds szop rxwe" 
                   ):
    if email_type == "contact_auto_reply":
        message_type = "contacted"
        action = "has contacted you"

    elif email_type == "faq_auto_reply":
        message_type ="asked a question"
        action = "has sent you an inquiry"

    email = MIMEMultipart()
    email["From"] = "Self"
    email["To"] = "Self"
    email["Subject"] = f"New person {visitor_name} {action}"
    body = f"""
A new person , with the email address '{visitor_email_address}' {action}.
Here is the message they sent:

{visitor_message}
""" 
    wrapped_body = MIMEText(body)
    email.attach(wrapped_body)
    email_to_send = email.as_string()
    server = smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()
    server.login(self_email,code)
    server.sendmail(self_email , self_email , email_to_send)
    server.quit()
