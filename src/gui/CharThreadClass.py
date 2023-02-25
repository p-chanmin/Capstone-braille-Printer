from tkinter import *
import threading
import time

from src.braille.braillePrint import CheckText

class CharThreadClass(threading.Thread):
    def __init__(self, homeInstance):
        super().__init__()
        self.homeInstance = homeInstance
        self.count = 0

    # override
    def run(self):
        print("run 함")
        while (True):
            for idx in  self.homeInstance.markIdx_lst:
                size = len("".join(idx).split(".")[-1])
                idx2 = round(float(idx) + 10 ** (-size), size + 1)
                ch = self.homeInstance.text_place.get(idx, idx2)


            string = self.homeInstance.text_place.get("1.0", END)

            lst = CheckText(string)
            self.incorrect_word_list = []
            if(lst == True):
                pass
            else:
                count = 0
                string = self.text_place.get("1.0", END)

                past_idx = 0
                cur_idx = len(lst)
                markIdx_lst = []
                for i in range(len(lst)):
                    cur_idx = lst[i]

                    self.text_place.insert(END, string[past_idx:cur_idx])
                    markIdx_lst.append(self.text_place.index(CURRENT))

                    self.text_place.insert(END, string[cur_idx])
                    past_idx = cur_idx + 1

                if past_idx < len(string):
                    self.text_place.insert(END, string[past_idx:])

                for idx in markIdx_lst:
                    size = len("".join(idx).split(".")[-1])
                    idx2 = round(float(idx) + 10 ** (-size), size + 1)
                    self.text_place.tag_add("강조", idx, idx2)
                self.text_place.tag_config("강조", background="yellow")

