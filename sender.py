import smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

csv_name = 'name_of_file.csv'

if 'promo' in csv_name:
    subject = " Promo"
else:
    subject = " Scrape"

body = "This is an automated email from the scrapper hosted on GCP. The results are attached to this email. Check for a csv file with today's date as the file name"
sender_email = "SENDER@gmail.com"
receiver_email = "RECEIVER@gmail.com"
password = "PASSWORD"

message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = subject
message["Bcc"] = receiver_email

message.attach(MIMEText(body, "plain"))


with open(csv_name, "rb") as attachment:
    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment.read())
  
encoders.encode_base64(part)

part.add_header(
    "Content-Disposition",
    f"attachment; filename= {csv_name}",
)

message.attach(part)
text = message.as_string()

context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, text)
