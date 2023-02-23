from tkinter import *
import tkinter.ttk as ttk
from tkinter import filedialog # 파일 선택 (__all__에 없어서), 파일창

import homeFunction
from UserClass import User

class Home:
  def __init__(self, user):
    self.__window=self.__createUI()
    self.__user = user
    self.word_list = None
    
  def __createUI(self):
    root = Tk()
    root.title("braille printer GUI")
    root.resizable(False, False) # x, y값 변경 불가(창 크기 변경 불가)

    #Label Frame
    labelFrame = Frame(root)
    labelFrame.pack(fill='x', padx=5, pady=5)

    label = Label(labelFrame, text='braille printer GUI')
    label.pack()

    # Text Fraem {scrollbar, text_place 2개가 들어감}

    text_frame = Frame(root)
    text_frame.pack(fill='both', padx=5, pady=5)

    scrollbar = Scrollbar(text_frame)
    scrollbar.pack(side='right', fill='y')

    self.text_place = Text(text_frame, height=20, yscrollcommand=scrollbar.set, state="normal")
    self.text_place.pack(side='left', fill='both', expand='True')
    scrollbar.config(command=self.text_place.yview)

    # Mode Frame {작성 모드, 파일 모드}

    mode_frame = LabelFrame(root, text="모드 선택")
    mode_frame.pack(fill='x', padx=5, pady=5)

    #######################################################
 
        
    #######################################################
    
    self.write_var = IntVar()
    write_radio_button = Radiobutton(mode_frame, text="작성모드", value=1, variable= self.write_var, command=self.mode_function)
    file_radio_button = Radiobutton(mode_frame, text="파일모드", value=2, variable= self.write_var, command=self.mode_function)



    write_radio_button.select()
    file_radio_button.pack(side='right')
    write_radio_button.pack(side='right')

    # File Select Frame

    button_Frame = Frame(root)
    button_Frame.pack(fill='x', padx=5, pady=5)

    self.file_selection_button = Button(button_Frame, width=13, height=1, text="파일 선택", command=self.getData, state="disabled")
    self.file_unselection_button = Button(button_Frame,  width = 13,height = 1, text="파일 해제", command=self.getData, state="disabled")

    self.file_unselection_button.pack(side="right", padx=3)
    self.file_selection_button.pack(side='right', padx=3)

    # 진행 상황 Progress Bar Frame
    frame_progress = LabelFrame(root, text='진행상황')
    frame_progress.pack(fill='x', padx=5, pady=5)

    p_var = DoubleVar()
    progress_bar = ttk.Progressbar(frame_progress, maximum=100, variable=p_var)
    progress_bar.pack(fill='x', padx=5, pady=5)

    # Print  Frame
    prit_Frmae = Frame(root)
    prit_Frmae.pack(fill='x', padx=5, pady=5)
    print_button = Button(prit_Frmae,  width = 13,height = 1, text="프린트 시작", command=self.startPrint)
    exit_button = Button(prit_Frmae,  width = 13,height = 1, text="닫기", command=lambda :root.quit())

    exit_button.pack(side='right', padx=3)
    print_button.pack(side='right', padx=3)
    return root
  
  
  def mode_function(self):
    num = self.write_var.get()
    
    if num==1: #작성모드
      self.text_place.config(state="normal")
      self.file_selection_button.config(state="disabled")
      self.file_unselection_button.config(state="disabled")
      self.text_place.delete("0.0", END)
      
      
    else: # 피일모드
      self.text_place.delete("0.0", END)
      self.text_place.config(state="disabled")
      self.file_selection_button.config(state="normal")
      self.file_unselection_button.config(state="normal")
      
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
    
    self.text_place.config(state='normal')
    # 텍스트 있을 수도 있으니까 삭제하고 집어넣기
    self.text_place.delete("0.0", END)	
    for c in self.word_list:
      self.text_place.insert(END, c[0])
    
    self.text_place.config(state='disabled')
    
   
  # 아두이노 구현
  def startPrint(self):
    pass
  
  def start(self):
    self.__window.mainloop() 