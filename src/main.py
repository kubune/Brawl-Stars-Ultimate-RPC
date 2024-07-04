import json
import time

from src.errors import *
from src.data.manager import Fetcher, Formatter
from src.rpc.rpc import Rpc


async def main():
    with open('config.json', 'r') as ConfigFile:
        Configuration: dict = json.load(ConfigFile)
        
    PlayerTag: str = Configuration['tag'].upper().replace("#", "").replace("O", "0")

    for letter in PlayerTag: 
        if letter not in ["0", "2", "8", "9", "P", "Y", "L", "Q", "G", "R", "J", "C", "U", "V"]:
            raise TagError("Wrong Tag")

    Rpc(Configuration['activity'], Configuration['client_id'])
    
    while True:
        PlayerProfile: dict = await Fetcher(PlayerTag).check_profile()
        PlayerBattle: dict = await Fetcher(PlayerTag).check_battlelog(Configuration['token'])
        Data: dict = await Formatter().format_data(PlayerProfile, PlayerBattle)
        with open('data.json', 'w') as json_file:
            json.dump(Data, json_file)
            
        time.sleep(5.0)