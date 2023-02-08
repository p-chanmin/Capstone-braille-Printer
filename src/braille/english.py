from src.braille import brailleDB
from src.braille import hangul
from src.utils.checkText import getChar
import re


def isEnglish(letter):
    """
    입력된 문자 1개가 영어인지 판별
        :param letter: 문자 1개
        :return: 영어면 true, 아니면 false
    """
    reg = re.compile(r'[a-zA-Z]')
    if(letter is None): return False
    # (@#^&)는 한글 점자 규정이 없어 영어 점자 규정을 따라간다. 따라서 영어로 해석되어야 함
    return True if (reg.match(letter) or letter in "@#^&") else False

def isSpace(letter):
    """
    입력된 문자가 공백인지 판별
        :param letter: 입력된 문자
        :return: 공백이면 true, 아니면 false
    """
    return True if letter == ' ' else False

def EnglishToBraille(letter, index, text):

    prev = getChar(text, index - 1)   # 이전 글자 가져오기
    next = getChar(text, index + 1)   # 다음 글자 가져오기

    ## 한글자 이상 입력이 들어올 경우
    if len(letter) > 1:
        print("ERR: Syllabification()은 한글자만 입력 받음")
        return ""

    if (not (isEnglish(letter) or isSpace(letter))):
        # print(f"ERR: <{letter}>은 한글 문자가 아님")
        # 영어 문자가 아니면 일단 그대로 반환
        return f"{letter}"

    tran = []  # 번역된 점자가 들어갈 리스트


    # 영어를 점자로 번역
    tran.append(brailleDB.eng_dict[letter])



    return "".join(tran)
