from src.braille import number, mark, hangul, english

#   점자의 번호:
#   (1) (4)
#   (2) (5)
#   (3) (6)

#   점자 유니코드는 U+2800 부터 시작한다.
#   점자 코드는 기계적으로 계산이 가능하게 배치되어있다.
#   점자 번호를 역순으로 나열해서 2진수로 계산하면 해당 점자 코드가 나온다.
#
#    예) ⠓ (1-2-5)일 경우, 점자 유무로 표기하면 "1 1 0 0 1 0 0 0"가 되고, 이를 역순 이진법으로 취하면 "00010011(19, 0x13)"이 된다.
#   그러므로 0x2800 + 0x13 = 0x2813, 즉 U+2813이 해당 점자의 유니코드가 된다.
from src.braille.english import isSpace, isEnglish
from src.braille.mark import isMark
from src.utils.checkText import getChar

Tag = "translate.py"

def data_to_braille(data: str):
    """
    데이터를 점자문자로 변환하는 함수
        :param data: 변환할 데이터 문자열(ex: "011010")
        :return: 변환된 점자문자(ex: "⠖")
    """
    braille = chr(0x2800 + int(data[::-1], 2))
    return braille

def braille_to_data(braille: str):
    """
    점자문자를 데이터로 변환하는 함수
        :param braille: 변환할 점자문자(ex: "⠖")
        :return: 변환된 데이터 문자열(ex: "011010")
    """
    index = bin((int(hex(ord(braille)), 16) - 0x2800))  # 해당 점자를 16진수로 변환하여 index값을 2진수로 추출
    return index[2:].zfill(6)[::-1] # 2진수 문자열을 8자리 0으로 채우고 역순을 취하여 반환


def translate(text: str):
    """
    주어진 문자열을 점자로 번역하는 함수
    :param text: 번역할 문자열(한글, 영어, 특수문자, 숫자)
    :return: 번역된 점자 문자열
    """

    # 문자열에서 약어를 적용
    text = hangul.HangleApplyAbbreviationWords(text)

    # 글자로 분리
    separated_text = list(text)
    # print(f"{Tag}: separated_text - {separated_text}")

    # 번역된 문자 저장될 리스트 (얕은 복사)
    translated_text = separated_text[:]

    eng_idx_start = None
    eng_idx_end = None

    # 약자를 반영하여 한글자씩 번역
    for i in range(len(separated_text)):
        # 한글자 씩 번역
        if hangul.isHangul(separated_text[i]):  # 한글 번역
            translated_text[i] = hangul.HangleToBraille(separated_text[i], i, text)
        elif number.isNumber(separated_text[i]):    # 숫자 번역
            translated_text[i] = number.NumberToBraille(separated_text[i], i, text)
        elif mark.isMark(separated_text[i]):    # 특수 문자 번역
            if(eng_idx_start is not None and eng_idx_end is not None and english.isEnglish(separated_text[i])):
                translated_text[i] = english.EnglishToBraille(separated_text[i], i, eng_idx_start, eng_idx_end, text)
            else:
                translated_text[i] = mark.MarkToBraille(separated_text[i], i, text)
        elif english.isEnglish(separated_text[i]):  # 영어 번역
            # 영어 문장의 범위 구하기
            # eng_idx_start = i, eng_idx_end = 영어 문장의 끝 인덱스
            if(eng_idx_start is None and eng_idx_end is None):
                print("영어 범위 계산")
                eng_idx_end = i+1
                next = getChar(text, eng_idx_end)
                while(isEnglish(next) or isSpace(next) or (isMark(next) and next != '.')):
                    eng_idx_end += 1
                    next = getChar(text, eng_idx_end)
                while(not ((isEnglish(next) and next not in  ')]}>〉')) or (isMark(next) and next not in  ')]}>〉')):
                    eng_idx_end -= 1
                    next = getChar(text, eng_idx_end)
                eng_idx_start = i

                print(text[eng_idx_start:eng_idx_end+1])
            translated_text[i] = english.EnglishToBraille(separated_text[i], i, eng_idx_start, eng_idx_end, text)
            
            # 해당 범위의 점역이 완료 되면 None 상태로 번경
            if(i == eng_idx_end):
                eng_idx_start = None
                eng_idx_end = None
                print("영어 범위 계산 초기화")

    return "".join(translated_text)

test = "that"
answer = "⠴⠹⠁⠞⠲"

print(translate(test))
print(answer)