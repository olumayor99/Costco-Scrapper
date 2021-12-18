import requests
from datetime import date
from bs4 import BeautifulSoup as bs

i = 1

header = {
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'DNT': '1',
        'Upgrade-Insecure-Requests': '1',
        # You may want to change the user agent if you get blocked
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',

        'Referer': 'https://www.booking.com/index.en-gb.html',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }

#loop through and scrape each url
while True:
    url = f"https://www.costco.ca/CatalogSearch?currentPage={i}&dept=All&pageSize=24&keyword=*&langId=-24"
    
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

                #write scraped urls to file
                today = str(date.today()).replace('-', '').replace(':', '')
                file_name = today + '.txt'
                myfile = open(file_name, 'a')
                product_info = name_of_product[j] + ', ' + prices[j] + ', ' + product_link[j]
                myfile.write("%s\n" % product_info)
                myfile.close()

        i += 1

browser.close()

#input("Press any key to continue...")
