from tkinter import *

class BrailleCharInfo:
    def __init__(self, hoemClassInstance):
        self.__createUI(hoemClassInstance)
        print(id(hoemClassInstance))
        print(id(self))

    def __createUI(self, hoemClassInstance):
        self.BCUIinstance = Tk()
        self.BCUIinstance.title("특수문자 안내")
        self.BCUIinstance.config(padx=20, pady=20)

        self.BCUIinstance.resizable(False, False)

        # -------------- Char_button_frame--------------
        self.char_button_frame = Frame(self.BCUIinstance)
        self.char_button_frame.pack(fill='x', padx=5, pady=5)

        # -------------- Char_button_frame 버튼 1행 --------------
        self.double_quotationLeft_button = Button(self.char_button_frame, width=15, pady=2, text="“\n여는 큰 따옴표",
                                             command=lambda: hoemClassInstance.text_place.insert(END, "“"))
        self.double_quotationRight_button = Button(self.char_button_frame, width=15, pady=2, text="”\n닫는 큰 따옴표",
                                              command=lambda: hoemClassInstance.text_place.insert(END, "”"))
        self.single_quotationLeft_button = Button(self.char_button_frame, width=15, pady=2, text="‘\n여는 작은 따옴표",
                                             command=lambda: hoemClassInstance.text_place.insert(END, "‘"))
        self.single_quotationRight_button = Button(self.char_button_frame, width=15, pady=2, text="’\n닫는 작은 따옴표",
                                              command=lambda: hoemClassInstance.text_place.insert(END, "’"))
        self.comma_button = Button(self.char_button_frame, width=15, pady=2,text=",\n아포스트로피",
                              command=lambda: hoemClassInstance.text_place.insert(END, ","))

        # -------------- Char_button_frame 버튼 2행 --------------

        self.hyphen_button = Button(self.char_button_frame, width=15, pady=2, text="‐\n붙임표",
                               command=lambda: hoemClassInstance.text_place.insert(END, "‐"))
        self.dash_button = Button(self.char_button_frame, width=15, pady=2, text="–\n줄표",
                             command=lambda: hoemClassInstance.text_place.insert(END, "–"))
        self.long_dash_button = Button(self.char_button_frame, width=15, pady=2, text="―\n긴 줄표",
                                  command=lambda: hoemClassInstance.text_place.insert(END, "―"))
        self.minus_button = Button(self.char_button_frame, width=15, pady=2, text="−\n빼기",
                              command=lambda: hoemClassInstance.text_place.insert(END, "−"))

        # -------------- char_button_frame 버튼 배치 --------------
        self.double_quotationLeft_button.grid(row=0, column=0, padx=2, pady=2)
        self.double_quotationRight_button.grid(row=0, column=1, padx=2, pady=2)
        self.single_quotationLeft_button.grid(row=0, column=2, padx=2, pady=2)
        self.single_quotationRight_button.grid(row=0, column=3, padx=2, pady=2)
        self.comma_button.grid(row=0, column=4, padx=2, pady=2)
        self.hyphen_button.grid(row=1, column=0, padx=2, pady=2)
        self.dash_button.grid(row=1, column=1, padx=2, pady=2)
        self.long_dash_button.grid(row=1, column=2, padx=2, pady=2)
        self.minus_button.grid(row=1, column=3, padx=2, pady=2)

        # -------------- cancel_button_frame 버튼 배치 --------------
        self.cancel_button_frame = Frame(self.BCUIinstance)
        self.cancel_button_frame.pack(fill='x', padx=5, pady=5)

        self.cancel_button = Button(self.cancel_button_frame, width=15, pady=2, text="닫기",
                              command=self.end)
        self.cancel_button.pack()

    def start(self):
        self.BCUIinstance.mainloop()
    def end(self):
        self.BCUIinstance.destroy()


 # a= UserFormerInfo()