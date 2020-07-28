#pesearch실재 수행 하는곳
#DisplayMessage()/parseCommandLine()
#ValidateFileRead()/ValidateWrite()
#Matrix(class)

import argparse
import os
import logging
import sys

log = logging.getLogger('main._psearch')

#상수
MIN_WORD = 5 #단어 바이트 크기의 최소값
MAX_WORD = 15 #단어바이트크기의 최대값
MAX_PHRASE = 80
PREDECESSOR_SIZE = 80 #일치하는 항목 발견 이전에 인쇄하기 위한값
WINDOW_SIZE = 240 #일치를 발견했을때, 덤프하기위한 전체 값

SPACE = '   '

#이름: parseCommandLine 함수
#설명: 명령줄 인수를 유효성검사 및 처리/파이썬 표준 라이브러리 argparse사용
#입력: 없음
#행위: 명령줄을 처리할 수 있는 표준 라이브러리 argparse사용

def parseCommandLine():

    parser = argparse.ArgumentParser('python Search')

    parser.add_argument('-v','--verbose', help="enables priting of additional program messages", action='stroe_true')
    parser.add_argument('-k','--keyWords', type=ValidateFileRead, required=True,help="specify the file containg search wrods")
    parser.add_argument('-t','--srchTarget',type=ValidateFileRead, required=True,help="specify the target file to search")
    parser.add_argument('-m','--theMatrix', type=ValidateFileRead, required=True, help="specify the weighed matrix file")
    parser.add_argument('-p','--keyPhrases', type=ValidateFileRead, required=True, help="specify the file containing search phrases")
    global gl_args

    gl_args = parser.parse_args()

    DisplayMessgage("Command line processed: Sucessfully")

    return


#parseCommandLine 함수의 끝
#
#이름: ValidateFileRead 함수
#설명: 파일이 존재하고 읽을수 있는지 검증하는 기능
#입력: 전체경로와함께 파일이름
#행위: 유효한 경로를 반환하는 경우/유효하지 않은 경우 argparse의 ArgumentTypeError를 호출
#      argparse에의하여 사용자에게 차례대로 보고 될것임



def ValidateFileRead(theFile):

    #경로가 유효한지 검사
    if not os.path.exists(theFile):
        raise argparse.ArgumentTypeError('File dose not exist')

    #경로가 읽기 가능한지 검사
    if os.access(theFile, os.R_OK):
        return theFile
    else:
        raise argparse.ArgumentTypeError('File is not readable')




#ValidateFileRead 함수의끝===================================================
#
#이름: DisplayMessage 함수
#설명: 명령줄 옵션이 -v 또는 verbose인경우 메시지를 표시
#입력: 메시지타입문자열
#행위: 메시지를 표시하기위해서 표준라이브러리 print기능을 사용
#


def DisplayMessage(msg):

    if gl_arg.verbose:
        print(msg)
    return

#Displaymessage 함수의 끝=============================
#
#이름: searchWord 함수
#명령줄인수 사용
#키워드에 대해 대상파일을 검색

def SearchWrods():

    #검색단어의 빈 집합을 만든다
    searchWords = set()

    searchPhrases = set()

    #열기를 시도하고 검색 단어 읽기를 시도
    try:
        fileWords = open(gl_args.keyWords)
        for line in fileWords:
            searchWords.add(line.strip())
    except:
        log.error('Keyowrd File Failure:'+gl_args.keyWords)
        sys.exit()
    finally:
        fileWords.close()
    try:
        filePhrase = open(gl_args.keyPhrases)
        for line in filePhrase:
            searchPhrases.add(line.strip())
    except:
        log.error('Phrase File Failure:' + gl_args.keyPhrases)
        sys.exit()
    finally:
        filePhrase.close()

    #검색하기위한 단어 항목 로그를 생성
    log.info('search words')
    log.info('input File:'+gl_args.keyWords)
    log.info(searchWords)

    log.info('search phrases')
    log.info('input File :'+gl_args.keyPhrases)
    log.info(searchPhrases)

    #대상파일을 열기 및 읽기를 시도하고 bytearray에 즉시 넣음

    try:
        targetFile = open(gl_args.srchTarget, 'rb')
        baTarget = bytearray(targetFile.read())
    except:
        log.error('Target File Failure:'+gl_args.srchTarget)
        sys.exit()
    finally:
        targetFile.close()

    sizeOfTarget = len(baTarget)

    #로그에 계시

    log.info('Target of Search:'+gl_args.srchTarget)
    log.info('file size:'+str(sizeOfTarget))

    baTargetCopy = baTarget

    wordCheck = class_Matrix()

    #검색반복문
    #1단계 모든 문자가 아닌 것들을 '0'으로 대체함

    for i in range(0, sizeOfTarget):
        character = chr(baTarget[i])
        if not character.isalpha() and character != SPACE:
            baTarget[i] = 0

    #2단계 bytearray로부터 가능한 단어를 추출 하고 검색단어 목록을 조사함
    #가능성 있는 발견되지 않은 항목의 빈목록을 생성

    indexOfWords = []

    cnt = 0
    for i in range(0, sizeOfTarget):
        character = chr(baTarget[i])
        #CDH 1-25-2015/알파와 공간들을 수집
        if character.isalpha() or character == SPACE:
            cnt += 1
        else:
            #최대치 파스 를 위해 수정 체크
            if (cnt >= MIN_WORD and cnt <= MAX_PHRASE):
                newPhrase = ""
                for z in range(i-cnt, i):
                    newPhrase = newPhrase + chr(baTarget[z])
                newPhrase = newPhrase.lower()

                for eachPhrase in searchPhrases:
                    # Determine if newPhrase is contained in eachPhrase
                    # if newPhrase.count(eachPhrase) > 0:
                    if eachPhrase in newPhrase:
                        # If the phrase matches one of the phrases
                        # then Print the Buffer
                        PrintBuffer(newPhrase, i - cnt, baTargetCopy, i - PREDECESSOR_SIZE, WINDOW_SIZE)
                        cnt = 0
                        print

                # CDH 1-25-2015 End Collect Possible Phrases Section
                # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

                # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++
                # CDH 1-25-2015 Now that we have a phrase
                #               we can split the phrase into possible words
                #               new section starts here
                # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++

                # Create a list of words found in the phrase
                # Using the the .split() method of the data type strings

                splitWordList = newPhrase.split()

                # Loop through the possible words in the splitWordList

                for eachWord in splitWordList:

                    # Check the word against the word list
                    # CDH 1-25-2015 This section did not change from orginal
                    #               Except that it is inside the for loop
                    #               in order to process each word in the
                    #               splitWordList

                    if (eachWord in searchWords):
                        PrintBuffer(eachWord, i - cnt, baTargetCopy, i - PREDECESSOR_SIZE, WINDOW_SIZE)
                        indexOfWords.append([eachWord, i - cnt])
                        cnt = 0
                        print
                    else:
                        if wordCheck.isWordProbable(eachWord):
                            indexOfWords.append([eachWord, i - cnt])
                        cnt = 0
            else:
                cnt = 0

    PrintAllWordsFound(indexOfWords)

    return

