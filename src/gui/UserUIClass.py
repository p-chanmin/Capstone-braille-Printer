from tkinter import *
from src.gui.serverFunction import get_user_info, user_delete
import tkinter.messagebox as msgbox

class UserUI:
    def __init__(self, homeInstance):
        self.homeInstance = homeInstance
        self.user = homeInstance.user

        email = None
        name = None

        result = get_user_info(self.user)
        if result is not None:
            email = result['email']
            name = result['name']

        self.window = Tk()

        self.labelFrame = Frame(self.window)
        self.labelFrame.pack(fill='x', padx=5, pady=5)
        self.email_label = Label(self.labelFrame, text=f"이메일: {email}")
        self.name_label = Label(self.labelFrame, text=f"이름: {name}")
        self.email_label.grid(row=0, column=0, padx=2 ,pady=2)
        self.name_label.grid(row=1, column=0, padx=2, pady=2)

        self.buttonFrame = Frame(self.window)
        self.buttonFrame.pack(fill='x', padx=5, pady=5)
        self.logoutButton = Button(self.buttonFrame, width=10, text='로그아웃', command=self.logoutF)
        self.userDelButton = Button(self.buttonFrame, width=10, text='회원 탈퇴', command=self.delUserF)
        self.cancelButton = Button(self.buttonFrame, width=10, text='닫기', command=self.cancelF)
        self.logoutButton.grid(row=0, column=0, padx=2, pady=2)
        self.userDelButton.grid(row=0, column=1, padx=2, pady=2)
        self.cancelButton.grid(row=0, column=2, padx=2, pady=2)


    def logoutF(self):
        num = msgbox.askyesno(title="로그아웃", message="로그아웃을 하겠습니까?")

        if num == 1:
            msgbox.showinfo(title="로그아웃 성공", message="로그아웃 성공")
            self.end()
            homeInstance = self.homeInstance
            homeInstance.end()

    def delUserF(self):
        homeInstance = self.homeInstance
        num = msgbox.askyesno(title="회원 탈퇴", message="회원탈퇴를 하겠습니까?")
        if user_delete(homeInstance.user):
            msgbox.showinfo(title="탈퇴 성공", message="회원가입 탈퇴에 성공했습니다")
            self.end()
            homeInstance.end()
        else:
            msgbox.showerror(title="탈퇴 실패", message="회원가입 탈퇴에 실패했습니다")
    def cancelF(self):
        self.end()

    def start(self):
        self.window.mainloop()

    def end(self):
        self.window.destroy()

    def quit(self):
        self.window.quit()