# -*- coding: utf-8 -*-
import brailleDB as db
from src.braille import hangul

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
