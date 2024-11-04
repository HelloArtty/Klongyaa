import __main__
import requests


def fetch_pill_channel_data(channelId):
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
                    'totalPills': pill.get('amount', ''),
                    'pillsPerTime': pill.get('amountPerTime', ''),
                    'timeToTake': [time.get('time', '').replace('.', ':') for time in pill.get('times', [])]
                
                }
