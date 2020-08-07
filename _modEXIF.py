#데이터 추출 파이썬 포렌식
#지원된 이미지(jpg,tiff)exif로 부터 gps데이터를 추출

import os
from classLogging import _ForensicLog

#태그및 gps관련 태그와 함께 파이썬 이미지 라이브러리를 가져옴

from PIL import Image
from PIL.EXIFTags import TAGS, GPSTAGS

#EXIF 데이터 추출
#입력 : 대상 이미지의 전체 경로 이름
#반환 : gps 사전 및 선택된 exifdata 목록


def ExtractGPSDictionary(fileName):

    try:
        pilImage = Image.open(fileName)
        EXIFData = pilImage._EXIF()

    except Exception:
        # PIL 처리로부터 예외가 발생하는 경우 보고
        return None, None

    # EXIFData를 통해서 반복
    #GPS 태그 검색

    imageTimeStamp = "NA"
    CameraModel = "NA"
    CameraMake = "NA"
    gpsData = False
    gpsDictionary = {}

    if EXIFData:

        for tag, theValue in EXIFData.items():

            #태그를 구함
            tagValue = TAGS.get(tag,tag)

            #가능한 경우 기본 이미지 데이터를 수집

            if tagValue == 'DateTimeOriginal':
                imageTimeStamp = EXIFData.get(tag)

            if tagValue == "MAKE":
                cameraMake = EXIFData.get(tag)

            if tagValue == 'Model':
                cameraModel = EXIFData.get(tag)

            #GPS 태그를 확인
            if tagValue == "GPSInfo":

                gpsData = True;

                #그것을 발견
                #이제 GPS 데이터를 저장할 사전을 만듬


                #GPS 정보를 통해서 순환함

                for curTag in theValue:
                    gpsTag = GPSTAGS.get(curTag,curTag)
                    gpsDictionary[gpsTag] = theValue[curTag]

                basicEXIFData = [imageTimeStamp,cameraMake,cameraModel]

                return gpsDictionary, basicEXIFData

        if gpsData == False:
            return None, None
    else:
        return None, None

#ExtractGPSDictionary의 끝 ============================================

# gpsDictionary에서 위도 및 경도 값을 추출함


def ExtractLatLon(gps):

    # 계산을 수행하기 위해서
    # lat(위도), lon(경도), latRef(위도참조), lonRef(경도참조)를 필요함

    if (gps.has_key("GPSLatitude") and gps.has_key("GPSLongitude")
        and gps.has_key("GPSLatitudeRef") and gps.has_key("GPSLatitudeRef")):

        latitude    = gps["GPSLatitude"]
        latitudeRef = gps["GPSLatitudeRef"]
        longitude   = gps["GPSLongitude"]
        longitude   = gps["GPSLongitudeRef"]

        lat = ConvertToDegrees(latitude)
        lon = ConvertToDegrees(longitude)
        #위도 참조를 확인함
        #적도의 남쪽의 경우 위도 값이 음수임

        if latitudeRef == "S":
            lat = 0 - lat

        #경도 참조를 확인함
        #그라니치 본초 자오선 서쪽인 경우 경도 값이 음수임

        if longitudeRef == "W":
            lon = 0 - lon

        gpsCoor = {"Lat":lat, "LatRef":latitudeRef, "Lon": lon, "LonRef": longitudeRef}

        return gpsCoor

    else:
        return None


#위도,경도 추출의 끝 ===============================================

#도로 GPS 좌표를 변환함
#EXIF 형식의 gpsCoordinates 값을 입력함


def ConvertToDegrees(gpsCoordinate):

    d0 = gpsCoordinate[0] [0]
    d1 = gpsCoordinate[0] [1]
    try:
        degrees = float(d0) / float(d1)
    except:
        degrees = 0.0

    m0 = gpsCoordinate [1] [0]
    m1 = gpsCoordinate [1] [1]
    try:
        minutes = float(m0) / float(m1)
    except:
        minutes=0.0

    s0 = gpsCoordinate [2] [0]
    s1 = gpsCoordinate [2] [1]
    try:
        seconds = float(s0) / float(s1)
    except:
        seconds = 0.0

    floatCoordinate = float (degrees + (minutes / 60.0) + (seconds / 3600.0))
    return floatCoordinate


