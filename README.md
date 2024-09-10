# shopify-scraper (ing..)

[//]: # (Simple scraper to extract all products from shopify sites)
[//]: # (  row = {'sku': sku, 'product_type': product_type,)
[//]: # (                       'title': title, 'option_value': option_value,)
[//]: # (                       'price': price, 'stock': stock, 'body': str&#40;product['body_html']&#41;,)
[//]: # (                       'variant_id': product_handle + str&#40;variant['id']&#41;,)
[//]: # (                       'product_url': product_url, 'image_src': image_src})
[//]: # (description: html 구조가 제각각이라 위의 구조같이 정형화 된 것만 파싱한다. )
[//]: # ([![forthebadge]&#40;https://forthebadge.com/images/badges/open-source.svg&#41;]&#40;https://forthebadge.com&#41;)

[![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)](https://forthebadge.com)
[![pythonbadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)

This project is a web application that scrapes shopify products that provide public information. 

<img src="./intro.png"  alt="intro"/>

[//]: # ('Title', 'Description', 'Specs', 'Price' , "Images")
This scraper will extract publicly available data: 
- Title
- Description
- Specs
- Price
- Images

---

[//]: # (## Updated Features)

[//]: # (2024.09.04)
[//]: # (  - **Company Search:** You can search for a company and get all the employees' information.)


## Stacks
```angular2html
Django 5.0.7
Python 3.10.11
tailwindcss 3.0.0
beautifulsoup4 4.12.3
```
  
## How to Run 

- Clone the repository
- Install Requirements
```bash
$ pip install -r requirements.txt
```
-  Run Django Server
```bash
$ python manage.py runserver
```

- Tailwind Build (for dev)
```bash
$ npx tailwindcss -i ./static/src/input.css -o ./static/src/output.css --watch
```

## Contact

For any feedback or queries, please reach out to me at [kimyk0120@gmail.com](kimyk0120@gmail.com).

