from tkinter import *



class UserFormerInfo:
  def __init__(self, historyList):
    self.historyList = historyList
    self.size = len(historyList)
    self.__window=self.__createUI()
    
  def __createUI(self):
    window=Tk()
    window.title("인쇄 기록")
    window.config(padx=20, pady=20)

    window.resizable(False, False)


    ############### text_frame #############
    text_frame = Frame(window)
    text_frame.pack(fill='both', padx=5, pady=5)

    scrollbar = Scrollbar(text_frame)
    scrollbar.pack(side='right', fill='y')

    text_place = Text(text_frame, height=20, yscrollcommand=scrollbar.set, state="normal")
    text_place.pack(side='left', fill='both', expand='True')
    scrollbar.config(command=text_place.yview)

    text_place.delete("0.0", END)	
    
    # "title": "test document title",
    # "page": 3,
    # "state": "인쇄중",
    # "submit_at": "2023-02-23T15:42:55.000Z"
    for history in self.historyList:
      title = history['title']
      page = history['page']
      state = history['state']
      submit_at = history['submit_at']
      string = \
      f'title: {title}\n\
      page: {page}\n\
      state: {state}\n\
      submit_at: {submit_at}\n\
      ===============================\n\n\n'
      text_place.insert(END, string)
    
    text_place.config(state='disabled')
    
    #Button
    button_frame = Frame(window)
    button_frame.pack(fill='x', padx=5, pady=5)

    login_button = Button(master=button_frame, text="확인완료", width=10, command = self.end)
    login_button.pack()
    return window
  
  
  def start(self):
    self.__window.mainloop()

  def end(self):
    self.__window.destroy()     


# historyList = [{"title": "test document title", "page": 3, "state": "인쇄중", "submit_at": "2023-02-23T15:42:55.000Z"},{"title": "test document title", "page": 3, "state": "인쇄중", "submit_at": "2023-02-23T15:42:55.000Z"},{"title": "test document title", "page": 3, "state": "인쇄중", "submit_at": "2023-02-23T15:42:55.000Z"},{"title": "test document title", "page": 3, "state": "인쇄중", "submit_at": "2023-02-23T15:42:55.000Z"},{"title": "test document title", "page": 3, "state": "인쇄중", "submit_at": "2023-02-23T15:42:55.000Z"},{"title": "test document title", "page": 3, "state": "인쇄중", "submit_at": "2023-02-23T15:42:55.000Z"}]
# a = UserInfo(historyList)
# a.start()