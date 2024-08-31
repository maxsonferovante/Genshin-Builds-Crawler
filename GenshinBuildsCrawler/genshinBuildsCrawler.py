import logging

from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(message)s',
    level=logging.INFO)


class GenBuildsCrawler:
    def __init__(self, url):
        self.url = self.validate_url(url)
        self.dictWeapon = {}
        self.dictCharacter = {}

        self.__responseHTML = None
        self.__objectHTML = None

    def download_url(self):
        try:
            logging.info(f'Crawling: {self.url}')
            self.__responseHTML = requests.get(self.url).text
            logging.info(f'Crawling Success in: {self.url}')
            return True
        except requests.RequestException:
            logging.info(f'Failed Crawling in: {self.url}')
            return False

    def get_information_response_html(self):
        logging.info(f'Get Information Response.')
        self.__objectHTML = BeautifulSoup(self.__responseHTML, 'html.parser')
        logging.info(f'Get Information Response Success.')

        self.get_dict_dungeon()
        self.get_dict_weapon()
        self.get_dict_character()

    def get_dict_dungeon(self):
        logging.info(f'Get Dungeon in object bs4.')
        for tr_item in self.__objectHTML.find_all('tr', class_='border-b border-gray-700 pt-2 align-middle'):
            self.dictWeapon[tr_item.td.h3.text] = []
        logging.info(f'Get Dungeon in object bs4 success.')

    def get_dict_weapon(self):
        logging.info(f'Get Weapon in object bs4.')
        for td_item in self.__objectHTML.find_all('tr', class_='border-b border-gray-700 pt-2 align-middle'):

            child_td_item = td_item.find_all('td')

            if len(child_td_item) >= 2:
                key = child_td_item[0].find('h3', class_='text-lg text-gray-200').get_text()
                for value in child_td_item[1].find_all('a'):
                    self.dictWeapon[key].append(
                        {
                            'name': value['href'].replace('/pt/weapon/', '').replace('_', ' ').title(),
                            'url': urljoin(self.url, value.get('href')),
                            'img': self.get_img_weapon(value['href'])
                        }
                    )

        logging.info(f'Get Weapon in object bs4 success.')

    def get_dict_character(self):
        logging.info(f'Get Character in object bs4.')
        
        weapon = self.__objectHTML.find_all('tr', class_='border-b border-gray-700 pt-2 align-middle')
        
        for td_item in self.__objectHTML.find_all('tr'):
            # o td_item não pode estar no array weapon
            if td_item in weapon:
                continue
            child_td_item = td_item.find_all('td')

            if len(child_td_item) == 2:
                key = child_td_item[0].find('h3', class_='text-lg text-gray-200').get_text()
                for value in child_td_item[1].find_all('a'):
                    
                    self.dictCharacter[key] = {
                        'name': value['href'].replace('/pt/character/', '').replace('_', ' ').title(),
                        'url': urljoin(self.url, value.get('href')),
                        'img': self.get_img_character(value['href'])
                    }
        logging.info(f'Get Character in object bs4 success.')
    @staticmethod
    def get_img_weapon(path):
        # pt/weapon/harbinger_of_dawn
        # https://i2.wp.com/genshinbuilds.aipurrjects.com/genshin/weapons/harbinger_of_dawn.png?strip=all&quality=100&w=80
        logging.info(f'Get Img Weapon in object bs4.')

        path_in_page = 'https://i2.wp.com/genshinbuilds.aipurrjects.com/genshin/weapons/' +  path.replace('pt/weapon/',
                                                                                                         '') + '.png?strip=all&quality=100&w=80'
        logging.info(f'Get Img Weapon in object bs4 success.')
        return path_in_page

    @staticmethod
    def get_img_character(path):
        # pt/character/amber
        # https://i2.wp.com/genshinbuilds.aipurrjects.com/genshin/characters/raiden_shogun/image.png?strip=all&quality=100&w=80
    
        path_in_page = 'https://i2.wp.com/genshinbuilds.aipurrjects.com/genshin/characters/' + path.split('/')[-1] + '/image.png?strip=all&quality=100&w=80'
        return path_in_page     
        
    @staticmethod
    def validate_url(url):
        if url is None:
            raise ValueError('URL is None')
        if not isinstance(url, str):
            raise ValueError('URL is not string')
        if url == '':
            raise ValueError('URL is empty')
        if not url.startswith('http') or not url.startswith('https'):
            raise ValueError('URL is not valid')
        if url.endswith('/'):
            return url[:-1]
        return url

