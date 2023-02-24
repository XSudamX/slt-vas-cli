import requests
import json
import os
import datetime
import calendar
import time
from jsonpath_ng import parse
from dotenv import load_dotenv


load_dotenv()
userName =  os.getenv("USERNAME")
password = os.getenv("PASSWORD")
subscriberId = os.getenv("SUBSCRIBERID")

def main():
    menu()

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
    
    print("===========================================================")
    print("Here is your usage as of", time)
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

def menu():
    '''Prints out the main menu for the program, and handles user input'''
    bannerText = """
 _______  _    _________                _______  _______        _______  _       _________
(  ____ \( \   \__   __/      |\     /|(  ___  )(  ____ \      (  ____ \( \      \__   __/
| (    \/| (      ) (         | )   ( || (   ) || (    \/      | (    \/| (         ) (   
| (_____ | |      | |         | |   | || (___) || (_____       | |      | |         | |   
(_____  )| |      | |         ( (   ) )|  ___  |(_____  )      | |      | |         | |   
      ) || |      | |          \ \_/ / | (   ) |      ) |      | |      | |         | |   
/\____) || (____/\| |           \   /  | )   ( |/\____) |      | (____/\| (____/\___) (___
\_______)(_______/)_(            \_/   |/     \|\_______)      (_______/(_______/\_______/
    """
    print(bannerText)
    def option_1():
        print("Fetching your Data...")
        authToken = getAccessToken()
        printUsageSummary(getUsageSummaryJson(authToken))

    def option_2():
        print("You selected Option 2")
        TotalUsageReport()

    while True:
        print("1. View current month summary")
        print("2. View consolidated detailed usage")
        choice = input("Enter your choice (1 or 2): ")
        if not choice:
            print("Invalid input. Please enter a value.")
            continue
        try:
            choice = int(choice)
            if choice == 1:
                option_1()
                break
            elif choice == 2:
                option_2()
                break
            else:
                print("Invalid input. Please enter 1 or 2.")
        except ValueError:
            print("Invalid input. Please enter a valid integer.")
        except OverflowError:
            print("Invalid input. The value is too large.")



def previousMonthDays():
    '''This function uses the datetime module to calculate the number of days in the previous month, and also return the prev month and year'''
    today = datetime.datetime.now()
    prevMonth = today.month - 1
    if prevMonth == 0:
        prevMonth = 12
        year = today.year - 1
    else:
        year = today.year
    numDays = calendar.monthrange(year, prevMonth)[1]
    prevMonth = str(prevMonth).zfill(2)
    return numDays,prevMonth,year


def getDailyUsageSummaryJson(date,token):
    '''This function accepts a data parameter, and gets the usage json for that particular date'''

    auth = token

    headers = {
        'Authorization': 'bearer ' + auth,
        'Origin': 'https://myslt.slt.lk',
        'Referer': 'https://myslt.slt.lk/',
        'X-IBM-Client-Id': '41aed706-8fdf-4b1e-883e-91e44d7f379b',
    }
    
    # construct url from date and subID
    url  = "https://omniscapp.slt.lk/mobitelint/slt/api/BBVAS/ProtocolReport?&subscriberID=" + subscriberId + "&date=" + date

    response = requests.get(url, headers=headers)
    jsonData = json.loads(response.content)
    return jsonData

def add_values_by_matching_key(dictionary, match_str):
    total = 0
    match_str = match_str.lower()
    for key, value in dictionary.items():
        if match_str in key.lower():
            total += value
    return total

def dailyConsolidate(dictionary,keywordsArray):
    data = [[keyword,0] for keyword in keywordsArray]
    for dataKey in data:
        dataKey[1] = add_values_by_matching_key(dictionary,dataKey[0])
    return data

def TotalUsageReport():
    '''This container function connects to the Omni API and then displays the total usage data for the current month'''

    keywords = ["torrent","youtube","instagram","teams","tiktok"] # these are the keywords that will sum up your usage
    timer = 5 # sleep timer in between requests to avoid getting timed out (in seconds)

    numDays,prevMonth,year = previousMonthDays()
    authToken = getAccessToken()
    dataTable = [[keyword, 0, 0] for keyword in keywords] # Create Data Table based on keywords array

    for x in range(1,numDays+1):
        
        #1 send request + return json
        date = str(year) + "-" + str(prevMonth) + "-" + str(x).zfill(2)
        print("Getting information for the following date now: " + date)
        dailyUsageJson = getDailyUsageSummaryJson(date,authToken)
        
        #2 parse json + return reduced usage dict of format = "{'BitTorrent': 40.042297, 'BitTorrent DHT': 20.896557, 'SSL': 13.350414}"
        #jsonResponse = json.loads(dailyUsageJson)
        parsedJson = dailyUsageJson["dataBundle"]["total"]
        dict = {}
        for item in parsedJson:
            dict[item["protocol"]] = item["presentage"]
        #print(dict)

        #3 use reduced dict and return consolidated dict containing daily usage per keyword
        dailyConsolidateDict = dailyConsolidate(dict,keywords)

        #4 search match between consolidated dict and data table. if match then 2nd dimension array modify increment and total
        for item in dailyConsolidateDict:
            keyword, integer = item[0], item[1]
            for i in range(len(dataTable)):
                if dataTable[i][0] == keyword:
                    dataTable[i][1] += integer
                    dataTable[i][2] += 1
                    break
        
        #5 Sleep Timer
        print("Sleeping now for " + str(timer) + " Seconds to avoid timeout.....")
        time.sleep(timer)
    

    
    # With updated data table, Create new dict calculating average for each data item
    resultDict = {}
    for item in dataTable:
        dataString,total,increment = item[0],item[1],item[2]
        try:
            average = total / increment
        except ZeroDivisionError:
            average = 0
        resultDict[dataString] = average

    
    # Output information
    print(resultDict)


main()