from selenium import webdriver
from time import sleep
from PIL import Image
from requests import get
from io import BytesIO
from itertools import count
from sys import argv
from bs4 import BeautifulSoup

if len(argv) == 1:
    print('No arguments, aborting...')
    exit()
elif not argv[1].startswith('https://www.scribd.com/document/'):
    print('The argument that you passed is invalid!')
    print('It must begin with "https://www.scribd.com/document/"')
    exit()
else:
    URL = argv[1]

options = webdriver.FirefoxOptions()
options.add_argument('--headless')

driver = webdriver.Firefox(firefox_options=options)
driver.get(URL)

pages = []
for i in count(1):
    try:
        page = driver.find_element_by_id('outer_page_'+str(i))
    except Exception as e:
        print(e)
        break
    soup = BeautifulSoup(page.get_attribute('innerHTML'), 'html.parser')
    page = soup.select('.absimg')[0]['src']
    pages.append(page)
    print(page)
    sleep(0.3)
    driver.execute_script("scroller = window.document.querySelector('.document_scroller');scroller.scrollBy(0, 2000);")

if len(pages) == 0:
    print('Could not find any image, aborting.')
    exit()

imgs = []
for i, page in enumerate(pages):
    response = get(page)
    img = Image.open(BytesIO(response.content))
    imgs.append(img)

imgs[0].save((URL.split('/')[-1] + '.pdf'), save_all=True, append_images=imgs[1:])