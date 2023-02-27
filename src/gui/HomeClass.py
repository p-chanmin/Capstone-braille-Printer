import threading
import time

from tkinter import *
import tkinter.ttk as ttk
from tkinter import filedialog # 파일 선택 (__all__에 없어서), 파일창
import tkinter.messagebox as msgbox


from src.gui.SpecialCharacterUIClass import SpecialCharacterUI
from src.braille.braillePrint import CheckText
from src.braille.translate import translate

from src.gui.CharThreadClass import CharThread
from src.gui import serverFunction, homeFunction
from src.gui.UserClass import User
from src.gui.DocumentPrintClass import DocumentPrint
from src.gui.DocumentPrintModifyClass import DocumentPrintModify
from src.gui.DocumentPrintDeleteClass import DocumentPrintDelete


class Home():
  def __init__(self, user):
    self.__user = user
    self.__window=self.__createUI()

    #self.text_place내에 있던 문자들 중에 점자 번역 매칭 안되는 문자들에 대한 text내 인덱스를 가지고 있는 리스트
    self.markIdx_lst = []
    self.Ungrammatical_ch_count = -1
    self.Ungrammatical_ch_idxList = []
    self.Ungrammatical_string = None

  def __createUI(self):
    root = Tk()
    root.title("braille printer GUI")
    root.resizable(False, False) # x, y값 변경 불가(창 크기 변경 불가)

   # Menu
   # menu = Menu(root, background='blue')
    menu = Menu(root)
    menu.config(background='blue')
    
    menu_1 = Menu(menu, tearoff=0)
    menu_1.add_command(label="인쇄 문서 기록 확인", command=self.print_information_function)
    menu_1.add_command(label="인쇄 문서 상태 변경", command=self.print_information_state_modify_function)
    menu_1.add_command(label="인쇄 문서 기록 삭제", command=self.print_information_delete_function)

    menu.add_cascade(label="인쇄 정보", menu=menu_1)

    menu_2 = Menu(menu, tearoff=0)
    menu_2.add_command(label="내 정보 더보기", command=self.more_my_information_function)
    menu_2.add_separator()
    menu_2.add_command(label="로그아웃", command=self.exit)
    menu_2.add_command(label="회원 탈퇴", command=self.user_delete)
    menu_2.add_separator()
    menu_2.add_command(label="종료", command= self.quit)
    menu.add_cascade(label="내 정보", menu=menu_2)

    menu_3 = Menu(menu, tearoff=0)
    menu_3.add_command(label="특수문자 도움말", command=lambda : self.createSpecialChacterUI())
    menu.add_cascade(label="도움말", menu=menu_3)

    root.config(menu=menu)


    #Label Frame
    labelFrame = Frame(root)
    labelFrame.pack(fill='x', padx=5, pady=5)

    label = Label(labelFrame, text='braille printer GUI')
    label.pack()
    
    user_email =  self.__user.getEmail()
    email_label = Label(labelFrame, text="email "+user_email)
    email_label.pack(fill='x', side='right')

    # Text Fraem {scrollbar, text_place 2개가 들어감}

    text_frame = Frame(root)
    text_frame.pack(fill='both', padx=5, pady=5)

    scrollbar = Scrollbar(text_frame)
    scrollbar.pack(side='right', fill='y')

    self.text_place = Text(text_frame, height=20, yscrollcommand=scrollbar.set, state="normal")
    self.text_place.mark_set("","0.0")
    self.text_place.pack(side='left', fill='both', expand='True')
    scrollbar.config(command=self.text_place.yview)

  # Text Button Frame {Text_Button_Frame={left_button_frame, right_button_frame} }
    Text_Button_Frame = Frame(root)
    Text_Button_Frame.pack(fill='both', padx=5, pady=5)
    
    # -------------- left_button_frame--------------
    left_button_frame = Frame(Text_Button_Frame)
    left_button_frame.pack(fill='x', padx=5, pady=5, side='left')
    
    # -------------- left_button_frame 버튼 1행 --------------
    special_characters_button = Button(left_button_frame, width=15, pady=2, text="특수 문자 추가", command=self.createSpecialChacterUI)

    # -------------- left_button_frame 버튼 배치 --------------
    special_characters_button.grid(row=0, column=0, padx=2, pady=2)


    # -------------- right_button_frame--------------
    right_button_frame = Frame(Text_Button_Frame)
    right_button_frame.pack(fill='x', padx=5, pady=5, side='right')
    
    # -------------- right_button_frame 버튼 1행 --------------
    check_button = Button(right_button_frame, width=5, pady=2, text="검사", command=self.check_braille_grammar)
    self.ungramatic_cnt_label = Label(right_button_frame, width=30, pady=2, text=f'문법 오류 개수: 0개')
    Braille_button = Button(right_button_frame, width=5, pady=2, text="점역", command=self.braille_review)

    # -------------- right_button_frame 버튼 배치 --------------
    check_button.grid(row=0, column=0, padx=2 ,pady=2)
    self.ungramatic_cnt_label.grid(row=0, column=1, padx=2, pady=2)
    Braille_button.grid(row=0, column=3, padx=2 ,pady=2)

  # -------------- braille Fraem --------------

    braille_frame = LabelFrame(root, text="점자 번역")
    braille_frame.pack(fill='both', padx=5, pady=5)

    scrollbar = Scrollbar(braille_frame)
    scrollbar.pack(side='right', fill='y')

    self.braille_place = Text(braille_frame, height=20, yscrollcommand=scrollbar.set, state="disabled")
    self.braille_place.pack(side='left', fill='both', expand='True')
    scrollbar.config(command=self.braille_place.yview)

  # -------------- Mode Frame {작성 모드, 파일 모드} --------------

    mode_frame = LabelFrame(root, text="모드 선택")
    mode_frame.pack(fill='x', padx=5, pady=5)
    
    self.write_var = IntVar()
    write_radio_button = Radiobutton(mode_frame, text="작성모드", value=1, variable= self.write_var, command=self.mode_function)
    file_radio_button = Radiobutton(mode_frame, text="파일모드", value=2, variable= self.write_var, command=self.mode_function)


    write_radio_button.select()
    file_radio_button.pack(side='right')
    write_radio_button.pack(side='right')

  # -------------- File Select Frame --------------

    button_Frame = Frame(root)
    button_Frame.pack(fill='x', padx=5, pady=5)

    self.file_selection_button = Button(button_Frame, width=13, height=1, text="파일 선택", command=self.getData, state="disabled")
    self.file_unselection_button = Button(button_Frame,  width = 13,height = 1, text="파일 해제", command=self.getData, state="disabled")

    self.file_unselection_button.pack(side="right", padx=3)
    self.file_selection_button.pack(side='right', padx=3)

  # -------------- 진행 상황 Progress Bar Frame --------------
    frame_progress = LabelFrame(root, text='진행상황')
    frame_progress.pack(fill='x', padx=5, pady=5)

    p_var = DoubleVar()
    progress_bar = ttk.Progressbar(frame_progress, maximum=100, variable=p_var)
    progress_bar.pack(fill='x', padx=5, pady=5)

  # -------------- Print  Frame --------------
    prit_Frmae = Frame(root)
    prit_Frmae.pack(fill='x', padx=5, pady=5)
    print_button = Button(prit_Frmae,  width = 13,height = 1, text="프린트 시작", command=self.startPrint)
    exit_button = Button(prit_Frmae,  width = 13,height = 1, text="닫기", command=lambda :root.quit())

    exit_button.pack(side='right', padx=3)
    print_button.pack(side='right', padx=3)
    return root
  
  
  
  ############################# menu function ###################################
  
  # 이전 프린트 목록 보여주기
  def print_information_function(self):

    #historyList = [{"title": "test document title", "page": 3, "state": "인쇄중", "submit_at": "2023-02-23T15:42:55.000Z"}, {"title": "test document title", "page": 3, "state": "인쇄중", "submit_at": "2023-02-23T15:42:55.000Z"}, {"title": "test document title", "page": 3, "state": "인쇄중", "submit_at": "2023-02-23T15:42:55.000Z"}, {"title": "test document title", "page": 3, "state": "인쇄중", "submit_at": "2023-02-23T15:42:55.000Z"}, {"title": "test document title", "page": 3, "state": "인쇄중", "submit_at": "2023-02-23T15:42:55.000Z"}, {"title": "test document title", "page": 3, "state": "인쇄중", "submit_at": "2023-02-23T15:42:55.000Z"}]
    historyList = serverFunction.get_print_documents(self.__user)

    # 못받아오면 경고 // 아무것도 없으면 경고
    if historyList is None or len(historyList) ==0:
      msgbox.showerror(title="불러오기 실패", message="불러오기를 실패했습니다.")
    else:
      uInfo = DocumentPrint(historyList)
      uInfo.start()

  def print_information_state_modify_function(self):
    # historyList = [{"title": "test document title", "page": 3, "state": "인쇄중", "submit_at": "2023-02-23T15:42:55.000Z"}, {"title": "test document title", "page": 3, "state": "인쇄중", "submit_at": "2023-02-23T15:42:55.000Z"}, {"title": "test document title", "page": 3, "state": "인쇄중", "submit_at": "2023-02-23T15:42:55.000Z"}, {"title": "test document title", "page": 3, "state": "인쇄중", "submit_at": "2023-02-23T15:42:55.000Z"}, {"title": "test document title", "page": 3, "state": "인쇄중", "submit_at": "2023-02-23T15:42:55.000Z"}, {"title": "test document title", "page": 3, "state": "인쇄중", "submit_at": "2023-02-23T15:42:55.000Z"}]
    historyList = serverFunction.get_print_documents(self.__user)

    # 못받아오면 경고 // 아무것도 없으면 경고
    if historyList is None or len(historyList) == 0:
      msgbox.showerror(title="불러오기 실패", message="불러오기를 실패했습니다.")
    else:
      uInfo = DocumentPrintModify(historyList)
      uInfo.start()

  def print_information_delete_function(self):
    # historyList = [{"title": "test document title", "page": 3, "state": "인쇄중", "submit_at": "2023-02-23T15:42:55.000Z"}, {"title": "test document title", "page": 3, "state": "인쇄중", "submit_at": "2023-02-23T15:42:55.000Z"}, {"title": "test document title", "page": 3, "state": "인쇄중", "submit_at": "2023-02-23T15:42:55.000Z"}, {"title": "test document title", "page": 3, "state": "인쇄중", "submit_at": "2023-02-23T15:42:55.000Z"}, {"title": "test document title", "page": 3, "state": "인쇄중", "submit_at": "2023-02-23T15:42:55.000Z"}, {"title": "test document title", "page": 3, "state": "인쇄중", "submit_at": "2023-02-23T15:42:55.000Z"}]
    historyList = serverFunction.get_print_documents(self.__user)

    # 못받아오면 경고 // 아무것도 없으면 경고
    if historyList is None or len(historyList) == 0:
      msgbox.showerror(title="불러오기 실패", message="불러오기를 실패했습니다.")
    else:
      uInfo = DocumentPrintDelete(self.__user, historyList)
      uInfo.start()

  def more_my_information_function(self):
    # None or dict
    u_dict = serverFunction.get_user_info(self.__user)

    if u_dict is None or u_dict['result'] !='ok':
      msgbox.showerror(title="불러오기 실패", message="불러오기를 실패했습니다.")
    else:
      msgbox.showinfo(title="유저 정보", message=f"email: {u_dict['email']}\nname: {u_dict['name']}")
  def user_delete(self):
    email = self.__user.getEmail()
    question = msgbox.askyesno(title="회원 탈퇴", message=f"{email} 회원을 탈퇴합니다")
    
    if(question):
      isDelUser = serverFunction.user_delete(self.__user)
      if(isDelUser):
        msgbox.showinfo(title="탈퇴 성공", message="회원 탈퇴에 성공했습니다")
        self.exit()
      else:
        msgbox.showerror(title="탈퇴 실패", message="회원 탈퇴에 실패했습니다")

  ############################# mode function ###################################
  
  def mode_function(self):
    num = self.write_var.get()
    
    if num==1: #작성모드
      self.text_place.delete("0.0", END)
      self.file_selection_button.config(state="disabled")
      self.file_unselection_button.config(state="disabled")
      
      
    else: # 피일모드
      self.text_place.delete("0.0", END)	
      self.text_place.config(state="disabled")
      self.file_selection_button.config(state="normal")
      self.file_unselection_button.config(state="normal")
      
  ############################# getDate function ###################################

  def getData(self):
    # 파일의 절대 위치 경로를 리턴받음
    filepath = filedialog.askopenfilename(title="워드 파일 선택", filetypes=(("docx 파일",'*.docx'), ("hwp 파일",'*.hwp'), ("pdf 파일",'*.pdf'), ("txt 파일",'*.txt'), ("모든 파일", "*.*")), initialdir=r"C:\Users\JDoubleU\Desktop")
    
    # 파일 확장자명 알기
    extension = filepath.split('.')[-1]
    
    if extension == 'docx':
      self.word_list = homeFunction.get_word(filepath)
    elif extension == 'hwp':
      pass
    elif extension == 'pdf':
      self.word_list = homeFunction.get_pdf(filepath)
    elif extension == 'txt':
      self.word_list =  homeFunction.get_txt(filepath)
    else:
      print("Unknown extension")
      return;
    
    # 텍스트 있을 수도 있으니까 삭제하고 집어넣기
    self.text_place.delete("0.0", END)	
    self.text_place.config(state='normal')
    
    #self.wort_list에는 파일에서 or 작성모드에서 작성한 글자들, 대응되는 유니코드 값들이 있음
    # ex) "abc" -> word_list = [(a, 65),(c, 67),(b, 66)]
    for c in self.word_list:
      self.text_place.insert(END, c[0])
    ############################# left button function ###################################

  def createSpecialChacterUI(self):
    SpecialCharacterUI(self).start()
  ############################# right button function ###################################
  def check_braille_grammar(self):
    string = self.text_place.get("1.0", END)

    self.Ungrammatical_ch_count = -1
    self.Ungrammatical_ch_idxList = []
    self.Ungrammatical_string = None



    # 문자열이 완벽하면 true / 고쳐야될 부분 있으면 해당인덱스를 포함하는 리스트 반환
    lst = CheckText(string)
    self.markIdx_lst = []
    if(lst == True):
      self.Ungrammatical_ch_count = 0
      msgbox.showinfo(title="점자 해독 가능", message="점자 해독이 가능합니다. 오른쪽에 점역 버튼을 눌러주세요")
    else:
      print("오류오류!!!!!")
      print(lst)
      count=0
      string = self.text_place.get("1.0", END)
      self.text_place.delete("1.0", END)

      self.Ungrammatical_ch_count = len(lst)
      self.Ungrammatical_ch_idxList = lst
      self.Ungrammatical_string = string

      past_idx = 0
      cur_idx = 0
      self.markIdx_lst = []
      for i in range(len(lst)):
        cur_idx = lst[i]
        self.text_place.insert(END, string[past_idx:cur_idx])
        self.markIdx_lst.append(self.text_place.index(CURRENT))
        print(cur_idx, self.text_place.index(CURRENT))
        self.text_place.insert(END, string[cur_idx])
        past_idx = cur_idx + 1

      if past_idx < len(string):
        self.text_place.insert(END, string[past_idx:])

      for idx in self.markIdx_lst:
        size = len("".join(idx).split(".")[-1])
        idx2 = round(float(idx) + 10 ** (-size), size + 1)
        self.text_place.tag_add("강조", idx, idx2)
      self.text_place.tag_config("강조", background="yellow")

      msgbox.showerror(title="점자 해독 불가", message="점자 해독이 불가능 합니다")
      self.createCharThread()

  def createCharThread(self):
    t = CharThread(self)
    t.daemon = True
    t.start()
  def go2Left(self):
    pass  
  
  def go2Right(self):
    pass
  
  # 점자 미리보기 구현 함수
  def braille_review(self):
    string = self.text_place.get("1.0", END)
    if (CheckText(string)):
      tanslated_braille = translate(string)
      self.braille_place.config(state="normal")
      self.braille_place.delete("1.0", END)
      self.braille_place.insert(END, tanslated_braille)
      self.braille_place.config(state="disabled")
    else:
      msgbox.showerror(title="점자 해독 불가", message="점자 해독이 불가능 합니다")
  
  ############################# arduino function ###################################
  def startPrint(self):
    pass


  ############################# process function ###################################  
  def start(self):
    self.__window.mainloop()
    
  
  def exit(self):
    del(self.__user)
    self.__window.destroy()

  def quit(self):
    self.__window.quit()
    
#####################################################################################
