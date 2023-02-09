from src.braille import brailleDB
from src.braille import hangul
from src.braille.mark import isMark
from src.utils.checkText import getChar
import re


def isEnglish(letter):
    """
    입력된 문자 1개가 영어인지 판별
        :param letter: 문자 1개
        :return: 영어면 true, 아니면 false
    """
    if(letter is None): return False
    # (@#^&)는 한글 점자 규정이 없어 영어 점자 규정을 따라간다. 따라서 영어로 해석되어야 함
    return True if (letter in brailleDB.eng_dict) else False

def isSpace(letter):
    """
    입력된 문자가 공백인지 판별
        :param letter: 입력된 문자
        :return: 공백이면 true, 아니면 false
    """
    return True if letter == ' ' else False

def EnglishToBraille(letter, i, start, end, text):

    ## 한글자 이상 입력이 들어올 경우
    if len(letter) > 1:
        print("ERR: Syllabification()은 한글자만 입력 받음")
        return ""

    if (not (isEnglish(letter) or isSpace(letter))):
        # print(f"ERR: <{letter}>은 한글 문자가 아님")
        # 영어 문자가 아니면 일단 그대로 반환
        return f"{letter}"

    tran = []  # 번역된 점자가 들어갈 리스트

    # 영어 시작 시 로마자 시작 표시
    if (i == start):
        tran.append(brailleDB.eng_start)
        
    # 영어를 점자로 번역
    tran.append(brailleDB.eng_dict[letter])

    # 영어 끝나면 로마자 종료 표시
    # 영어 다음에 (.)이 나오면 종료 표시 대신 마침표(.)의 점자를 찍음
    if (i == end and getChar(text, end+1) != '.'):
        tran.append(brailleDB.eng_end)



    return "".join(tran)
