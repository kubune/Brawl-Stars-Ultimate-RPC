from src.main import main
import asyncio
import os
import json

if not os.path.exists('config.json'):
    with open('config.json', 'w') as file:
        json.dump({"client_id": 1162777598913433650,"tag": "YOUR TAG HERE","activity": "pushing","token": "YOUR TOKEN FROM developer.brawlstars.com HERE"}, file)
    print('Please configure config.json file')
    
asyncio.run(main())