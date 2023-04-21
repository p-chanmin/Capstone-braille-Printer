from tkinter import *
from tkinter import ttk
import tkinter.messagebox as msgbox

from src.gui import serverFunction


class DocumentPrintDelete:
    def __init__(self, user, historyList, homeUI):
        self.__user = user
        self.__ids = []
        self.historyList = historyList
        self.size = len(historyList)
        self.homeUI = homeUI
        self.__window = self.__createUI()

    def __createUI(self):
        window = Tk()
        window.title("인쇄 기록")
        window.config(padx=20, pady=20)

        window.resizable(False, False)

        ############### main_frame ############# {text_frame,modify_frame}
        main_Frame = Frame(window)
        main_Frame.pack(fill='both', padx=5, pady=5)

        ############### text_frame #############
        text_frame = Frame(main_Frame)
        text_frame.pack(fill='both', padx=5, pady=5, side='left')

        scrollbar = Scrollbar(text_frame)
        scrollbar.pack(side='right', fill='y')

        self.text_place = Text(text_frame, height=20, yscrollcommand=scrollbar.set, state="normal")
        self.text_place.pack(side='left', fill='both', expand='True')
        scrollbar.config(command=self.text_place.yview)

        self.text_place.delete("0.0", END)

        # "title": "test document title",
        # "page": 3,
        # "state": "인쇄중",
        # "submit_at": "2023-02-23T15:42:55.000Z"
        for history in self.historyList:
            id = history['id']
            self.__ids.append(id)
            title = history['title']
            page = history['page']
            state = history['state']
            submit_at = history['submit_at']
            string = \
            f'\
            id:       {id}\
            title:      {title}\n\
            page:       {page}\n\
            state:      {state}\n\
            submit_at:  {submit_at}\n\
            ===============================\n\n\n'
            self.text_place.insert(END, string)

        self.text_place.config(state='disabled')

        ############### modify_frame #############
        modify_frame = Frame(main_Frame)
        modify_frame.pack(fill='x', padx=5, pady=5, side='right')

        self.combobox = ttk.Combobox(modify_frame, height=15, values=self.__ids)
        self.combobox.pack(pady=3)
        self.combobox.set("id 선택")
        delete_button = Button(master=modify_frame, text="삭제하기", width=10, command=self.modify)
        delete_button.pack(pady=3)

        load_button = Button(master=modify_frame, text="불러오기", width=10, command=self.load)
        load_button.pack(pady=3)

        return window

    def load(self):
        user = self.__user
        selected_id = self.combobox.get() #문자열
        print(selected_id)
        result = serverFunction.load_print_document(user, selected_id)
        print(result)
        if result[0]:
            self.homeUI.text_place.delete("1.0", END)
            self.homeUI.text_place.insert(END, result[1])
            self.homeUI.braille_place.config(state="normal")
            self.homeUI.braille_place.delete("1.0", END)
            self.homeUI.braille_place.insert(END, result[2])
            self.homeUI.braille_place.config(state="disabled")

            msgbox.showinfo(title="불러오기 성공", message="불러오기 성공")
        else:
            msgbox.showerror(title="불러오기 실패", message="불러오기 실패")

    def modify(self):
        user = self.__user
        selected_id = self.combobox.get() #문자열
        print(selected_id)
        if serverFunction.delete_print_document(user, selected_id):
            self.update()
            msgbox.showerror(title="삭제 성공", message="삭제 성공")

        else:
            msgbox.showerror(title="삭제 실패", message="삭제 실패")


    def update(self):
        historyList = serverFunction.get_print_documents(self.__user)

        # 못받아오면 경고 // 아무것도 없으면 경고
        if historyList is None or len(historyList) == 0:
           return



        self.__ids = []
        self.text_place.config(state='normal')
        self.text_place.delete("1.0", END)

        print("update")
        print(self.text_place.get("1.0",END))
        print(historyList)

        for history in historyList:
            id = history['id']
            self.__ids.append(id)
            title = history['title']
            page = history['page']
            state = history['state']
            submit_at = history['submit_at']
            string = \
            f'\
            id:         {id}\n\
            title:      {title}\n\
            page:       {page}\n\
            state:      {state}\n\
            submit_at:  {submit_at}\n\
            ===============================\n\n\n'
            self.text_place.insert(END, string)

        self.text_place.config(state='disabled')
        self.combobox.config(values=self.__ids)
    def start(self):
        self.__window.mainloop()

    def end(self):
        self.__window.destroy()

    # historyList = [{"title": "test document title", "page": 3, "state": "인쇄중", "submit_at": "2023-02-23T15:42:55.000Z"},{"title": "test document title", "page": 3, "state": "인쇄중", "submit_at": "2023-02-23T15:42:55.000Z"},{"title": "test document title", "page": 3, "state": "인쇄중", "submit_at": "2023-02-23T15:42:55.000Z"},{"title": "test document title", "page": 3, "state": "인쇄중", "submit_at": "2023-02-23T15:42:55.000Z"},{"title": "test document title", "page": 3, "state": "인쇄중", "submit_at": "2023-02-23T15:42:55.000Z"},{"title": "test document title", "page": 3, "state": "인쇄중", "submit_at": "2023-02-23T15:42:55.000Z"}]
# a = UserInfo(historyList)
# a.start()