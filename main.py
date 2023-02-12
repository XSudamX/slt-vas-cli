import requests
import json
import os
from jsonpath_ng import parse
from dotenv import load_dotenv

load_dotenv()
userName =  os.getenv("USERNAME")
password = os.getenv("PASSWORD")
subscriberId = os.getenv("SUBSCRIBERID")

def main():
    print("===========================================================")
    print("SLT VAS Custom Program")
    authToken = getAccessToken()
    printUsageSummary(getUsageSummaryJson(authToken))



def getAccessToken():
    '''Sends a Post Request to Omni API using Credentials, and captures Access Token'''
    
    headers = {
    'Origin': 'https://myslt.slt.lk',
    'Referer': 'https://myslt.slt.lk/',
    'X-IBM-Client-Id': '41aed706-8fdf-4b1e-883e-91e44d7f379b',
    }

    data = {
    'username': userName,
    'password': password,
    'channelID': 'WEB',
    }

    response = requests.post('https://omniscapp.slt.lk/mobitelint/slt/api/Account/Login', headers=headers, data=data)
    accessCode = response.json()['accessToken']
    return accessCode

def getUsageSummaryJson(token):
    '''Uses the Auth Token to return Usage Summary JSON'''
    
    auth = token

    headers = {
    'Authorization': 'bearer ' + auth,
    'Origin': 'https://myslt.slt.lk',
    'Referer': 'https://myslt.slt.lk/',
    'X-IBM-Client-Id': '41aed706-8fdf-4b1e-883e-91e44d7f379b',
    }

    params = {
    'subscriberID': subscriberId,
    }

    response = requests.get('https://omniscapp.slt.lk/mobitelint/slt/api/BBVAS/UsageSummary', params=params, headers=headers)
    jsonData = json.loads(response.content)
    return jsonData

def printUsageSummary(jsonData):
    '''Uses the Usage JSON to parse and Print Out Cohesive Output'''
    
    time = parse('$.dataBundle.my_package_info.reported_time').find(jsonData)[0].value

    # Daytime Usage
    dayTimeRemaining = parse('$.dataBundle.my_package_info.usageDetails[0].remaining').find(jsonData)[0].value
    dayTimeUsed = parse('$.dataBundle.my_package_info.usageDetails[0].used').find(jsonData)[0].value
    dayTimeLimit = parse('$.dataBundle.my_package_info.usageDetails[0].limit').find(jsonData)[0].value
    dayTimePercentageRemaining = parse('$.dataBundle.my_package_info.usageDetails[0].percentage').find(jsonData)[0].value
    

    # Total Usage
    totalUsageRemaining = parse('$.dataBundle.my_package_info.usageDetails[1].remaining').find(jsonData)[0].value
    totalUsageUsed = parse('$.dataBundle.my_package_info.usageDetails[1].used').find(jsonData)[0].value
    totalUsageLimit = parse('$.dataBundle.my_package_info.usageDetails[1].limit').find(jsonData)[0].value
    totalUsagePercentageRemaining = parse('$.dataBundle.my_package_info.usageDetails[1].percentage').find(jsonData)[0].value

    # Night time
    nightTimeUsed = int(float(totalUsageUsed)) - int(float(dayTimeUsed))
    nightTimeLimit = int(float(totalUsageLimit)) - int(float(dayTimeLimit))
    nightTimeRemaining = int(float(nightTimeLimit)) - int(float(nightTimeUsed))
    nightTimePercentageRemaining = round((nightTimeRemaining/nightTimeLimit)*100)
    
    print("Your usage as of", time)
    print("===========================================================")

    print("Day Time - " + str(dayTimePercentageRemaining) + "% Remaining")
    print(dayTimeUsed + "GB Used out of " + dayTimeLimit + "GB")
    print("Remaining Data: " + dayTimeRemaining + "GB")
    print("===========================================================")
    
    print("Night Time - " + str(nightTimePercentageRemaining) + "% Remaining")
    print(str(nightTimeUsed) + "GB Used out of " + str(nightTimeLimit) + "GB")
    print("Remaining Data: " + str(nightTimeRemaining) + "GB")
    print("===========================================================")
    
    print("Total - " + str(totalUsagePercentageRemaining) + "% Remaining")
    print(totalUsageUsed + "GB Used out of " + totalUsageLimit + "GB")
    print("Remaining Data: " + totalUsageRemaining + "GB")
    print("===========================================================")

def TotalUsageReport():
    '''
    Instagram - "Instagram Video"
    Tiktok - "TikTok"
    Youtube - "YouTube"
    Torrent - "BitTorrent UTP","BitTorrent DHT","BitTorrent","BitTorrent Encrypted"
    '''


main()