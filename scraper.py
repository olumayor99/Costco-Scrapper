import csv
from seleniumwire import webdriver 
from datetime import datetime
from bs4 import BeautifulSoup as bs


filename = []
now = datetime.now()
dt = now.strftime("%d/%m/%Y %H:%M:%S")
today = str(dt).replace('-', '').replace(':', '').replace(' ', '').replace('/', '')
filename.append(today)
csv_name = filename[0] + '.csv'
csv_promo = filename[0] + 'promo.csv'
file_name = filename[0] + '.txt'
file_promo = filename[0] + 'promo.txt'

i = 1
j = 0

header = {
        "User-Agent":
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }

fireFoxOptions = webdriver.FirefoxOptions()
fireFoxOptions.add_argument("--headless")
driver = webdriver.Firefox(options=fireFoxOptions)

def interceptor(request):
    del request.headers['Referer']  
    request.headers['Referer'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36'

driver.request_interceptor = interceptor

def promo():
    promo = []
    collected_data = []

    caption = soup.find_all("div",attrs={'class':'product'})

    for c in caption:
        try:
            price = c.find("div",attrs={'class':'price'}).text.replace("\n","").replace("\t","").replace(",","")
        except Exception as e:
            promo = "No Price"
        name = c.find("span",attrs={'class':'description'}).text.replace("\n","").replace("\t","").replace(",","")
        url_link = c.find('span',attrs={'class':'description'}).a["href"]
        
        try:
            promo = c.find('p', attrs={'class':'promo'}).string
        except Exception as e:
            promo = "Normal"
        if 'OFF' in promo:
            myfile = open(file_promo, 'a')
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
            with open(csv_promo, 'w', newline='',encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=field_names)
                writer.writeheader()
                for k in collected_data:
                    writer.writerow(k)

        elif '.97' in price:
            myfile = open(file_name, 'a')
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
            try:
                with open(csv_name, 'w', newline='',encoding='utf-8') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=field_names)
                    writer.writeheader()
                    for k in collected_data:
                        writer.writerow(k)
            except Exception as e:
                print("skipped")

while (True):
    url = f"https://www.costco.ca/CatalogSearch?currentPage={i}&dept=All&pageSize=24&keyword=*"
    #url = f"https://www.costco.ca/CatalogSearch?currentPage={i}&dept=All&pageSize=24&keyword=women"

    driver.get(url)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    html = driver.page_source
    soup = bs(html, 'html.parser')

    if soup.find_all("div",attrs={'class':'price'}) == []:
    #if i > m:
        print(i)
        break
    else:
        try:
            promo()
            print(i)

        except Exception as e:
            print("skipped")
    i += 1

driver.quit()