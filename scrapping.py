import urllib
from bs4 import BeautifulSoup
import requests

def scrapping_harenantsika_product (search_term, max=15):
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
            if (len(product_list) < max):
                product_list.append(product_item)
            else :
                break

        return product_list

    except:
        raise Exception("Erreur")

def scrapping_harenantsika_magasin(search_term, max=15):
    product_list = []
    try:
        url = 'https://nyharenantsika.com/fr/recherche?controller=search&orderby=position&orderway=desc&search_query_cat=store&search_query={}&submit_search='.format(
            search_term)

        # Perform the request
        request = urllib.request.Request(url)

        # Set a normal User Agent header, otherwise Google will block the request.
        request.add_header('User-Agent',
                           'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36')
        raw_response = urllib.request.urlopen(request).read()
        html = raw_response.decode("utf-8")
        soup = BeautifulSoup(html, 'html.parser')
        divs = soup.select("li.shop_item")
        for div in divs:
            product_item = []
            for titles in div.select('div.logo'):
                for title in titles.select('a', title=True):
                    title = title.get('title')
                    product_item.append(title)

            for logos in div.select('div.logo'):
                for logo in logos.select('img'):
                    logo = logo.get('src')
                    product_item.append(logo)

            for descs in div.select('div.middle-side'):
                for desc in descs.select('p'):
                    desc = desc.text
                    product_item.append(desc)

            for links in div.select('div.middle-side'):
                for link in links.select('a', href = True):
                    link = link.get('href')
                    product_item.append(link)

         #   for prices in div.select('span.price'):
             #   price = prices.text
              #  product_item.append(price)
            #for descriptions in div.select('p.product-desc'):
             #   desc = descriptions.text
              #  product_item.append(desc)
            #for images in div.select('img.replace-2x'):
             #   img = images.get('data-original')
              #  product_item.append(img)
            #for link in div.select('a.product_img_link', href=True):
             #   lien = link.get("href")
              #  product_item.append(lien)
            if (len(product_list) < max):
                product_list.append(product_item)
            else:
                break

        return product_list

    except:
        raise Exception("Erreur")

if __name__ == '__main__':
    results = scrapping_harenantsika_magasin("harena")
    print(len(results))
    print(results)
    for result in results:
        title = result[0]
        img = result[1]
        desc = result[2]
        link = result[3]

