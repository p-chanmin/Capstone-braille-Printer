from tkinter import filedialog # 파일 선택 (__all__에 없어서), 파일창
from tkinter import *
import homeFunction

def mode_function():
  pass

def add_file(text_place):
  # initialdir에 초기 폴더 위치 넣으면 됨
  
  # 파일의 절대 위치 경로를 리턴받음
  filepath = filedialog.askopenfilename(title="워드 파일 선택", filetypes=(("docx 파일",'*.docx'), ("hwp 파일",'*.hwp'), ("pdf 파일",'*.pdf'), ("txt 파일",'*.txt'), ("모든 파일", "*.*")), initialdir=r"C:\Users\JDoubleU\Desktop")
  
  # 파일 확장자명 알기
  extension = filepath.split('.')[-1]
  word_lists = None
  
  if extension == 'docx':
    word_lists = homeFunction.get_word(filepath)
  elif extension == 'hwp':
    pass
  elif extension == 'pdf':
    word_lists = homeFunction.get_pdf(filepath)
  elif extension == 'txt':
   word_lists =  homeFunction.get_txt(filepath)
  else:
    print("Unknown extension")
    return;
  
  text_place.config(state='normal')
  
  # 텍스트 있을 수도 있으니까 삭제하고 집어넣기
  text_place.delete("0.0", END)	
  for c in word_lists:
    text_place.insert(END, c[0])
  
  text_place.config(state='disabled')

  
def del_file(text_place):
  text_place.delete("0.0", END)	
