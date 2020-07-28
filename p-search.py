#간단한 단어의 목록읽기
#bytearray안에 바이너리 파일 읽기
#일치하는 단어를 헥사/아스키 표시로 인쇄
#일치하지 않는 것으로 식별 가능한 단어의 목록을 인쇄
#단어의 정의 예를 들어 단어는 4~12개의 알파벡 문자가 연결 되어있는 것



import logging
import  time
import _psearch

if __name__=='__main__':
    PESEARCH_VERSION='1.0'

    #로깅을 설정함
logging.basicConfig(filename='pSearchLog.log',level=logging.DEBUG,format='%(asctime's %(messase)s'')

    #명령줄인수를 처리
    _psearch.parseCommandLine()
    log = logging.getLogger('main._pesearch')
    log.info("p-search started")

    #시작시간을 기록
    startTime = time.time()

    #키워드 검색수행
    _psearch.searchWords()
    
    #종료하는 시간을 기록
    endTime = time.time()
    duration = endTime - startTime

    logging.info('Elapsed Time:'+str(duration)+'second')
    logging.info('')

    logging.info('Program Terminated Normarlly')


