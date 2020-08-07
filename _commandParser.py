import argparse     #파이썬 표준 라이브러리 명령줄옵션,인수엔대한 파서
import os

#이름 : parseCommand 기능
#설명 : 파이썬 표준 라이브러리 모듈 argparse를 사용하여 명령줄 인수를 처리및 유효성 검증
#행위 : 명령줄을 처리하기 위해서 표준 라이브러리 argparse를 사용
#입력 : 없음


def ParseCommandLine():
    parser = argparse.ArgumentParser('python gpsExtractor')

    parser.add_argument('-V','--verbose', help="enable printing of additional program message", action='stroe_true')
    parser.add_argument('-l','-loogPath', type=ValidateDirectory, required=True, help="specify the directory for forensic log output file")
    parser.add_argument('-c','--csvPath', type=ValidateDirecory,required=True, help="specify the out put directory for the csv file")
    parser.add_argument('-d','--scanPath', type=ValidateDirectory, required=True, help="specify the directory to scan")

    theArgs = parser.parse_args()

    return theArgs

#명령줄 파서의 끝 ===================================================================

def ValidateDirectory(theDir):
    #경로가 디렉토리인지 유효성 검증함
    if not os.path.isdir(theDir):
        raise argparse.ArgumentTypeError('Directory dose not exits')

    #경로가 쓰기 가능한지 유효성 검사함
    if os.access(theDir,os.W_OK):
        return theDir
    else:
        raise argparse.ArgumentTypeError('Directory is not writable')

#ValidateDirectory의 끝 =====================


