from tkinter import *
from tkinter import ttk

class DocumentPrintModify:
    def __init__(self, historyList):
        self.historyList = historyList
        self.size = len(historyList)
        self.__window = self.__createUI()
        self.__ids = []
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
            title = history['title']
            page = history['page']
            state = history['state']
            submit_at = history['submit_at']
            string = \
            f'\
            id:         {id}\
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

        combobox = ttk.Combobox(window, height=15, values=self.__ids)
        combobox.pack()

        login_button = Button(master=modify_frame, text="삭제하기 확인", width=10, command=self.modify)
        login_button.pack()
        return window

    def modify(self):

        pass

    def update(self):
        self.ids=[]
        self.text_place.config(state='normal')
        for history in self.historyList:
            title = history['title']
            page = history['page']
            self.ids.append(page)
            state = history['state']
            submit_at = history['submit_at']
            string = \
                f'title: {title}\n\
             page: {page}\n\
             state: {state}\n\
             submit_at: {submit_at}\n\
             ===============================\n\n\n'
            self.text_place.insert(END, string)

        self.text_place.config(state='disabled')

    def start(self):
        self.__window.mainloop()

    def end(self):
        self.__window.destroy()

    # historyList = [{"title": "test document title", "page": 3, "state": "인쇄중", "submit_at": "2023-02-23T15:42:55.000Z"},{"title": "test document title", "page": 3, "state": "인쇄중", "submit_at": "2023-02-23T15:42:55.000Z"},{"title": "test document title", "page": 3, "state": "인쇄중", "submit_at": "2023-02-23T15:42:55.000Z"},{"title": "test document title", "page": 3, "state": "인쇄중", "submit_at": "2023-02-23T15:42:55.000Z"},{"title": "test document title", "page": 3, "state": "인쇄중", "submit_at": "2023-02-23T15:42:55.000Z"},{"title": "test document title", "page": 3, "state": "인쇄중", "submit_at": "2023-02-23T15:42:55.000Z"}]
# a = UserInfo(historyList)
# a.start()