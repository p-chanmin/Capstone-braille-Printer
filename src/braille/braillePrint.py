# -*- coding: utf-8 -*-
import src.braille.brailleDB as db
from src.braille import hangul
import numpy as np

from src.braille.translate import translate


def CheckText(text):
    """
    문자열에서 점역이 불가능한 문자가 있는지 검사하는 함수
        :param text: 점역할 문자열
        :return: 문자열이 점역 가능하면 True, 그렇지 않으면 점역 불가능한 문자의 인덱스값을 가지는 리스트를 반환
    """

    nontranslatable_index = []

    for i in range(len(text)):
        if hangul.isHangul(text[i]):
            pass
        elif text[i] == " ":
            pass
        elif text[i] == "\n":
            pass
        elif text[i] in db.han_cho_dict:
            pass
        elif text[i] in db.han_jung_dict:
            pass
        elif text[i] in db.num_dict:
            pass
        elif text[i] in db.mark_dict:
            pass
        elif text[i] in db.eng_dict:
            pass
        elif text[i] in db.eng_mark_dict:
            pass
        else:
            nontranslatable_index.append(i)

    return True if len(nontranslatable_index) == 0 else nontranslatable_index


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

def transfrom_to_braille(braille_text, horizontal = 32):
    """
    점자 문자열을 가로칸에 맞춰 줄바꿈하고, 여백을 점자 공백으로 채우는 함수
        :param braille_text: 점자 문자열
        :param horizontal: 최대 가로칸
        :return: 최대 가로칸으로 줄바꿈(\n)한 점자 문자열
    """
    # 문자열처리를 위해 점자 공백을 일반 공백으로 변경
    braille_text = braille_text.replace("⠀", " ")

    words = braille_text.split(" ")  # 공백으로 단어로 나눔
    words_list = []  # 결과를 저장할 리스트

    # 가로길이에 맞게 단어 분할
    for word in words:
        while len(word) > horizontal:  # 단어가 horizontal글자보다 길 경우
            words_list.append(word[:horizontal])  # horizontal글자까지 자른 후 추가
            word = word[horizontal:]  # 나머지 단어로 다시 반복

        words_list.append(word)  # horizontal글자 이하인 단어는 그대로 추가

    # 최대 길이 horizontal으로 나누기
    lines = []
    line = ''
    # 단어 목록을 순회하면서 줄바꿈
    for word in words_list:
        # 단어를 추가했을 때 가로보다 길면 라인을 추가하고, 새로운 라인 생성
        if len(line) + len(word) + 1 > horizontal:
            lines.append(line)
            line = ""
        # 단어 중간에 줄바꿈 표가 있을 경우 줄바꿈을 우선으로 라인 생성
        if "\n" in word:
            split_words = word.split("\n")
            for i, split_word in enumerate(split_words):
                if len(line) + len(split_word) + 1 > horizontal:
                    lines.append(line)
                    line = ""
                else:
                    if line:
                        line += " "
                    line += split_word
        # 그렇지 않으면 공백으로 단어 추가
        else:
            if line:
                line += " "
            line += word

    # 마지막 라인이 있으면 추가
    if line:
        lines.append(line)

    # 모든 줄을 넘파이 배열로 변환
    chunks = np.array(lines)

    # 패딩할 점자 공백("⠀")
    pad_char = "⠀"

    # 각 문자열에 대해 패딩을 적용하여 가로칸을 맞춤
    padded_array = []
    for s in chunks:
        if len(s) < horizontal:
            pad_length = horizontal - len(s)
            padded_string = s + pad_char * pad_length
        else:
            padded_string = s
        # 문자열에서 공백을 데이터화 가능한 점자 공백("⠀")으로 변경
        padded_array.append(padded_string.replace(" ", "⠀"))

    return "\n".join(padded_array)

def transform_to_print(braille_text):
    """
    점자 문자열을 출력 데이터폼으로 변경하는 함수
        :param braille_text: 줄 바꿈 된 점자 문자열
        :param horizontal: 가로줄의 최대 칸 수
        :return: 인쇄를 위한 데이터 출력 위치에 1, 아닌 위치는 0인 리스트 반환
    """

    padded_array = braille_text.split("\n")

    result_form = []
    # 각 줄마다 데이터화 하여 인쇄 형태로 변형
    for line in padded_array:
        line_form = []
        for c in line:
            # 점자를 문자열 데이터로 변경
            str_data = braille_to_data(c)
            lst = [[int(str_data[i]), int(str_data[i + 3])] for i in range(3)]
            # 데이터를 넘파이 배열로 저장
            data = np.array(lst)
            line_form.append(data)

        # 한 줄의 점자 데이터들을 3줄의 점 데이터로 변형
        dot_data = np.concatenate(line_form, axis=1)
        for d in dot_data:
            # 데이터를 역순으로 하여 인쇄 시 찍어야하는 위치로 변형
            # 최종 결과 폼에 저장
            result_form.append(d[::-1])

    return result_form

def get_page(braille_text, vertical = 26):
    line = len(braille_text.split("\n"))
    return line//vertical if(line%vertical == 0) else line//vertical + 1

# test_text = "3D 프린터―3차원 설계도를 보고 입체적인 물건을 인쇄하는 프린터\n3차원 프린터는 어떤 원리로 물건을 인쇄할까? 3차원 프린터는 입체적으로 그려진 물건을 마치 미분하듯이 가로로 1만 개 이상 잘게 잘라 분석한다. 그리고 아주 얇은 막(레이어)을 한 층씩 쌓아 물건의 바닥부터 꼭대기까지 완성한다. 잉크젯 프린터가 빨강, 파랑, 노랑 세 가지 잉크를 조합해 다양한 색상을 만드는 것처럼 3차원 프린터는 설계에 따라 레이어의 위치를 조절해 쌓아 올린다. 지금까지 개발된 3차원 프린터는 1시간당 높이 2.8cm를 쌓아 올린다. 레이어의 두께는 약 0.01~0.08mm로 종이 한 장보다도 얇다. 쾌속 조형 방식으로 인쇄한 물건은 맨 눈에는 곡선처럼 보이는 부분도 현미경으로 보면 계단처럼 들쭉날쭉하다. 그래서 레이어가 얇으면 얇을수록 물건이 더 정교해진다."
# str = translate(test_text)
# print(str)
# result_str = transfrom_to_braille(str, 32)
# result_data = transform_to_print(result_str)
#
# print(f"({result_str})")
# print()
# for i in result_data:
#     print(f"{len(i)} : {i}")
# print(get_page(result_str))


