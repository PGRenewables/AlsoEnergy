# -*- coding: utf-8 -*-
"""
Created on Tue Jan  5 18:02:32 2021

@author: JacobJackson
"""

import requests
base_url= 'https://api.alsoenergy.com'


auth_ext = '/Auth/token'
auth_url=base_url+auth_ext
auth_params = {
    "grant_type":"password",
    "username":"jjackson",
    "password":"Bunzin4lyfe"
    }
response = requests.post(url=auth_url,data=auth_params)
response.raise_for_status()
token = response.json()['access_token']
token_type = response.json()['token_type']
user_id = response.json()['userId']
print('Authentication credentials are -', token, token_type, user_id)
api_token = token_type + ' ' + token
print(api_token)


custom_header = {
    'Authorization':api_token
    }
#bonfish ID - 51252
siteId = 51252
bone_ext = f'/Sites/{siteId}/Charts'
bone_url = base_url + bone_ext
#bonefish_response = 
bone_response = requests.get(bone_url,headers=custom_header)
print(bone_response)
data = bone_response.json()['items']

'''
This response is formated:
    {items:[list of dictionaries
            {'chartId': {id},
             'chartName':name,
             'chartSpans': ['day', 'week', 'month', 'year', 'lifetime', 'custom', 'customtime']
             'supportedHardware':xyz
                },
            {
                },
            {
                },
            {
                },
            ......
            ]
    }
'''
total = 0
for chart in data:
    print(chart['chartId'], chart['chartName'])

'''
#chart_params = {
#    'chartId':176,
#    'startTime':,
#    'span':'Day',
#    'siteId':51252,
#    }

chart_ext = '/Charts/176/Data'
chart_url = base_url + chart_ext
bone_response_chart = requests.get(chart_url,headers=custom_header,params=)
data_two = bone_response_chart.json()
print(data_two)
'''