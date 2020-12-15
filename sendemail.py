import smtplib
from validate_email import validate_email
from email.message import EmailMessage

def send_mail(remail,hint):
    if validate_email(remail) is True:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.ehlo()

        server.login("thetenpostmail@gmail.com", "amoldada23")
        msg = EmailMessage()
        msg.set_content(f'We do not store any passwords for security reasons. Below is the hint hope it helps.\n Hint:{hint}')

        msg['Subject'] = 'EtchGuard Password Hint'
        msg['From'] = "thetenpostmail@gmail.com"
        msg['To'] = remail
        try:
            server.send_message(msg)
            server.quit()
            return f"Email with Hint was Sent to {remail}"

        except:
            return "An error ocuured."
    else:
        return "Please Enter A Valid Email."
    




