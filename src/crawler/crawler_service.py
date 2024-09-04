from nest.core import Injectable
from src.config import configs
from .crawler_model import EnumCrawler, Item, MemberTeam, TeamsResponse, WeaponsResponse, CharacterResponse, DungeonsResponse

from datetime import datetime
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
        
        self.__last_datetime_updated = None
    
    
    def get_weapon(self,option: EnumCrawler) -> WeaponsResponse:
        
        self.__download_url()
        self.__get_information_response_html()
        
        objectResponse = WeaponsResponse()
        
        objectResponse.option = option
        
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
    
    def get_character(self, option: EnumCrawler) -> CharacterResponse:
        
        self.__download_url()
        self.__get_information_response_html()
        
        objectResponse = CharacterResponse()
        
        objectResponse.option = option
        
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

    def get_dungeon(self) -> DungeonsResponse:
        self.__download_url()
        self.__get_information_response_html()
        
        objectResponse = DungeonsResponse()
        objectResponse.option = EnumCrawler.DUNGEON
        objectResponse.data['Weapons'] = []
        objectResponse.data['Characters'] = []
        
        
        weapon = self.__objectHTML.find_all('tr', class_='border-b border-gray-700 pt-2 align-middle')        
        
        for tr_item in self.__objectHTML.find_all('tr'):
            
            child_td_item = tr_item.find_all('td')
            quantity = len(child_td_item[1].find_all('a')) if  len(child_td_item) >=2 else 0 
            
            if tr_item in weapon:                
                objectResponse.data['Weapons'].append({
                    'name': tr_item.td.h3.text,
                    'quantity': quantity
                })        
            else:
                objectResponse.data['Characters'].append({
                    'name': tr_item.td.h3.text,
                    'quantity': quantity
                })
        
        return objectResponse
    
    def get_teams(self):
        self.__download_url(self.url_base + '/teams')
        self.__get_information_response_html()
        return []        
    
    def __download_url(self, url = None):
        try:
            if self.__available_update():
                url_final = url if url is not None else self.url_base
                self.__responseHTML = requests.get(url_final, timeout=30).text  
                self.__updated_last_datetime()
            else:
                print('No update available')
                
                                     
        except requests.RequestException as e:
            print(f'Error: {e}')
            raise e

    def __get_information_response_html(self):
        self.__objectHTML = BeautifulSoup(self.__responseHTML, 'html.parser')

    def __available_update(self):
        
        if self.__last_datetime_updated is None:
            return True
        
        datetime_now = datetime.now()
        difference = (datetime.now() - self.__last_datetime_updated).seconds
        
        print (f'Datetime now: {datetime_now} - Last update: {self.__last_datetime_updated} - Difference: {difference}')
    
        
        if difference > 60:
            print('Update available')
            return True
        print ('Update not available')
        return False
    
    def __updated_last_datetime(self):
        self.__last_datetime_updated = datetime.now()
        print (f'Last update: {self.__last_datetime_updated}')
    
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
