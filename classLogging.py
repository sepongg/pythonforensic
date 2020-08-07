#클랙스 : _ForensicLog
#설명 : 포렌식 로깅 작업을 처리
#메소드 생성자 : 로거를 초기화 함
#   writeLog : 로그에 레코드를 기록함
#   destructor : 정보 메시지를 기록하고 로거를 종료함

import  logging

class _ForensicLog:
    def __init__(self, logName):
        try:
            #로깅을 설정함
            logging.basicConfig(filename=logName,level=logging.DEBUG,format='%(asctime)s %(message)s')
        except:
            print
            "Forensic Log Initalization Failure ...Aborting"
            exit(0)

    def writeLog(self,logType, logMessage):
        if logType == "INFO":
            logging.info(logMessage)
        elif logType == "ERROR":
            logging.error(logMessage)
        elif logType == "WARNING":
            logging.warning(logMessage)
        else:
            logging.error(logMessage)
        return

    def __del__(self):
        logging.info("Logging Shutdown")
        logging.shutdown()

