from src.braille import brailleDB
from src.braille import hangul


def isNumber(letter):
    """
    입력된 문자 1개가 숫자인지 판별
        :param letter: 문자 1개
        :return: 숫자이면 true, 아니면 false
    """
    return True if (letter in "0123456789") else False

def isSpace(letter):
    """
    입력된 문자가 공백인지 판별
        :param letter: 입력된 문자
        :return: 공백이면 true, 아니면 false
    """
    return True if letter == ' ' else False

def NumberToBraille(letter, prev, next):


    ## 한글자 이상 입력이 들어올 경우
    if len(letter) > 1:
        print("ERR: Syllabification()은 한글자만 입력 받음")
        return ""

    if (not (isNumber(letter) or isSpace(letter))):
        # print(f"ERR: <{letter}>은 한글 문자가 아님")
        # 숫자 문자가 아니면 일단 그대로 반환
        return f"{letter}"

    tran = []  # 번역된 점자가 들어갈 리스트

    # 이전 문자가 숫자가 아니라면 수표 추가
    if(prev is None or not isNumber(prev)):
        tran.append(brailleDB.num_start)

    # 숫자를 점자로 번역
    tran.append(brailleDB.num_dict[letter])

    # 제 38항 예외, 숫자 뒤에 (ㄴㄷㅁㅋㅌㅍㅎ)의 첫 글자, (운)의 약자가 올때는 띄어쓰기 추가
    if(next is not None and hangul.isHangul(next)):
        # 다음 글자가 한글일 경우 음절 분리
        next_cho, next_jung, next_jong = hangul.Syllabification(next)
        if(next_cho in "ㄴㄷㅁㅋㅌㅍㅎ" or next == '운'):
            tran.append(" ")



    return "".join(tran)
