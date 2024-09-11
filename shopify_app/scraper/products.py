import json
import ssl
import urllib.request

from bs4 import BeautifulSoup

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'


def get_all_products_by_req(url):
    page = 1
    products_json_list = []
    while True:
        url = url + '/products.json?limit=250&&page={}'.format(page)
        req = urllib.request.Request(
            url,
            data=None,
            headers={
                'User-Agent': USER_AGENT
            }
        )
        data = urllib.request.urlopen(req, context=ssl_context).read()

        products = json.loads(data.decode())['products']
        if not products:
            break

        for product in products:
            products_json_list.append(product)

        page += 1

    return products_json_list


def get_parse_data(products_list):
    result_json = []
    for product in products_list:

        # title
        title = product['title']
        description_body = product['body_html']

        soup = BeautifulSoup(description_body, 'html.parser')

        # description
        description = ""
        description_el = soup.find("p")
        if description_el:
            description = description_el.get_text().strip()
        else:
            description = soup.get_text().strip()

        description = description.replace('\n', '').replace('\t', '')
        description = description.replace(u'\xa0', u' ')
        description = description.replace(u'\u2028', u' ')

        # specs
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

        # price
        price = product['variants'][0]['price']

        # images
        images = product['images']
        image_urls = []
        for image in images:
            image_urls.append(image['src'])

        result_json.append({
            "title": title,
            "description": description,
            "specs": spec_json,
            "price": price,
            "image_urls": image_urls
        })
    return result_json
