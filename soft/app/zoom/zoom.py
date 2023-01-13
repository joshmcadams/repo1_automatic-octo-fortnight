import requests
from datetime import date
import json
from urllib.parse import quote

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
            'page_size': '30',
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
                meetings.append(Meeting(self._token, meeting))

            query_params['next_page_token'] = response['next_page_token']
            
            if not query_params['next_page_token']:
                return meetings

class Meeting(object):
    # 'uuid': 'Ojgl6wcGRlWWaEK5TmzUgg=='
    # 'id': 87135907544
    # 'topic': 'Sunday @ 5PM » HWYW : Spanish — Shannon — La vida sobria [¿Cómo fue tu semana?] (7544)'
    # 'host': 'LifeRing Convenor (ch7)'
    # 'email': 'xxxxx@lifering.org'
    # 'user_type': 'Licensed'
    # 'start_time': '2023-01-09T00:53:32Z'
    # 'end_time': '2023-01-09T01:54:37Z'
    # 'duration': '01:01:05'
    # 'participants': 2
    # 'has_pstn': False
    # 'has_archiving': False
    # 'has_voip': True
    # 'has_3rd_party_audio': False
    # 'has_video': True
    # 'has_screen_share': False
    # 'has_recording': False
    # 'has_sip': False
    # 'audio_quality': 'good'
    # 'has_manual_captions': False
    # 'has_automated_captions': False

    def __init__(self, token: str, meeting_data: dict):
        self._token = token
        self._data = meeting_data

    def __str__(self):
        return self._data

    def _headers(self):
        return {
            'Authorization': f'Bearer {self._token}',
            'Content-Type': 'application/json',
        }

    def get_participants(self):
        participants = []
        uuid = quote(self._data.get('uuid'))

        query_params = {
            'type': 'past',
            'page_size': '30',
            'next_page_token': ''
        }

        while True:
            query_params_str = '&'.join([f'{k}={v}' for k, v in query_params.items()])
            meetings_request_url = f'{Zoom.MEETING_API_URL}/{uuid}/participants?{query_params_str}'
            page = requests.get(meetings_request_url, headers=self._headers())

            if (page.status_code != 200):
                raise Exception(page.content)
            
            response = json.loads(page.content.decode('utf-8'))

            for participant in response['participants']:
                participants.append(Participant(self._token, participant))

            query_params['next_page_token'] = response['next_page_token']
            
            if not query_params['next_page_token']:
                return participants


class Participant(object):

    def __init__(self, token: str, participant_data: dict):
        self._token = token
        self._data = participant_data
        if participant_data['user_name'] == 'Lisa Livingstone':
            print(participant_data)

        # 'id': 'apohGG3OSJ2_K-JQ3iwDig'
        # 'user_id': '141234123'
        # 'user_name': 'xxxxx xxx'
        # 'device': 'Unknown'
        # 'ip_address': '174.207.229.75'
        # 'location': 'Toledo (US)'
        # 'network_type': 'Cellular'
        # 'data_center': 'United States'
        # 'full_data_center': 'United States;'
        # 'connection_type': 'UDP'
        # 'join_time': '2023-01-10T00:33:03Z'
        # 'leave_time': '2023-01-10T00:59:53Z'
        # 'share_application': False
        # 'share_desktop': False
        # 'share_whiteboard': False
        # 'recording': False
        # 'pc_name': ''
        # 'domain': ''
        # 'mac_addr': ''
        # 'harddisk_id': ''
        # 'version': ''
        # 'leave_reason': 'XXXXXX left the meeting.<br>Reason: left the meeting.'
        # 'registrant_id': ''
        # 'status': 'in_meeting'
        # 'customer_key': ''
        # 'sip_uri': ''
        # 'from_sip_uri': ''
        # 'role': 'attendee'
        # 'participant_user_id': 'apohGG3OSJ2_K-JQ3iwDig'
        # 'audio_call': []
