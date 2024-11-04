import __main__
import requests


def checkTakePill(channelId):
    url = f"{__main__.config['url']}/user/hardwareGetPillChannels/{__main__.config['userId']}"
    response = requests.get(url)
    if response.status_code == 200:
        json_response = response.json()
        for pill in json_response:
            if int(pill.get('channelIndex', 0)) == channelId:
                return {
                    'id': pill.get('id', ''),
                    'channelId': int(pill.get('channelIndex', 0)),
                    'pillId': pill.get('medicine', {}).get('id', ''),
                    'name': pill.get('medicine', {}).get('name', ''),
                    'medicalname': pill.get('medicine', {}).get('medicalname', ''),
                    'totalPills': pill.get('total', ''),
                    'amountPills': pill.get('amount', ''),
                    'pillsPerTime': pill.get('amountPerTime', ''),
                    'timeToTake': [
        {
            'time': time.get('time', '').replace('.', ':'),
            'isTaken': time.get('isTaken', False)
        } for time in pill.get('times', [])
    ],
                
                }
