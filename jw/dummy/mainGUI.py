from tkinter import *
import tkinter.ttk as ttk

import mainFunctions

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

text_place = Text(text_frame, height=20, yscrollcommand=scrollbar.set, state="normal")
text_place.pack(side='left', fill='both', expand='True')
scrollbar.config(command=text_place.yview)

# Mode Frame {작성 모드, 파일 모드}

mode_frame = LabelFrame(root, text="모드 선택")
mode_frame.pack(fill='x', padx=5, pady=5)

#######################################################
def mode_function():
  num = write_var.get()
  if num==1: #작성모드
    text_place.config(state="normal")
    file_selection_button.config(state="disabled")
    file_unselection_button.config(state="disabled")
    
  else: # 피일모드
    text_place.delete("0.0", END)	
    
    file_selection_button.config(state="normal")
    file_unselection_button.config(state="normal")
    
#######################################################

write_var = IntVar()
write_radio_button = Radiobutton(mode_frame, text="작성모드", value=1, variable= write_var, command=mode_function)
file_radio_button = Radiobutton(mode_frame, text="파일모드", value=2, variable= write_var, command=mode_function)

write_radio_button.select()
file_radio_button.pack(side='right')
write_radio_button.pack(side='right')

# File Select Frame

button_Frame = Frame(root)
button_Frame.pack(fill='x', padx=5, pady=5)

file_selection_button = Button(button_Frame, width=13, height=1, text="파일 선택", command=lambda : mainFunctions.add_file(text_place), state="disabled")
file_unselection_button = Button(button_Frame,  width = 13,height = 1, text="파일 해제", command=lambda : mainFunctions.del_file(text_place), state="disabled")

file_unselection_button.pack(side="right", padx=3)
file_selection_button.pack(side='right', padx=3)

# 진행 상황 Progress Bar Frame
frame_progress = LabelFrame(root, text='진행상황')
frame_progress.pack(fill='x', padx=5, pady=5)

p_var = DoubleVar()
progress_bar = ttk.Progressbar(frame_progress, maximum=100, variable=p_var)
progress_bar.pack(fill='x', padx=5, pady=5)

# Print  Frame
prit_Frmae = Frame(root)
prit_Frmae.pack(fill='x', padx=5, pady=5)
print_button = Button(prit_Frmae,  width = 13,height = 1, text="프린트 시작")
exit_button = Button(prit_Frmae,  width = 13,height = 1, text="닫기")

exit_button.pack(side='right', padx=3)
print_button.pack(side='right', padx=3)

root.mainloop() 