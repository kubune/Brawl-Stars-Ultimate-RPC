import discordrpc
import json
from threading import Thread
import os
import time
from src.const import *
from src.presets.presets import Activities

class Rpc():
    def __init__(self, ActivityType: str, ClientId: int):
        self.ActivityType = ActivityType
        self.ClientId = ClientId
        self.rpc = discordrpc.RPC(app_id=self.ClientId)
        Thread(target=self.start).start()

    def start(self):
        while True:
            if os.path.exists('data.json'):
                with open('data.json', 'r') as Data:
                    DATA = json.load(Data)
                self.SetUp(DATA)
            else:
                continue
            time.sleep(0.5)
            
    def SetUp(self, DATA: dict):
        if os.path.exists(f'src/presets/{self.ActivityType}.py'):
            RPC_Data: dict = Activities[self.ActivityType]().activity(DATA)
            self.rpc.set_activity(**RPC_Data)
        elif self.ActivityType == 'default':
            self.DefaultType(DATA)
        else:
            self.DefaultType(DATA)    
            
    def DefaultType(self, DATA: dict):
        self.rpc.set_activity(
                details = f'{DATA['name']} ({DATA['tag']})',
                state = f'Trophies: {DATA['stats']['currentTrophies']:,}/{DATA['stats']['highestTrophies']:,}🏆, 3v3 Victories: {DATA['stats']['3v3']:,}, Solo: {DATA['stats']['solo']:,}',
                large_image='https://i.scdn.co/image/ab6761610000e5ebf7b952107c126c561c52171e',
            )
        