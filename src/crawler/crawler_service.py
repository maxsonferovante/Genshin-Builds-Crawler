from nest.core import Injectable
from src.config import configs
from .crawler_model import EnumCrawler, Item, MemberTeam, TeamsResponse, WeaponsResponse, CharacterResponse, DungeonsResponse, Team, ItemDungeon

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
        
    
    
    def get_weapon(self,option: EnumCrawler) -> WeaponsResponse:
        
        self.__download_url(self.url_base)
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
        
        self.__download_url(self.url_base)
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
        self.__download_url(self.url_base)
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
    
    def get_teams(self) -> TeamsResponse:
        
        url_teams = self.url_base + '/teams'
        
        self.__download_url(url_teams)
        
        self.__get_information_response_html()
        
        teams_div = self.__objectHTML.find_all('div', class_='grid gap-4 lg:grid-cols-2')
        if teams_div.__len__() == 0 :
            return TeamsResponse()
        
        teams_div_list = teams_div[0].find_all('div', class_='card mx-2 md:mx-0')
        if teams_div_list.__len__() == 0:
            return TeamsResponse()
        
        objectResponse = TeamsResponse()
        
        for team in teams_div_list:
            teamResponse = Team()
            teamResponse.bestTeamForCharacter = team.find('h3', ).get_text().split(' ')[-1]
            
            members_div_list = team.find('div', class_='grid grid-cols-4 gap-2')            
    
            for member_div in members_div_list.children:
                
                position = member_div.find('div', class_='md:min-h-auto min-h-10 text-center text-xs lg:text-sm').get_text()
                
                url = url_teams + member_div.find('div', class_='flex justify-center text-center').find('a').get('href').replace('/pt/teams','')
                
                name = member_div.find('div', class_='flex justify-center text-center').find('a').find('span').get_text()
                
                img = member_div.find('div', class_='flex justify-center text-center').find('a').find('div', class_="group relative overflow-hidden rounded-full border-4 border-transparent transition hover:border-vulcan-500").find('img').get('src')

                teamResponse.members.append(MemberTeam(name=name, position=position, url=url, img=img))
            
            objectResponse.data.append(teamResponse)
        
        objectResponse.quantity_teams = objectResponse.data.__len__()
        
        return objectResponse
    
    def __download_url(self, url = None):
        try:
            self.__responseHTML = requests.get(url, timeout=30).text  
        except requests.RequestException as e:
            print(f'Error: {e}')
            raise e

    def __get_information_response_html(self):
        self.__objectHTML = BeautifulSoup(self.__responseHTML, 'html.parser')
    
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
