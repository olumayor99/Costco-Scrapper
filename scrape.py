import csv
import requests
from datetime import datetime
from bs4 import BeautifulSoup as bs
import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

i = 1
collected_data = []
filename = []
now = datetime.now()
dt = now.strftime("%d/%m/%Y %H:%M:%S")
today = str(dt).replace('-', '').replace(':', '').replace(' ', '').replace('/', '')
filename.append(today)
csv_name = filename[0] + '.csv'
file_name = filename[0] + '.txt'

subject = dt + " Costco.ca Scrape"
body = "This is an automated email from the scrapper hosted on GCP. The results are attached to this email. Check for a csv file with today's date as the file name"
sender_email = "sender@gmail.com"
receiver_email = "reciever@gmail.com"
password = "password"

message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = subject
message["Bcc"] = receiver_email 


header = {
    "User-Agent":
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
        "authority": "www.costco.ca", 
        "X-Requested-With": "XMLHttpRequest"
    }

while True:
    url = f"https://www.costco.ca/CatalogSearch?currentPage={i}&dept=All&pageSize=24&keyword=*&langId=-24"
    #url = f"https://www.costco.ca/CatalogSearch?currentPage={i}&dept=All&pageSize=24&keyword=holiday"    
    browser = requests.get(url, headers=header)
    scrapped_data = browser.content
    soup = bs(scrapped_data, 'html.parser')

    if soup.find_all("span", class_ = "description") == []:
        break
    else:
        caption = soup.find_all("div", attrs={'class':'caption'})

        name_of_product = []
        prices = []
        product_link = []
        j = 0

        for price in soup.find_all("div",attrs={'class':'price'}):
            prices.append(price.text.replace("\n","").replace("\t",""))
            
        for product_name in soup.find_all("span",attrs={'class':'description'}):
            name_of_product.append(product_name.text.replace("\n","").replace("\t",""))
            
        for product_url in soup.find_all('a',attrs={'tabindex':0}, href=True):
            product_link.append(product_url["href"])

        product_array = zip(prices, name_of_product, product_link)
        array_length = len(prices)

        for j in range(array_length):
            if '.97' in prices[j]:
                myfile = open(file_name, 'a')
                product_info = name_of_product[j] + ', ' + prices[j] + ', ' + product_link[j]
                myfile.write("%s\n" % product_info)
                myfile.close()

                field_names = ["Name", "Price", "Link"]
                collected_data = collected_data+[
                    {
                        "Name": name_of_product[j],
                        "Price": prices[j],
                        "Link": product_link[j]
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