import json
import requests
import os
from dotenv import load_dotenv

load_dotenv()
userName = os.getenv("USERNAME")
password = os.getenv("PASSWORD")
subscriberId = os.getenv("SUBSCRIBER_ID")

headers = {
    "Origin": "https://myslt.slt.lk",
    "Referer": "https://myslt.slt.lk/",
    "X-IBM-Client-Id": "41aed706-8fdf-4b1e-883e-91e44d7f379b",
}


def getAccessToken():
    """Sends a Post Request to Omni API using Credentials, and captures Access Token"""
    data = {
        "username": userName,
        "password": password,
        "channelID": "WEB",
    }

    response = requests.post(
        "https://omniscapp.slt.lk/mobitelint/slt/api/Account/Login",
        headers=headers,
        data=data,
    )
    accessCode = response.json()["accessToken"]
    return accessCode


def getUsageSummaryJson(token):
    """Uses the Auth Token to return Usage Summary JSON"""

    headers["Authorization"] = "bearer " + token

    params = {
        "subscriberID": subscriberId,
    }

    response = requests.get(
        "https://omniscapp.slt.lk/mobitelint/slt/api/BBVAS/UsageSummary",
        params=params,
        headers=headers,
    )
    jsonData = json.loads(response.content)
    return jsonData


def getDailyUsageSummaryJson(date, token):
    """This function accepts a data parameter, and gets the usage json for that particular date"""

    headers["Authorization"] = "bearer " + token

    # construct url from date and subID
    url = (
            "https://omniscapp.slt.lk/mobitelint/slt/api/BBVAS/ProtocolReport?&subscriberID="
            + subscriberId
            + "&date="
            + date
    )

    response = requests.get(url, headers=headers)
    jsonData = json.loads(response.content)
    return jsonData
