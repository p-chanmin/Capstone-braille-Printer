import docx2txt

from PyPDF2 import PdfReader

def get_word(filepath):
  
  text = docx2txt.process(filepath)

  lst_tmp = [(c, ord(c)) for c in text]

  #워드파일에 엔터 누르고 다음줄에 쓰면 \n이 2개 연속으로 됨(디버그 해보니까 이렇게 나옴)
  # 그래서 1개씩 뺴주야됨

  #2개 연속으로
  words_list=[]
  tmp=None
  for tuple in lst_tmp:
    if tuple[0] == '\n':
      if tmp ==True:
        tmp=False
        continue
      else:
        tmp=True
    words_list.append(tuple)

  return words_list  



def get_pdf(filepath):
  pdf = PdfReader(open(filepath, 'rb'))

  words_list = [(c, ord(c))    for i in range(len(pdf.pages))  for c in pdf.pages[i].extract_text()]
  return words_list



# 한글파일은 모르겠음
def get_hwP(filepath):
  pass




def get_txt(filepath):
  words_list = None
  with open(filepath, encoding='UTF-8') as f:
    words_list = [(c, ord(c)) for c in f.read()]
    
  print(words_list)
  return words_list

def get_string(string):
  words_list = [(c, ord(c))    for c in string]
  return words_list

def switchIdx2TkIdx(string, original_idx_lst):
  # 문자열, 일반적인 인덱스를 담고 있는 리스트
  idx_lst = original_idx_lst
  idx = 0

  tkinter_idx_lst = []
  tkinter_idx = 0

  text_string = string
  total_length = 0
  row = 1

  for string in text_string.split('\n'):
    length = len(string) + 1
    while (idx < len(idx_lst) and total_length + length > idx_lst[idx]):
      col = idx_lst[idx] - total_length
      tk_idx = f"{row}.{col}"
      tkinter_idx_lst.append(tk_idx)
      idx += 1

    row += 1
    total_length += length

  return tkinter_idx_lst