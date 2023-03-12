from sltcli.omni import getAccessToken, getUsageSummaryJson
from jsonpath_ng import parse


def main():
    print("Fetching your Data...")
    authToken = getAccessToken()
    printUsageSummary(getUsageSummaryJson(authToken))


def printUsageSummary(json_data):
    """Uses the Usage JSON to parse and Print Out Cohesive Output"""

    time = parse("$.dataBundle.my_package_info.reported_time").find(json_data)[0].value

    # Daytime Usage
    dayTimeRemaining = (
        parse("$.dataBundle.my_package_info.usageDetails[0].remaining")
        .find(json_data)[0]
        .value
    )
    dayTimeUsed = (
        parse("$.dataBundle.my_package_info.usageDetails[0].used")
        .find(json_data)[0]
        .value
    )
    dayTimeLimit = (
        parse("$.dataBundle.my_package_info.usageDetails[0].limit")
        .find(json_data)[0]
        .value
    )
    dayTimePercentageRemaining = (
        parse("$.dataBundle.my_package_info.usageDetails[0].percentage")
        .find(json_data)[0]
        .value
    )

    # Total Usage
    totalUsageRemaining = (
        parse("$.dataBundle.my_package_info.usageDetails[1].remaining")
        .find(json_data)[0]
        .value
    )
    totalUsageUsed = (
        parse("$.dataBundle.my_package_info.usageDetails[1].used")
        .find(json_data)[0]
        .value
    )
    totalUsageLimit = (
        parse("$.dataBundle.my_package_info.usageDetails[1].limit")
        .find(json_data)[0]
        .value
    )
    totalUsagePercentageRemaining = (
        parse("$.dataBundle.my_package_info.usageDetails[1].percentage")
        .find(json_data)[0]
        .value
    )

    # Nighttime
    nightTimeUsed = int(float(totalUsageUsed)) - int(float(dayTimeUsed))
    nightTimeLimit = int(float(totalUsageLimit)) - int(float(dayTimeLimit))
    nightTimeRemaining = int(float(nightTimeLimit)) - int(float(nightTimeUsed))
    nightTimePercentageRemaining = round((nightTimeRemaining / nightTimeLimit) * 100)

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
