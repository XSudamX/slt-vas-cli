def main():
    print("Starting your Report generation now...")
    TotalUsageReport()


def TotalUsageReport():
    """This container function connects to the Omni API and then displays the total usage data for the current month"""

    keywords = [
        "torrent",
        "youtube",
        "instagram",
        "teams",
        "tiktok",
        "Windows Update",
        "Microsoft",
        "Others",
        "SSL",
        "LinkedIn",
        "OneDrive",
        "RiotGames",
        "Spotify",
        "Google",
    ]  # these are the keywords that will sum up your usage
    timer = 5  # sleep timer in between requests to avoid getting timed out (in seconds)

    numDays, prevMonth, year = previousMonthDays()
    authToken = getAccessToken()
    dataTable = [
        [keyword, 0, 0] for keyword in keywords
    ]  # Create Data Table based on keywords array

    for x in range(1, numDays + 1):
        # 1 send request + return json
        date = str(year) + "-" + str(prevMonth) + "-" + str(x).zfill(2)
        print(
            "■ Fetching data now for the following date: "
            + date
            + "...               ",
            end="\r",
        )
        dailyUsageJson = getDailyUsageSummaryJson(date, authToken)

        # 2 parse json + return reduced usage dict of format = "{'BitTorrent': 40.042297, 'BitTorrent DHT': 20.896557, 'SSL': 13.350414}"
        parsedJson = dailyUsageJson["dataBundle"]["total"]
        dict = {}
        for item in parsedJson:
            dict[item["protocol"]] = item["presentage"]

        # 3 use reduced dict and return consolidated dict containing daily usage per keyword
        dailyConsolidateDict = dailyConsolidate(dict, keywords)

        # 4 search match between consolidated dict and data table. if match then 2nd dimension array modify increment and total
        for item in dailyConsolidateDict:
            keyword, integer = item[0], item[1]
            for i in range(len(dataTable)):
                if dataTable[i][0] == keyword:
                    dataTable[i][1] += integer
                    dataTable[i][2] += 1
                    break

        # 5 Sleep Timer
        print(
            "■ Waiting now for "
            + str(timer)
            + " seconds to avoid getting timed out from the API...",
            end="\r",
        )
        time.sleep(timer)

    # With updated data table, Create new dict calculating average for each data item
    resultDict = {}
    totalCaptured = 0.0

    for item in dataTable:
        dataString, total, increment = item[0], item[1], item[2]
        try:
            average = total / increment
        except ZeroDivisionError:
            average = 0
        resultDict[dataString] = average

    for value in resultDict.values():
        totalCaptured += value
    totalCaptured = round(totalCaptured, 1)

    # Output information
    print(
        "Generation Complete! Successfully Captured "
        + str(totalCaptured)
        + "% of your total usage using provided keywords"
    )
    print(
        "============================================================================================"
    )
    print(
        "============================================================================================"
    )
    sorted_data = sorted(resultDict.items(), key=lambda x: x[1], reverse=True)
    max_length = max(len(key) for key in resultDict.keys())
    for key, value in sorted_data:
        bar_length = int(value)
        bar = "■" * bar_length
        key = key.capitalize()
        print(f"{key.ljust(max_length)} | {bar.ljust(20)} {value:.2f}%")
    print(
        "============================================================================================"
    )
