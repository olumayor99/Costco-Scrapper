import csv
import requests
from datetime import datetime
from bs4 import BeautifulSoup as bs
import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

promo = []
prices = []
i = 1
collected_data = []
filename = []
promo = []
now = datetime.now()
dt = now.strftime("%d/%m/%Y %H:%M:%S")
today = str(dt).replace('-', '').replace(':', '').replace(' ', '').replace('/', '')
filename.append(today)
csv_name = filename[0] + 'promo.csv'
file_name = filename[0] + 'promo.txt'

subject = dt + " Scrape"
body = "This is the list of products on promo today."
sender_email = "oom.taiwo@gmail.com"
receiver_email = "olumayoor99@gmail.com"
password = "!987!61255"

message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = subject
message["Bcc"] = receiver_email 

header = {
    "User-Agent":
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
        "authority": "www.google.com", 
        "X-Requested-With": "XMLHttpRequest"
    }

while True:
    url = f"https://www.costco.ca/CatalogSearch?currentPage={i}&dept=All&pageSize=24&keyword=*&langId=-24"
    browser = requests.get(url, headers=header)
    scrapped_data = browser.content
    soup = bs(scrapped_data, 'html.parser')

    if soup.find_all("span", class_ = "description") == []:
        break
    else:

        caption = soup.find_all("div",attrs={'class':'product'})

        for c in caption:
            try:
                price = c.find("div",attrs={'class':'price'}).text.replace("\n","").replace("\t","")
            except Exception as e:
                promo = "No Price"
            name = c.find("span",attrs={'class':'description'}).text.replace("\n","").replace("\t","")
            url_link = c.find('span',attrs={'class':'description'}).a["href"]
            
            try:
                promo = c.find('p', attrs={'class':'promo'}).string
            except Exception as e:
                promo = "Normal"
            if 'OFF' in promo:
                myfile = open(file_name, 'a',encoding='utf-8')
                product_info = name + ', ' + price + ', ' + url_link
                myfile.write("%s\n" % product_info)
                myfile.close()

                field_names = ["Name", "Price", "Link"]
                collected_data = collected_data+[
                    {
                        "Name": name,
                        "Price": price,
                        "Link": url_link
                    }
                ]
                with open(csv_name, 'w', newline='',encoding='utf-8') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=field_names)
                    writer.writeheader()
                    for k in collected_data:
                        writer.writerow(k)
        i += 1

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