from src.braille import brailleDB
from src.braille import hangul
from src.braille.mark import isMark
from src.braille.number import isNumber
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

def UpperDFS(i, d, eng_text, end = False, now_cnt = 1, prev_cnt = 1):
    next = getChar(eng_text, d+1)
    if(next is None):
        return (i, d, False)
    elif(now_cnt >= 1 and eng_text[d].isupper() and next.isupper()): # 대문자 1개인 상태에서 다음 대문자로 넘어갈 경우
        (ti, td, te) = UpperDFS(i, d+1, eng_text, end, now_cnt+1, prev_cnt+1)
        return (i, td, te)
    elif (prev_cnt != 1 and now_cnt == 0 and next.isupper() and getChar(eng_text, d+2) is not None and getChar(eng_text, d+2).isupper()):  # 현재 카운트 0인 상태에서 다음 대문자 단어로 넘어가는 경우
        (ti, td, te) = UpperDFS(i, d + 1, eng_text, end, now_cnt + 1, 1)
        return (i, td, te)
    elif((isSpace(next) or next in ",")):
        (ti, td, te) = UpperDFS(i, d+1, eng_text, end, 0, prev_cnt)
        return (i, td, te)
    else: # 대문자 종료 구문
        if(next.islower() or isNumber(next) or (isMark(next) and next not in ",")):
            return (i, d, True)
        else:
            return (i, d, end)


def findUpper(eng_text):
    max_idx = -1
    one_upper = []
    word_upper = []
    str_upper = []
    end_upper = []


    for i in range(len(eng_text)):
        if(i <= max_idx):
            continue
        if(eng_text[i].isupper()):  # 대문자 범위 탐색
            start_idx, end_idx, end  = UpperDFS(i, i, eng_text)   # 대문자 범위 탐색
            max_idx = end_idx   # 최대 idx 갱신, 범위 안의 문자는 다시 탐색x

            sub_text = re.sub(r"\s+$", "", eng_text[start_idx:end_idx+1])   # 문자열의 마지막 공백을 제거한 대문자 범위 문자열
            print(sub_text, end)

            if(len(sub_text) == 1): # 대문자 1개일 경우, 대문자 기호표
                print("대문자 1개")
                one_upper.append(i)
            else:   # 대문자 1개 이상일 경우
                sub_text_list = sub_text.split(" ") # 공백으로 단어 분리
                if(len(sub_text_list) >= 3):    # 단어가 3개 이상일 경우, 대문자 구절표
                    print("대문자 구절표")
                    str_upper.append(i)
                    if(end):    # 대문자 종료표를 적어야 할 경우
                        end_upper.append(i+len(sub_text))
                else: # 단어가 2개 이하일 경우, 대문자 단어표
                    print("대문자 단어표")
                    for ti in range(len(sub_text_list)):
                        if(ti == 0): word_upper.append(i)
                        else:
                            word_upper.append(i + len(sub_text_list[ti-1]) + 1)
                    if (end):  # 대문자 종료표를 적어야 할 경우
                        end_upper.append(i + len(sub_text))


    return one_upper, word_upper, str_upper, end_upper


def EnglishToBraille(start, end, text):

    tran = []  # 번역된 점자가 들어갈 리스트

    # 영어 시작 시 로마자 시작 표시
    # if (i == start):
    #     tran.append(brailleDB.eng_start)

    # eng_idx = i - start
    eng_text = text[start:end+1]
    print(eng_text)
    one_upper, word_upper, str_upper, end_upper = findUpper(eng_text)

    eng_text = list(text[start:end + 1])
    # 대문자 표 작성
    for i in range(len(eng_text)):
        if (i in one_upper):
            eng_text[i] = brailleDB.eng_upper + eng_text[i]
        elif (i in word_upper):
            eng_text[i] = brailleDB.eng_word_upper + eng_text[i]
        elif (i in str_upper):
            eng_text[i] = brailleDB.eng_str_upper + eng_text[i]
        if (i in end_upper):
            eng_text[i] = brailleDB.eng_end_upper + eng_text[i]

    eng_text = "".join(eng_text)
    # 로마자 시작 표시 추가
    eng_text = brailleDB.eng_start + eng_text

    # 영어 끝나면 로마자 종료 표시
    # 영어 다음에 (.)이 나오면 종료 표시 대신 마침표(.)의 점자를 찍음
    if (eng_text[-1] != '.'):
        # 제 31항 단위 부호로 끝날 경우 공백을 추가
        #   °C, °F
        #   %p
        if(eng_text[-1] in "%‰°′″Å"
                or (eng_text[-1] in "CF" and eng_text[-2] == "°")
                or (eng_text[-1] in "p" and eng_text[-2] == "%")):
            # 이미 공백이면 생략
            if(getChar(text, end+1) == " "):
                pass
            else:
                tran.append(' ')
        elif(getChar(text, end+1) is not None and (getChar(text, end+1).isnumeric() or getChar(text, end+1) == '.')):
            print("로마자 종료표 생략")
            pass
        else:   # 일반적인 경우 로마자 종료 표시
            eng_text = eng_text + brailleDB.eng_end

    for i in brailleDB.eng_word_abb_dict:
        eng_text = eng_text.replace(i, brailleDB.eng_word_abb_dict[i])

    print(eng_text)


    return "".join(eng_text)
