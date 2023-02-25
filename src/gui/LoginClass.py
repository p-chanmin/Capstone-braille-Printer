import tkinter.messagebox as msgbox
from tkinter import *

from src.gui import StateClass, serverFunction
from src.gui.StateClass import State


class Login:
  

  
  def __init__(self):
    self.__window=self.__createUI()

    self.__tmp_email = None
    self.__tmp_password = None

    # 로그인 확인 여부
    self.state = None
    
  def __createUI(self):
    window=Tk()
    window.title("로그인")
    window.config(padx=20, pady=20)

    window.resizable(False, False)

    canvas = Canvas(window, width=200, height=200, background="white")
    image = PhotoImage(file='src/images/logo.png')
    canvas.create_image(100,100,image=image)
    canvas.grid(row=0, column=1)

    #Label
    email_label = Label(text="이메일")
    email_label.grid(row=1, column=0)
    email_label.config(padx=2, pady=2)

    password_label = Label(text="패스워드")
    password_label.grid(row=2, column=0)
    password_label.config(padx=2, pady=2)

    #Entry
    self.__email_entry = Entry(width=35)
    self.__email_entry.grid(row=1, column=1)

    self.__password_entry = Entry(width=35)
    self.__password_entry.grid(row=2, column=1)

    #Button
    login_button = Button(text="로그인", width=10, command = self.__LoginCheck)
    login_button.grid(row=1, column=2, padx=5)


    create_email_button = Button(text="회원가입", width=10, command= self.__CreateAddress)
    create_email_button.grid(row=1, column=3, padx=5)
    
    return window
  
  
  def start(self):
    self.__window.mainloop()

    # 로그인 확인 완료되서 유저 객체 생성
    if self.state == StateClass.State.LOGINOK:
      email = self.__tmp_email
      password = self.__tmp_password
      return State(StateClass.State.LOGINOK, email, password)
    
    elif self.state == StateClass.State.CREATEUSER:
      return State(StateClass.State.CREATEUSER)
    
    else:
      return State(StateClass.State.OTHER)
  def __end(self):
    self.__window.destroy()
  
  ############### event functions #################
  
  def __LoginCheck(self):
    self.__tmp_email = self.__email_entry.get()
    self.__tmp_password = self.__password_entry.get()
    
    # 입력안했으니깐 경고
    if self.__tmp_email =="" or self.__tmp_password =="":
      
      msgbox.showwarning(title="경고", message="아이디 또는 비밀번호를 입력하지 않았습니다.")
      
      self.__tmp_email = None
      self.__tmp_password = None
      return
    
    #로그인 완료되면 다음단계로 ㄱㄱ
    if serverFunction.LoginOk(self.__tmp_email,self.__tmp_password):
      self.ok = True
      self.__end()
      self.state = StateClass.State.LOGINOK
    else: #경고 메세지
      msgbox.showwarning(title="경고", message="아이디 또는 비밀번호가 올바르지 않습니다.")

  def __CreateAddress(self):
     self.state = StateClass.State.CREATEUSER
     self.__end()

