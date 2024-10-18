import __main__


def checkIsTaken(channelId, haveToTake):
    if len(haveToTake) == 0: return "no data"
    for item in haveToTake:
        if item["channelId"] == channelId and item["isTaken"] == False:
            return "not take"
        elif item["channelId"] == channelId and item["isTaken"] == True:
            return "is taken"
    return "no data"

def checkIsSendLateMessage(channelId, haveToTake):
    if len(haveToTake) == 0: return "no data"
    for item in haveToTake:
        if item["channelId"] == channelId and item["isLateMessageSended"] == False:
            return "not send"
        elif item["channelId"] == channelId and item["isLateMessageSended"] == True:
            return "already send"
    return "no data"


# def checkTakePill(self, n, pill_channel_buttons, pill_channel_datas, haveToTake, config):
#     for index in range(8):
#         pill_channel_btn = pill_channel_buttons[index]
#         pill_channel_data = pill_channel_datas[str(index)]

#         # ถ้ามีข้อมูลยาในช่อง
#         if len(pill_channel_data) != 0:
#             for time in pill_channel_data['timeToTake']:
#                 now = datetime.now()
                
#                 if time.split(":")[0] == "00":
#                     now += timedelta(days=1)
                    
#                 nowDate = now.strftime("%Y-%m-%d")
#                 takePillDateTime = nowDate + " " + time
#                 timeObject = datetime.strptime(takePillDateTime, '%Y-%m-%d %H:%M')
#                 stringCompareTime = str(timeObject - now)

#                 # ถ้าเวลาใกล้ถึงกำหนด (ภายใน 5 นาที) และยังไม่ทานยา
#                 if not stringCompareTime.startswith('-1'):
#                     willTakeMinute = int(stringCompareTime.split(':')[1])
#                     willTakeHour = int(stringCompareTime.split(':')[0])
                    
#                     if willTakeMinute <= 5 and willTakeMinute >= 0 and willTakeHour == 0:
#                         alreadyTakeFlag = False
#                         haveItemFlag = False
#                         for item in haveToTake:
#                             if item["channelId"] == index:
#                                 haveItemFlag = True
#                             if item["channelId"] == index and item["isTaken"]:
#                                 alreadyTakeFlag = True
                        
#                         # If not have item in haveToTake list
#                         if not haveItemFlag:
#                             takeTimeData = {
#                                 "channelId": index,
#                                 "time": time,
#                                 "isTaken": False,
#                                 "isLateMessageSended": False,
#                             }
#                             haveToTake.append(takeTimeData)
                            
#                         # ถ้ายังไม่ได้หยิบยา
#                         if not alreadyTakeFlag and not alreadyShown[index]:
#                             global isSoundOn
#                             if not isSoundOn :
#                                 playSound()
#                                 sendLineMessage(pill_channel_datas[str(index)], stringCompareTime, self.config)
#                                 isSoundOn = True
                                    
#                             # for button in pill_channel_buttons:
#                             #     button.hide()
                                
#                             detailScreen = showPillDetailsScreen(pill_channel_data)
#                             __main__.widget.addWidget(detailScreen)
#                             __main__.widget.setCurrentIndex(__main__.widget.currentIndex() + 1)
#                             alreadyShown[index] = True
                                
#                         # else :
#                         #         stopSound()
                            
#                     else :
#                         haveItemFlag = False
#                         for item in haveToTake :
#                             if item["channelId"] == index:
#                                 haveItemFlag = True
#                         if not haveItemFlag :
#                             pill_channel_btn.setStyleSheet("background-color : #FBFADD")
#                             pill_channel_btn.setText("")
                            
#                 else :
#                         if checkIsTaken(index, haveToTake) == "not take" and checkIsSendLateMessage(index, haveToTake) == "not send":
#                             print("User have not take the pill")
                        
#                             sendLateMessage(pill_channel_datas[str(index)], time, config)
#                             for no, item in enumerate(haveToTake):
#                                 if item["channelId"] == index :
#                                     haveToTake[no]["isLateMessageSended"] = True
#                             for button in pill_channel_buttons:
#                                 button.show()

#                             home_screen_instance = __main__.HomeScreen(pill_channel_datas, config)  # Create an instance
#                             home_screen_index = __main__.widget.indexOf(home_screen_instance)  # Use the instance
#                             print("home : ",home_screen_index )
#                             __main__.widget.removeWidget(detailScreen)
#                             __main__.widget.setCurrentIndex(home_screen_index)
#                             alreadyShown[index] = False
                            
#                             stopSound()
                            

                                    
#                         # check that it have item in haveToTake pill list that not taken
#                         flag = 0
#                         for item in haveToTake :
#                             if item["channelId"] == index and not item["isTaken"]:
#                                 flag = 1

#                         if flag == 1 :
#                             for item in haveToTake :
#                                 if item["channelId"] == index :
#                                     haveToTake.remove(item)
                                    
#                         #  If time to take is already pass and you already take pill remove that data from haveToTake list
#                         for no, item in enumerate(haveToTake):
#                             if item["channelId"] == index :
#                                 del haveToTake[no]

#                         pill_channel_btn.setStyleSheet("background-color : #FBFADD")
#                         pill_channel_btn.setText("")
                        
#     flag = 0
#     for item in haveToTake :
#         if item["isTaken"] == False:
#             flag = 1
    
#     if len(haveToTake) != 0 and flag == 1 :
#             for index in range(8) :
#                 pill_channel_btn = pill_channel_buttons[index]
#                 pill_channel_data = pill_channel_datas[str(index)]

#                 # If have data in that slot
#                 if len(pill_channel_data) == 0 :
#                     pill_channel_btn.setStyleSheet("background-color : #FBFADD")
#                     pill_channel_btn.setIcon(QtGui.QIcon())
                    
                    
#     else :
#             # Set data to every channel of pill
#             for index in range(8) :
#                 pill_channel_btn = pill_channel_buttons[index]
#                 pill_channel_data = pill_channel_datas[str(index)]

#                 # If have data in that slot
#                 if len(self.pill_channel_datas[str(index)]) != 0 :
#                     font = QtGui.QFont()
#                     font.setPointSize(18)
#                     pill_channel_btn.setFont(font)

#                     channel_text = "ช่องที่ " + str(index + 1) + " \n" + self.pill_channel_datas[str(index)]["name"]
#                     pill_channel_btn.setText(channel_text)
#                     pill_channel_btn.setStyleSheet("background-color : #F8F37D")
#                 else :
#                     # If don't have data in that slot
#                     pill_channel_btn.setStyleSheet("background-color : #97C7F9")
#                     pill_channel_btn.setIcon(QtGui.QIcon('../shared/images/plus_icon.png'))
#                     pill_channel_btn.setIconSize(QtCore.QSize(60, 60))


