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
csv_file_path = '../output/belortimelegacy_products_20240908.csv'

# Check if the file exists
file_exists = os.path.isfile(csv_file_path)

with open(csv_file_path, 'a', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)

    # If the file does not exist, write the header
    if not file_exists:
        csv_writer.writerow(['Title', 'Description', 'Specs', 'Price', "Images"])

    for page in range(1, end_page + 1):
        url = "https://www.belortimelegacy.com/collections/shop/products.json?page={}".format(page)

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
            description = soup.find("p").get_text()
            description = description.replace('\n', '').replace('\t', '')

            specs_tr = soup.find_all("tr")
            spec_json = {}
            for spec in specs_tr:
                key = spec.find_all("td")[0].get_text()
                value = spec.find_all("td")[1].get_text()
                spec_json[key] = value

            specs = json.dumps(spec_json)
            price = product['variants'][0]['price']

            images = product['images']
            image_urls = []
            for image in images:
                image_urls.append(image['src'])

            csv_writer.writerow([title, description, specs, price, image_urls])

print("end of script")

if __name__ == '__main__':
    pass
    # parser = OptionParser()
    # parser.add_option("--list-collections", dest="list_collections",
    #                   action="store_true",
    #                   help="List collections in the site")
    # parser.add_option("--collections", "-c", dest="collections",
    #                   default="",
    #                   help="Download products only from the given collections (comma separated)")
    # (options, args) = parser.parse_args()
    # if len(args) > 0:
    #     url = fix_url(args[0])
    #     if options.list_collections:
    #         for col in get_page_collections(url):
    #             print(col['handle'])
    #     else:
    #         collections = []
    #         if options.collections:
    #             collections = options.collections.split(',')
    #         extract_products(url, 'products_all_20240907.csv', collections)
