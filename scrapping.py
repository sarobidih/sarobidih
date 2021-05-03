import urllib
from bs4 import BeautifulSoup
import requests

def scrapping_harenantsika_product (search_term):
    product_list = []
    try:
        url = 'https://nyharenantsika.com/fr/recherche?controller=search&orderby=position&orderway=desc&search_query_cat=2&search_query={}&submit_search='.format(search_term)

        # Perform the request
        request = urllib.request.Request(url)

        # Set a normal User Agent header, otherwise Google will block the request.
        request.add_header('User-Agent',
                           'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36')
        raw_response = urllib.request.urlopen(request).read()
        html = raw_response.decode("utf-8")
        soup = BeautifulSoup(html, 'html.parser')
        divs = soup.select("div.product-container")
        for div in divs:
            product_item = []
            for link in div.select('a.product_img_link', title=True):
                title = link.get('title')
                product_item.append(title)
            for prices in div.select('span.price'):
                price = prices.text
                product_item.append(price)
            for descriptions in div.select('p.product-desc'):
                desc = descriptions.text
                product_item.append(desc)
            for images in div.select('img.replace-2x'):
                img = images.get('data-original')
                product_item.append(img)
            for link in div.select('a.product_img_link', href=True):
                lien = link.get("href")
                product_item.append(lien)
            product_list.append(product_item)

        return product_list

    except:
        raise Exception("Erreur")
if __name__ == '__main__':
    results = scrapping_harenantsika_product("sac")
    print(len(results))
    for ressult in results:
        title = ressult[0]
        price = ressult[1]
        desc = ressult[2]
        img= ressult[3]
        lien = ressult[4]
        print(title)
        print(price)
        print(desc)
        print(img)
        print(lien)