from tkinter import *
import UserClass



user=None

window=Tk()
window.title("로그인")
window.config(padx=20, pady=20)

window.resizable(False, False)

canvas = Canvas(window, width=200, height=200, background="white")

image = PhotoImage(file='./images/logo.png')
canvas.create_image(100,100,image=image)
canvas.grid(row=0, column=1)

#Label
id_label = Label(text="ID")
id_label.grid(row=1, column=0)
id_label.config(padx=2, pady=2)

password_label = Label(text="Password")
password_label.grid(row=2, column=0)
password_label.config(padx=2, pady=2)

#Entry
id_entry = Entry(width=35)
id_entry.grid(row=1, column=1)

password_entry = Entry(width=35)
password_entry.grid(row=2, column=1)

#Button
login_button = Button(text="로그인", width=10)
login_button.grid(row=1, column=2, padx=5)


create_id_button = Button(text="회원가입", width=10)
create_id_button.grid(row=1, column=3, padx=5)



window.mainloop()
