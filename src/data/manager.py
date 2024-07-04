import aiohttp

from src.errors import *


URL_HPDEVFOX = 'https://api.hpdevfox.ru/profile/'
URL_OFFICIAL = 'https://api.brawlstars.com/v1/players/%23'

class Fetcher():
    def __init__(self, PlayerTag: str):
        self.PlayerTag = PlayerTag
        self.session = aiohttp.ClientSession()
        
        
    async def check_profile(self):
        async with self.session as session:
            async with session.get(URL_HPDEVFOX+self.PlayerTag) as resp:
                if resp.status != 200:
                    APIError('Response wasn\'t ok')
                    return
                else:
                    return await resp.json()
                
    async def check_battlelog(self, Token: str):
        async with self.session as session:
            async with session.get(URL_OFFICIAL+self.PlayerTag+"/battlelog", headers={"Authorization": f"Bearer {Token}"}) as resp:
                if resp.status != 200:
                    APIError('Response wasn\'t ok')
                    return
                else:
                    return await resp.json()   
                         
class Formatter():
    def __init__(self):
        self.FormattedData = {}
        
    async def format_data(self, profile: dict, battlelog: dict):
        self.Profile = profile
        self.Battle = battlelog['items']
        ResponseData: dict = self.Profile['response']
        StatsData: dict = ResponseData['Stats']
        self.FormattedData['state'] = self.Profile['state']
        self.FormattedData['tag'] = self.Profile['tag']
        self.FormattedData['name'] = ResponseData['Name']
        self.FormattedData['icon'] = ResponseData['ProfileIcon']
        self.FormattedData['stats'] = {
            "3v3": StatsData['1'],
            "currentTrophies": StatsData['3'],
            "highestTrophies": StatsData['4'],
            "solo": StatsData['8'],
            "duo": StatsData['11'],
        }
        self.FormattedData['brawlers'] = [
            {'id': hero['Character'], 'trophies': hero['Trophies'], 'highestTrophies': hero['HighestTrophies'], 'mastery': hero['Mastery']}
            for hero in ResponseData['Heroes']
        ]
        Battles: list = []
        for battle in self.Battle:
            json_data = {
                'mode': battle['battle']['mode'],
                'timestamp': battle['battleTime'],
                'result': battle['battle']['result'],
                'type': battle['battle']['type']
            }
            for team in battle['battle']['teams']:
                for player in team:
                    if player['tag'] == self.Profile['tag']:
                        json_data['brawler'] = player['brawler']
            Battles.append(json_data)
                        
        self.FormattedData['battles'] = Battles
        
        return self.FormattedData