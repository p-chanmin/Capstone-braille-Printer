from tkinter import *
import threading
from src.braille.braillePrint import CheckText
from src.gui import homeFunction
import tkinter.messagebox as msgbox

import time

from src.braille.braillePrint import CheckText

class CharThread(threading.Thread):
    def __init__(self, homeInstance):
        super().__init__()
        self.homeInstance = homeInstance
        self.count = 0

    def run(self):
        # 원본 스트링 일반 인덱스 적용
        # 수정 스트링 일반 인덱스 적용
        print("thread Run!")
        homeInstance = self.homeInstance

        original_string = homeInstance.text_place.get("1.0", END)
        # 원본 스트링에 대한 Tk인덱스 리스트["1.4", "3.2"]
        original_idxList = homeInstance.Ungrammatical_ch_idxList


        while len(original_idxList) > 0:
            cur_string = homeInstance.text_place.get("1.0", END)
            # 수정 스티링에 대한 Tk인덱스 리스트
            cur_idxList = CheckText(cur_string)

            if cur_idxList == True:
                break

            homeInstance.ungramatic_cnt_label.config(text=f"문법 오류 개수: {len(cur_idxList)}개")

        msgbox.showinfo(title="오류 제거 완료", message="오류가 모두 제거 되었습니다.\n검사 버튼을 다시 눌러 주세요")
        homeInstance.ungramatic_cnt_label.config(text=f"문법 오류 개수: {0}개")


    #============== 찐===============
    # def run(self):
    #     print('thread run')
    #     ungramatic_idx_lst = self.homeInstance.Ungrammatical_ch_idxList
    #     past_ungramatic_string = self.homeInstance.Ungrammatical_string
    #
    #     past_string_cnt = len(self.homeInstance.text_place.get("1.0", END))
    #
    #     try:
    #         print(len(past_ungramatic_string), past_string_cnt)
    #     except TypeError as e:
    #         past_ungramatic_string=[]
    #         print(len(past_ungramatic_string), past_string_cnt)
    #
    #     cur_ungramatic_idx_lst = ungramatic_idx_lst
    #     while(len(ungramatic_idx_lst) > 0):
    #         cur_string = self.homeInstance.text_place.get("1.0", END)
    #         difference = (len(cur_string) -1)- len(past_ungramatic_string)
    #
    #         print("31")
    #         print(cur_ungramatic_idx_lst)
    #         if difference != 0:
    #             cur_ungramatic_idx_lst = list(map(lambda x:x+1, cur_ungramatic_idx_lst))
    #         print("33")
    #         print(cur_ungramatic_idx_lst)
    #         del_idx = []
    #         for past_idx, cur_idx in zip(ungramatic_idx_lst, cur_ungramatic_idx_lst):
    #             if past_ungramatic_string[past_idx] == cur_string[cur_idx]:
    #                 pass
    #             else: # 틀린 문법 고쳤음
    #                 del_idx.append((past_idx, cur_idx))
    #         print("43")
    #         print(del_idx)
    #
    #         try:
    #             for idx in del_idx[::-1]:
    #                 del ungramatic_idx_lst[idx[0]]
    #                 del cur_ungramatic_idx_lst[idx[1]]
    #         except IndexError as e:
    #             break
    #
    #         print("49")
    #         print(ungramatic_idx_lst)
    #         self.homeInstance.ungramatic_cnt_label.config(text=f'문법 오류 개수: {len(ungramatic_idx_lst)}개')
    #
    #     print("end")

    ## override
    # def run(self):
    #     print("run 함")
    #     while (True):
    #         for idx in  self.homeInstance.markIdx_lst:
    #             size = len("".join(idx).split(".")[-1])
    #             idx2 = round(float(idx) + 10 ** (-size), size + 1)
    #             ch = self.homeInstance.text_place.get(idx, idx2)
    #
    #
    #         string = self.homeInstance.text_place.get("1.0", END)
    #
    #         lst = CheckText(string)
    #         self.incorrect_word_list = []
    #         if(lst == True):
    #             pass
    #         else:
    #             count = 0
    #             string = self.text_place.get("1.0", END)
    #
    #             past_idx = 0
    #             cur_idx = len(lst)
    #             markIdx_lst = []
    #             for i in range(len(lst)):
    #                 cur_idx = lst[i]
    #
    #                 self.text_place.insert(END, string[past_idx:cur_idx])
    #                 markIdx_lst.append(self.text_place.index(CURRENT))
    #
    #                 self.text_place.insert(END, string[cur_idx])
    #                 past_idx = cur_idx + 1
    #
    #             if past_idx < len(string):
    #                 self.text_place.insert(END, string[past_idx:])
    #
    #             for idx in markIdx_lst:
    #                 size = len("".join(idx).split(".")[-1])
    #                 idx2 = round(float(idx) + 10 ** (-size), size + 1)
    #                 self.text_place.tag_add("강조", idx, idx2)
    #             self.text_place.tag_config("강조", background="yellow")

