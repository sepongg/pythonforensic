#gps 추출
#파이썬 포렌식



import os
import _modEXIF
import _csvHandler
import _commnadParser
from classLogging import _ForensicLog
import pfGoogle
#타임스탬프 카메라 제조사 및 모델에 대해서 반환 EXIFDATA에 오프셋 함

TS = 0
MAKE = 1
MODEL = 2

#명령줄 인수를 처리함
userArgs = _commnadParser.parseCommandLine()

#로그 객체를 만듬
logPath = userArgs.logPath+"ForeniscLog.txt"
oLog = _ForensicLog(logPath)

oLog.writeLog("INFO","Scan Started")

cvsPath = userArgs.csvPath+"imageResults.csv"
oCSV = _csvHandler._CVSWriter(cvsPath)

#탐색하기 위한 디렉토리를 정의함
scanDir = userArgs.scanPath
try:
    picts = os.listdir(scanDir)
except:
    oLog.writeLog("ERROR", "Invalid Directory"+scanDir)
    exit(0)

print
"Program Start"
print

#CDH
#맵핑 만듬

mymap = pfGoogle.maps(33.7167,78.8833,3)

for aFile in picts:
    targetFile = scanDir+aFile
    if os.path.isfile(targetFile):

        gpsDictionary, EXIFList = _modEXIF.ExtractGPSDictionary
        (targetFile)

        if (gpsDictionary != None):

            #변환된 도로 gpsDictiroy에서 위도 경도 값을 구함
            #반환 값은 사전 키/값 쌍이다

            dCoor = _modEXIF.ExtractLatLon(gpsDictionary)
            if dCoor:
                lat = dCoor.get("Lat")
                latRef = dCoor.get("latRef")
                lon = dCoor.get("Lon")
                lonRef = dCoor.get("LonRef")

                if (lat and lon and latRef and lonRef):
                    print
                    str(lat)+','+str(lon)

                    #CDH를 지도 위에 표시
                    mymap.addpointwithTile(lat,lon,"#0000FF",aFile)


                    #출력 파일에 한행을 기록함
                    oCSV.writerCSVRow(targetFile,EXIFList[TS], EXIFList[MAKE], EXIFList[MODEL],latRef,lat,lonRef,lon)
                    oLog.writeLog("INFO", "GPS Data Calculated for:"+ targetFile)
                else:
                    oLog.writeLog("WARING","No GPS EXIF Data for"+ targetFile)
            else:
                oLog.writeLog("WARING", "Improper GPS Data for "+ targetFile)
        else:
             oLog.writeLog("WARING","No GPS EXIF Data for"+ targetFile)
    else:
        oLog.writeLog("WARING", targetFile + "not a valid file")

print
"Program End"

#구글맵에 파일생성해서 담기

mymap.draw('./pfmap.html')


del oLog
del oCSV
