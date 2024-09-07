import json
import ssl
import urllib.request
import shopify_app.utils.url_utils as url_utils

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'

# https://www.chrononation.com/collections.json?page=1&&limit=3

base_url = "www.chrononation.com"
base_url = url_utils.validate_url(base_url)

def get_all_products_by_req(url):
    page = 1
    collections = []
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

        products_json = json.loads(data.decode())['products']
        collections += products_json
        if not products_json:
            break
        page += 1

    return collections

products = get_all_products_by_req(base_url)


print("end of script")



