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

def isAllUpper(str: str):
    result = True
    for i in str:
        if(i.isupper() or isMark(i)):
            pass
        else:
            result = False
            break
    return result


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

    eng_idx = i - start
    eng_text = text[start:end+1]
    global state
    global end_idx
    state = 'lower'
    end_idx = 0
    one_upper = []
    word_upper = []
    str_upper = []
    end_upper = []
    for ei in range(len(eng_text)):
        if(state == 'lower' and eng_text[ei].isupper()):
            state = 'upper'
            next = getChar(eng_text, ei+1)
            tmp = ei+1
            end_idx = ei
            # 대문자의 범위 탐색
            while(not (next is None or next.islower() or next in "@#^&/")):
                if(next is None):
                    end_idx = tmp - 1
                    break
                else:
                    tmp += 1
                    next = getChar(eng_text, tmp)
                    if(next is None or next.islower() or next in "@#^&/"): end_idx = tmp - 1
            if (ei == end_idx): # 대문자가 범위가 1개일 경우
                print("대문자표 하나")
                if(eng_text[ei] == "Å"):    # 단위표 옹스트롬은 대문자로 인식하지만, 대문자 취급x
                    pass
                else:
                    one_upper.append(ei)
                state = 'lower'
            else:
                tmp_text = eng_text[ei:end_idx+1]
                if(len(tmp_text.split(" ")) >= 3):  # 범위를 스플릿 했을 때 3개 이상 나올 경우 구절
                    print("구절표")
                    str_upper.append(ei)
                else:   # 그렇지 않은 경우 단어표
                    print("단어표")
                    eng_word_list = tmp_text.split(" ")
                    for t in range(len(eng_word_list)):
                        if(t == 0): word_upper.append(ei)
                        else: word_upper.append(ei+len(eng_word_list[t-1])+1)

        elif(state == 'upper' and eng_text[ei].isupper()):
            pass
        elif(state == 'upper' and eng_text[ei].islower()):
            end_upper.append(ei)
            state = 'lower'

    # 대문자 표 작성
    if (eng_idx in one_upper): tran.append(brailleDB.eng_upper)
    elif (eng_idx in word_upper): tran.append(brailleDB.eng_word_upper)
    elif (eng_idx in str_upper): tran.append(brailleDB.eng_str_upper)
    if (eng_idx in end_upper): tran.append(brailleDB.eng_end_upper)
        
    # 영어를 점자로 번역
    tran.append(brailleDB.eng_dict[letter])

    # 영어 끝나면 로마자 종료 표시
    # 영어 다음에 (.)이 나오면 종료 표시 대신 마침표(.)의 점자를 찍음
    if (i == end and getChar(text, end+1) != '.'):
        # 제 31항 단위 부호로 끝날 경우 공백을 추가
        #   °C, °F
        #   %p
        if(letter in "%‰°′″Å"
                or (letter in "CF" and getChar(text, i-1) == "°")
                or (letter in "p" and getChar(text, i-1) == "%")):
            # 이미 공백이면 생략
            if(getChar(text, i+1) == " "):
                pass
            else:
                tran.append(' ')
        elif(getChar(text, i+1) is not None and getChar(text, i+1).isnumeric()):
            print("asdf")
            pass
        else:   # 일반적인 경우 로마자 종료 표시
            tran.append(brailleDB.eng_end)



    return "".join(tran)
