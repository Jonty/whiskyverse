import json
import requests
import lxml.html
from dateutil import parser as dp

whisky_pages = {}

for root, available in (
    ('https://www.smws.com/archive', False),
    ('https://www.smws.com/whisky', True)):

    req = requests.get(root)
    root_page = req.content

    root = lxml.html.document_fromstring(root_page)
    links = root.xpath('//span[contains(@class, "product-box--cask")]/../../..')
    for link in links:
        whisky_pages[link.attrib['href']] = available

whiskies = {}

for page, available in whisky_pages.items():
    whisky = {}
    req = requests.get(page)
    root_page = req.content
    root = lxml.html.document_fromstring(root_page)

    cask_string = root.xpath('//*[@id="product_addtocart_form"]/div/div[2]/div/div[1]/span[1]')
    if not cask_string:
        continue

    _, distillery, cask = cask_string[0].text.split('.')

    whisky = {
        'url': page,
        'name': root.xpath('//*[@id="product_addtocart_form"]/div/div[2]/div/div[1]/p')[0].text.strip(),
        'available': available,
        'distillery': distillery.strip(),
        'cask': cask.strip(),
        'type': root.xpath('//*[@id="product_addtocart_form"]/div/div[2]/div/div[1]/span[2]')[0].text,
        'age': int(root.xpath('//*[@id="product_addtocart_form"]/div/div[2]/div/div[3]/div[1]/span[2]')[0].text.replace(' Years', '').strip()),
        'date_distilled': str(dp.parse(root.xpath('//*[@id="product_addtocart_form"]/div/div[2]/div/div[3]/div[1]/span[4]')[0].text)),
        'cask_type': root.xpath('//*[@id="product_addtocart_form"]/div/div[2]/div/div[3]/div[2]/span[2]')[0].text,
        'region': root.xpath('//*[@id="product_addtocart_form"]/div/div[2]/div/div[3]/div[1]/span[8]')[0].text,
        'outturn': int(root.xpath('//*[@id="product_addtocart_form"]/div/div[2]/div/div[3]/div[2]/span[4]')[0].text.replace('1 of ','').replace(' bottles','')),
        'abv': float(root.xpath('//*[@id="product_addtocart_form"]/div/div[2]/div/div[3]/div[3]/span[1]')[0].text_content().replace('ABV: ', '').replace('%', '').strip()),
        'colour': root.xpath('//*[@id="product_addtocart_form"]/div/div[2]/div/div[3]/div[3]/span[4]')[0].text_content().replace('Colour: ', '').strip(),
        'image': root.xpath('//*[@id="product_addtocart_form"]/div/div[1]/section/div/figure/img')[0].attrib['src'],
        'description': root.xpath('//*[@id="further-details"]/div[1]')[0].text_content().strip(),
        'drinking_tip': root.xpath('//*[@id="further-details"]/div[2]/span[2]')[0].text_content().strip(),
    }

    whiskies[page] = whisky

print json.dumps(whiskies, sort_keys=True, indent=4, separators=(',', ': '))
