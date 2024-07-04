from src.activity import Activity
import requests

class Pushing(Activity):
    def __init__(self):
        pass
        
    def activity(self, DATA: dict):
        for index, battle in enumerate(DATA['battles'],start=0):
            if battle['type'] == 'ranked':
                break
        for i, brawler in enumerate(DATA['brawlers'], start=0):
            if brawler["id"] == DATA['battles'][index]['brawler']['id']:
                break 
            
        BrawlerImage = requests.get(url=f'https://api.brawlify.com/v1/brawlers/{DATA['brawlers'][i]['id']}').json()['imageUrl2']
        
        exports = {
            'details': f'{DATA['name']} ({DATA['tag']})',
            'state': f'Pushing {DATA['battles'][index]['brawler']['name'].title()} {DATA['brawlers'][i]['trophies']}/{DATA['brawlers'][i]['highestTrophies']}🏆 Mastery: {DATA['brawlers'][i]['mastery']}',
            'large_image': 'https://i.scdn.co/image/ab6761610000e5ebf7b952107c126c561c52171e',
            'small_image': BrawlerImage,
            'small_text': DATA['battles'][index]['brawler']['name'].title()
        }
        
        return exports
        