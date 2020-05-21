from django.core.management.base import BaseCommand

from market.models import Category, SubCategory, PhoneNumber, Enterprise

import os
import requests
from bs4 import BeautifulSoup as bs
import lxml
import shutil
from mysite.settings import BASE_DIR


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
        except FileNotFoundError as e:
            print(e)

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
                print(new_url)
                catalog = requests.get(new_url)
                new_soup = bs(catalog.text, 'lxml')
                div = new_soup.find_all('div', {'class': 'teaser-item'})
                for item in div:
                    pass
        print('FINISH')
