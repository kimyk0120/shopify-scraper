import csv
import json
import os
import ssl
import urllib.request

from bs4 import BeautifulSoup

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'

end_page = 21  # 페이지가 어디까지 인지  확인 필요
csv_file_path = '../output/dannysvintagewatches_products_20240909.csv'

# Check if the file exists
file_exists = os.path.isfile(csv_file_path)

with open(csv_file_path, 'a', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)

    # If the file does not exist, write the header
    if not file_exists:
        csv_writer.writerow(['Title', 'Description', 'Specs', 'Price', "Images"])

    for page in range(1, end_page + 1):
        url = "https://dannysvintagewatches.com/collections/wear-a-piece-of-history-shop-watches/products.json?limit=250&&page={}".format(
            page)

        req = urllib.request.Request(
            url,
            data=None,
            headers={
                'User-Agent': USER_AGENT
            }
        )

        data = urllib.request.urlopen(req, context=ssl_context).read()
        products = json.loads(data.decode())['products']

        for product in products:
            title = product['title']
            description_body = product['body_html']

            soup = BeautifulSoup(description_body, 'html.parser')

            description = ""
            description_el = soup.find("p")
            if description_el:
                description = description_el.get_text().strip()
            else:
                description = soup.get_text().strip()

            # description2_p = soup.find_all("p")[1].get_text()
            # description = description + description2_p
            description = description.replace('\n', '').replace('\t', '')
            # remove nbsp
            description = description.replace(u'\xa0', u' ')
            # remove lsep
            description = description.replace(u'\u2028', u' ')

            specs_tr = soup.find_all("tr")
            spec_json = {}
            for spec in specs_tr:
                th_els = spec.find_all("th")
                td_els = spec.find_all("td")
                if len(th_els) > 0:
                    key = th_els[0].get_text()
                    value = th_els[1].get_text()
                    spec_json[key] = value
                else:
                    key = td_els[0].get_text()
                    value = td_els[1].get_text()
                    spec_json[key] = value

            specs = json.dumps(spec_json)

            price = product['variants'][0]['price']

            images = product['images']
            image_urls = []
            for image in images:
                image_urls.append(image['src'])

            csv_writer.writerow([title, description, specs, price, image_urls])

print("end of script")
