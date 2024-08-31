from nest.core import Injectable
from src.config import configs

from .crawler_model import EnumCrawler, CrawlerResponse, Item

from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests

@Injectable
class CrawlerService:

    def __init__(self):
        self.database = []
        self.url_base = configs['url_base']
        
        self.__responseHTML = None
        self.__objectHTML = None

    def run(self, option: EnumCrawler) -> CrawlerResponse:
        self.__download_url()
        self.__get_information_response_html()
        
        if option == EnumCrawler.WEAPON:
        
            result = self.__get_dict_weapon()
            result.option = option
            return result
        
        elif option == EnumCrawler.CHARACTER:
            
            result = self.__get_dict_character()
            result.option = option
            return result
            
        else:
            raise ValueError('Option not found')
            
    
    def __download_url(self):
        try:
            self.__responseHTML = requests.get(self.url_base, timeout=30).text       
        
        except requests.RequestException as e:
            print(f'Error: {e}')
            raise e

    def __get_information_response_html(self):
        self.__objectHTML = BeautifulSoup(self.__responseHTML, 'html.parser')


    def __get_dict_dungeon(self):

        for tr_item in self.__objectHTML.find_all('tr', class_='border-b border-gray-700 pt-2 align-middle'):
            self.dictWeapon[tr_item.td.h3.text] = []


    def __get_dict_weapon(self) -> CrawlerResponse:
        objectResponse = CrawlerResponse()
        
        for td_item in self.__objectHTML.find_all('tr', class_='border-b border-gray-700 pt-2 align-middle'):

            child_td_item = td_item.find_all('td')

            if len(child_td_item) >= 2:
                key = child_td_item[0].find('h3', class_='text-lg text-gray-200').get_text()
                objectResponse.data[key] = []
                for value in child_td_item[1].find_all('a'):
                    
                    objectResponse.data[key].append(Item(
                                                name = value['href'].replace('/pt/weapon/', '').replace('_', ' ').title(),
                                                url = urljoin(self.url_base, value.get('href')),
                                                img = self.__get_img_weapon(value['href'])))

        return objectResponse
    
    def __get_dict_character(self) -> CrawlerResponse:
        objectResponse = CrawlerResponse()
        
        weapon = self.__objectHTML.find_all('tr', class_='border-b border-gray-700 pt-2 align-middle')
        
        for td_item in self.__objectHTML.find_all('tr'):
            # o td_item não pode estar no array weapon
            if td_item in weapon:
                continue
            child_td_item = td_item.find_all('td')

            if len(child_td_item) == 2:
                key = child_td_item[0].find('h3', class_='text-lg text-gray-200').get_text()
                objectResponse.data[key] = []
                for value in child_td_item[1].find_all('a'):
                    objectResponse.data[key].append(Item(
                        name = value['href'].replace('/pt/character/', '').replace('_', ' ').title(),
                        url = urljoin(self.url_base, value.get('href')),
                        img = self.__get_img_character(value['href'])))
        
        return objectResponse

    def __get_img_weapon(self,path):
        # pt/weapon/harbinger_of_dawn
        # https://i2.wp.com/genshinbuilds.aipurrjects.com/genshin/weapons/harbinger_of_dawn.png?strip=all&quality=100&w=80
        path_in_page = 'https://i2.wp.com/genshinbuilds.aipurrjects.com/genshin/weapons/' +  path.replace('pt/weapon/',
                                                                                                         '') + '.png?strip=all&quality=100&w=80'
        return path_in_page

    def __get_img_character(self,path):
        # pt/character/amber
        # https://i2.wp.com/genshinbuilds.aipurrjects.com/genshin/characters/raiden_shogun/image.png?strip=all&quality=100&w=80    
        path_in_page = 'https://i2.wp.com/genshinbuilds.aipurrjects.com/genshin/characters/' + path.split('/')[-1] + '/image.png?strip=all&quality=100&w=80'
        return path_in_page     
