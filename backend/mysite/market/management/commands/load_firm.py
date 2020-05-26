from django.core.management.base import BaseCommand

from market.models import Category, SubCategory, PhoneNumber, Enterprise

import requests
from bs4 import BeautifulSoup as bs
import lxml
import shutil
from mysite.settings import BASE_DIR
from django.core.files import File


class Command(BaseCommand):

    def handle(self, *args, **options):
        print('Clearing DB ...')
        # удаляем записи и картинки
        Category.objects.all().delete()
        SubCategory.objects.all().delete()
        PhoneNumber.objects.all().delete()
        Enterprise.objects.all().delete()
        try:
            shutil.rmtree(f'{BASE_DIR}/media/enterprises')
        except FileNotFoundError:
            pass

        # парсим главную страницу
        base_url = 'https://west-info.biz/'
        print(f'Start import from {base_url}')
        res = requests.get(base_url)
        soup = bs(res.text, 'lxml')

        # находим нужный контент
        categories = soup.find_all('li', {'class': 'submenu_item'})
        for i in categories[:5]:
            c = Category()
            c.name = i.find('a').text
            c.save()
            print(f'Import {c.name}')
            subcategories = i.find_all('a', {'class': 'sub2menu_link'})
            for k in subcategories:
                sub = SubCategory()
                sub.name = k.text
                sub.category = c
                sub.save()
                print(f'Import {sub.name}')
                new_url = f"https://west-info.biz{k['href']}"
                catalog = requests.get(new_url)
                new_soup = bs(catalog.text, 'lxml')
                div = new_soup.find_all('div', {'class': 'teaser-item'})
                for item in div:
                    firm_name = item.find('h2', {'class': 'pos-title'})
                    firm_description = item.find('p')
                    firm_city = item.find('div', {'class': 'element element-text'})
                    firm_adress = item.find_all('div', {'class': 'element element-text'})
                    firm_phones = item.find('div', {'class': 'element element-text last'})
                    a = item.find_all('img')
                    for aa in a:
                        print(aa['src'])

                    if firm_phones:
                        phones_list = firm_phones.text.replace(' ', '').replace(',', ' ').replace(';', ' ').split()
                    e = Enterprise()
                    if firm_name:
                        e.name = firm_name.text
                    if firm_description:
                        e.description = firm_description.text
                    if firm_city:
                        e.city = firm_city.text
                    if firm_adress and len(firm_adress) >= 2:
                        e.adress = firm_adress[1].text
                    else:
                        e.adress = 'Отсутствует'
                    p = PhoneNumber()
                    for z in phones_list:
                        p.number = z
                        p.save()
                        e.phone = p
                    e.category = c
                    e.sub_category = sub
                    e.save()
                    print(f'{e.name} save...')
        print('***FINISH***')
