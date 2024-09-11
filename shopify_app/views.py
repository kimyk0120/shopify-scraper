import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .scraper import products as scraper


# Create your views here.
def index(request):
    return render(request, 'index.html')



@csrf_exempt
def scrape(request):
    if request.method == 'POST':

        # get parameters from request body
        request_body = request.body.decode('utf-8')
        req_json_data = json.loads(request_body)
        print("req_json_data: ", req_json_data)

        url = req_json_data['url']

        if not url:
            return JsonResponse({"error": "Invalid request body"}, status=400)

        products_json_list = scraper.get_all_products_by_req(url)
        jsonData = scraper.get_parse_data(products_json_list)

        return render(request, 'products.html', {'data': jsonData})
    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)
