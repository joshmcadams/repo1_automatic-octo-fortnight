import requests
from datetime import date
import json

class Zoom(object):
    """LifeRing Zoom support."""

    # https://marketplace.zoom.us/docs/api-reference/zoom-api/methods/#operation/dashboardMeetings
    MEETING_API_URL = 'https://api.zoom.us/v2/metrics/meetings'

    def __init__(self, token: str):
        self._token = token

    def _headers(self):
        return {
            'Authorization': f'Bearer {self._token}',
            'Content-Type': 'application/json',
        }

    def get_meetings(self, day: date):
        meetings = []
        query_params = {
            'type': 'past',
            'page_size': '5',
            'from': day.isoformat(),
            'to': day.isoformat(),
            'next_page_token': ''
        }
        
        while True:
            query_params_str = '&'.join([f'{k}={v}' for k, v in query_params.items()])
            meetings_request_url = f'{Zoom.MEETING_API_URL}?{query_params_str}'
            page = requests.get(meetings_request_url, headers=self._headers())

            if (page.status_code != 200):
                raise Exception(page.content)
            
            response = json.loads(page.content.decode('utf-8'))

            for meeting in response['meetings']:
                meetings.append(Meeting(meeting))

            query_params['next_page_token'] = response['next_page_token']
            
            if not query_params['next_page_token']:
                return meetings

        # print(len(meetings))
        # print(page.status_code)
        # print(page.content)
        # meetings = page.content.decode('utf-8')
        # print(meetings)
        # meetings = json.loads(meetings)
        # print(meetings)
        # print(meetings['from'])
        # print(meetings['to'])
        # print(meetings['page_count'])
        # print(meetings['page_size'])
        # print(meetings['total_records'])
        # print(meetings['next_page_token'])
        # print(len(meetings['meetings']))
        # print(type(meetings['meetings'][0]))
        # print(meetings['meetings'][0])

class Meeting(object):

    def __init__(self, meeting_data: dict):
        self._data = meeting_data

    def __str__(self):
        return self._data