#searchWrods 함수의 끝
#
#16진수 아스키 페이지 제목을 인쇄
#

def PrintHeading():

    print("offset 00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F     ASCII")
    print("----------------------------------------------------------------")

    return
#Printheading의끝

#버퍼인쇄 하기
#
#검색되는 단어에 대한 버퍼 내용을 인쇄
#매개변수
# 1) 찾은단어
# 2) 단어가 시작하는 부분에 대한 오프셋
# 3) 대상을보유하고 있는 bytearray
# 4) 인쇄하기 위해서 버퍼에 시작 위치 오프셋
# 5) hexSize,윈도우 화면에 출력하기 위한 핵사 크기
#

def PrintBuffer(word, directOffset, buff, offset, hexSize):
    print
    "Found: " + word + " At Address: ",
    print
    "%08x     " % (directOffset)

    PrintHeading()

    for i in range(offset, offset + hexSize, 16):
        for j in range(0, 17):
            if (j == 0):
                print
                "%08x     " % i,
            else:
                byteValue = buff[i + j]
                print
                "%02x " % byteValue,
        print
        "      ",

        # CDH 1-25-2015 Fixed Small Bug in Print Buffer
        # Changed 2nd value in range parameter to 16 vs 17

        for j in range(0, 16):
            byteValue = buff[i + j]
            if (byteValue >= 0x20 and byteValue <= 0x7f):
                print
                "%c" % byteValue,
            else:
                print
                '.',
        print

    return


#printBuffer의끝
#
#printAllWordsFound
#

def PrintAllWordsFound(wordList):
    print
    "Index of All Words"
    print
    "---------------------"

    wordList.sort()

    for entry in wordList:
        print
        entry

    print
    "---------------------"
    print

    return

#printAllwordFound의 끝 ============

#
#클래스 Matrix
#초기화 방법,weightedMatrix 설정으로 매트릭스 적재
#
#isWordProbable방법
#1) 제공된 단어의 가중치를계산
#2) 최소길이를 확인
#3) 단어에 대한 가중치를 계산
#4) 행렬안에 존재에 관한 단어를 시험
#5) true 또는 false 반환



class class_Matrix:

    weightedMatrix = set()

    def __init__(self):
        try:
                fileTheMatrix = open(gl_args.theMatrix,'rb')
                for line in fileTheMatrix:
                    value = line.strip()
                    self.weightedMatrix.add(int(value,16))
        except:
            log.error('Matrix File Error:'+gl_args.theMatrix)
            sys.exit()
        finally:
            fileTheMatrix.close()
        return

    def isWordProbable(self,theWord):

        if (len(theWord) < MIN_WORD):
            return False
        else:
            BASE = 96
            wordWeight = 0

            for i in  range(4,0,-1):
                charValue = (ord(theWord[i])-BASE)
                shiftValue = (i-1)*8
                charWedight = charValue << shiftValue
                wordWeight = (wordWeight | charWedight)

            if (wordWeight in self.weightedMatrix):
                    return True
            else:
                    return False

## Class Matrix 의 끝


