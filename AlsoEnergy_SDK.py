# -*- coding: utf-8 -*-
"""
Created on Fri Jan 15 07:42:14 2021

@author: JacobJackson
"""
import requests
import pandas as pd

base_url= 'https://api.alsoenergy.com'

def auth(username="jjackson", password="Bunzin4lyfe"):
    
    ##################################################
    '''
    Method used to login and authenticate using the API!
    
    Parameters
    ----------
    username : String
        The username used to login to AlsoEnergy Powertrack. The default is "jjackson".
    password : String
        The username used to login to AlsoEnergy Powertrack. The default is "Bunzin4lyfe".

    Returns
    -------
    api_token : String
        The API token used to authenticate requests made to the AlsoEnergy API

    '''
    ##################################################
    
    auth_url=base_url + '/Auth/token'
    auth_params = {
    "grant_type":"password",
    "username":username,
    "password":password
    }
    response = requests.post(url=auth_url,data=auth_params)
    response.raise_for_status()
    token = response.json()['access_token']
    token_type = response.json()['token_type']
    user_id = response.json()['userId']
    api_token = token_type + ' ' + token
    return api_token
    
def get_weather(api_token, siteId, year, month, day, span='Day'):
    
    ##################################################
    '''
    Method used to get measured weather data for a site! 
    Currently returns POA, GHI, and Temperature data as dataframes.
    The only time granularity available at current time is hourly data.

    Parameters
    ----------
    api_token : String
        The API token used to authenticate requests made to the AlsoEnergy API.
    siteId : Int
        The ID in Powertrack of the site. Can be found in the URL when on Powertrack, also in the site settings.
    year : Int
        Year of the desired data.
    month : Int
        Month of the desired data.
    day : Int
        Day of the desired data.
    span : String, optional
        The length of time for desired data. Options are Day, FiveDay, Week, Month, Year, Lifetime. All must be entered as strings. The default is 'Day'.

    Returns
    -------
    POA : Pandas Dataframe
        Timestamp / POA (W/m2)
    GHI : Pandas Dataframe
        Timestamp / GHI (W/m2)
    TEMP : Pandas Dataframe
        Timestamp / Temperature (W/m2)

    '''
    ##################################################
    
    start_time_string = f'{year}-{month}-{day}T00:00:00'
    params = {
        'chartId':[21,19],
        'startTime':start_time_string,
        'span':span,
        'siteId':siteId,
        'binSize':'Bin1Hour',
    }
    
    header = {
    'Authorization':api_token
    }
    
    weather_dict = {}
    
    for chart in params['chartId']:
        chartIdStr = str(chart)
        url = f'https://api.alsoenergy.com/Charts/{chartIdStr}/Data'
        response = requests.get(url,headers=header,params=params)
        data = response.json()
        if chart == 21:
            for irradience_data in data['data']:
                timestamps = []
                irradience = []
                dataframe_name = irradience_data['title'] + '_dataframe'
                for item in irradience_data['points']:
                    timestamps.append(item['x'])
                    irradience.append(item['y'])
                weather_dict[irradience_data['title']] = irradience
        else:
            amb_temp = []
            timestamps = []
            for item in data['data'][0]['points']:
                amb_temp.append(item['y'])
                timestamps.append(item['x'])
            weather_dict[data['data'][0]['title']] = amb_temp
        weather_dict['timestamps'] = timestamps
            
    #print(weather_dict)
            
    POA = pd.DataFrame(list(zip(weather_dict['timestamps'], weather_dict['Weather Station (Standard)'])), columns =['Timestamp', 'POA (W/m2)'])
    GHI = pd.DataFrame(list(zip(weather_dict['timestamps'], weather_dict['Weather Station (GHI w/ Mod Temp) (GHI)'])), columns =['Timestamp', 'GHI (W/m2)'])
    TEMP = pd.DataFrame(list(zip(weather_dict['timestamps'], weather_dict['Weather Station (Standard) - Ambient Temperature'])), columns =['Timestamp', 'Temperature (F)'])
    
    return POA, GHI, TEMP
    






