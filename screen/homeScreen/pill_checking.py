from datetime import datetime, timedelta

from PyQt5 import QtCore, QtGui
from screen.homeScreen.line_messaging import sendLateMessage


def checkIsTaken(id, haveToTake):
    if len(haveToTake) == 0: return "no data"
    for item in haveToTake:
        if item["id"] == id and item["isTaken"] == False:
            return "not take"
        elif item["id"] == id and item["isTaken"] == True:
            return "is taken"
    return "no data"

def checkIsSendLateMessage(id, haveToTake):
    if len(haveToTake) == 0: return "no data"
    for item in haveToTake:
        if item["id"] == id and item["isLateMessageSended"] == False:
            return "not send"
        elif item["id"] == id and item["isLateMessageSended"] == True:
            return "already send"
    return "no data"

def checkTakePill(self, n, pill_channel_buttons, pill_channel_datas, haveToTake, config):
    for index in range(8):
        pill_channel_btn = pill_channel_buttons[index]
        pill_channel_data = pill_channel_datas[str(index)]

        # If have data in that slot
        if len(pill_channel_data) != 0:
            for time in pill_channel_data['timeToTake']:
                now = datetime.now()
                if time.split(":")[0] == "00":
                    now += timedelta(days=1)
                nowDate = now.strftime("%Y-%m-%d")
                takePillDateTime = nowDate + " " + time
                timeObject = datetime.strptime(takePillDateTime, '%Y-%m-%d %H:%M')
                stringCompareTime = str(timeObject - now)

                # if time to take is not already past
                if not stringCompareTime.startswith('-1'):
                    willTakeMinute = int(stringCompareTime.split(':')[1])
                    willTakeHour = int(stringCompareTime.split(':')[0])
                    if willTakeMinute <= 10 and willTakeMinute >= 0 and willTakeHour == 0:
                        alreadyTakeFlag = False
                        haveItemFlag = False
                        for item in haveToTake:
                            if item["id"] == index:
                                haveItemFlag = True
                            if item["id"] == index and item["isTaken"]:
                                alreadyTakeFlag = True

                        if not haveItemFlag:
                            takeTimeData = {
                                "id": index,
                                "time": time,
                                "isTaken": False,
                                "isLateMessageSended": False,
                            }
                            haveToTake.append(takeTimeData)

                        if not alreadyTakeFlag:
                            pill_channel_btn.setStyleSheet("background-color : #FBFADD")
                            pill_channel_btn.setText("")
                        else:
                            pill_channel_btn.setStyleSheet("background-color : #F8F37D")
                            pill_channel_btn.setText("")

                else:
                    if checkIsTaken(index, haveToTake) == "not take" and checkIsSendLateMessage(index, haveToTake) == "not send":
                        print("User have not take the pill")
                        sendLateMessage(pill_channel_datas[str(index)], time, config)
                        for no, item in enumerate(haveToTake):
                            if item["id"] == index:
                                haveToTake[no]["isLateMessageSended"] = True

                    flag = 0
                    for item in haveToTake:
                        if item["id"] == index and not item["isTaken"]:
                            flag = 1

                    if flag == 1:
                        for item in haveToTake:
                            if item["id"] == index and not item["isTaken"]:
                                pill_channel_btn.setStyleSheet("background-color : #FBFADD")
                                pill_channel_btn.setText("")
                    else:
                        pill_channel_btn.setStyleSheet("background-color : #97C7F9")
                        pill_channel_btn.setIcon(QtGui.QIcon('../shared/images/plus_icon.png'))
                        pill_channel_btn.setIconSize(QtCore.QSize(60, 60))