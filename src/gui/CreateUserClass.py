from tkinter import *
import tkinter.messagebox as msgbox

from src.gui import serverFunction


class CreateUser:
  def __init__(self, con):
    self.__window = self.__createUI()
    self.__con = con
    
  def __createUI(self): 
    window=Tk()
    window.title("회원가입")
    window.config(padx=20, pady=20)

    window.resizable(False, False)
    
    #Label
    id_label = Label(master = window, text="아이디")
    id_label.grid(row=0, column=0)
    id_label.config(padx=2, pady=2)

    password_label = Label(master = window, text="비밀번호")
    password_label.grid(row=1, column=0)
    password_label.config(padx=2, pady=2)

    name_label = Label(master = window, text="이름")
    name_label.grid(row=2, column=0)
    name_label.config(padx=2, pady=2)

    #Entry
    self.__id_entry = Entry(master = window, width=35)
    self.__id_entry.grid(row=0, column=1, columnspan=2)

    self.__password_entry = Entry(master = window, width=35)
    self.__password_entry.grid(row=1, column=1, columnspan=2)
    
    self.__name_entry = Entry(master = window, width=35)
    self.__name_entry.grid(row=2, column=1, columnspan=2)
    
    #Button
    login_button = Button(master = window, text="중복확인", width=10, command = self.__idCheck)
    login_button.grid(row=0, column=3, padx=5)


    create_id_button = Button(master = window, text="가입", width=30, command= self.__CreateAddress)
    create_id_button.grid(row=3, column=1, padx=5)
    
    cancel_button = Button(master = window, text="취소", width=10, command= self.__end)
    cancel_button.grid(row=3, column=3, padx=5)
    return window
  
  def start(self):
    self.__window.mainloop()
 

  def __end(self):
    self.__window.destroy()
    return 
  
  ############### event functions #################  
  def __idCheck(self):
    #db에서 아이디 중복검사 통과했나 확인
    if(serverFunction.idCheckOk(self.__id_entry.get(), self.__con)):
      msgbox.showinfo(title="확인완료", message="사용가능한 아이디 입니다")
    else:
      msgbox.showwarning(title="에러", message="중복된 아이디가 있습니다")
      self.__id_entry.delete("0.0", END)
  
  def __CreateAddress(self):
    id = self.__id_entry.get()
    password = self.__password_entry.get()
    name = self.__name_entry.get()
    con = self.__con
    
    if id =="" or password =="" or name =="":
      msgbox.showerror(title="생성 불가", message="모든칸이 입력되지 않았습니다")
      return
    
    if serverFunction.JoinOk(id, password, name, con):
      msgbox.showinfo(title="가입 완료", message="가입이 완료되었습니다")
      self.__end()
      return
      
    else:
      msgbox.showerror(title="생성 불가", message="회원가입이 거부되었습니다\n"+"다시 시도해 주세요")
      
      self.__id_entry.delete("0.0", END)
      self.__password_entry.delete("0.0", END)
      self.__name_entry.delete("0.0", END)
      return
