import asyncio
import threading
import tkinter as tk
from tkinter import messagebox

from src.gui.BluetoothSettingUI import Bluetooth, ConnectBluetooth

class InitTest(threading.Thread):
    def __init__(self, ui):
        super().__init__()
        self.bluetooth = Bluetooth()
        self.connect = ConnectBluetooth(None, None, ui)

    async def init_test(self):
        print("Init_test...")

        if(self.bluetooth.client is not None and self.bluetooth.client.is_connected):
            # 테스트 코드 전송
            print(f"Send Data : I|{self.connect.ZeroPoint}")
            send = (f"I|{self.connect.ZeroPoint}").encode()
            await self.bluetooth.client.write_gatt_char(self.bluetooth.write_uuid, bytes(send))
        else:
            messagebox.showinfo("연결 프린터 없음", "연결된 프린터가 없습니다.")

    def run(self):
        loop = asyncio.new_event_loop()  # 이벤트 루프를 얻음
        loop.run_until_complete(self.init_test())
        loop.close()

class SetInit(threading.Thread):
    def __init__(self, point, ui):
        super().__init__()
        self.bluetooth = Bluetooth()
        self.connect = ConnectBluetooth(None, None, ui)
        self.point = point

    async def init_set(self):
        print("Init_test...")

        if(self.bluetooth.client is not None and self.bluetooth.client.is_connected):
            # 테스트 코드 전송
            print(f"Send Data : I|{self.point}")
            send = (f"I|{self.point}").encode()
            await self.bluetooth.client.write_gatt_char(self.bluetooth.write_uuid, bytes(send))
        else:
            messagebox.showinfo("연결 프린터 없음", "연결된 프린터가 없습니다.")

    def run(self):
        loop = asyncio.new_event_loop()  # 이벤트 루프를 얻음
        loop.run_until_complete(self.init_set())
        loop.close()

class PrintInitialClass:

    def __init__(self):
        self.bluetooth = Bluetooth()
        self.connect = ConnectBluetooth(None, None, self)
        self.__window = self.__createUI()

    def init_test_callback(self):
        thread = InitTest()
        thread.start()

    def __createUI(self):
        # tkinter 창 생성
        root = tk.Tk()
        root.title("프린터 설정값 변경")
        root.geometry("470x160")

        # 왼쪽 프레임 생성
        left_frame = tk.Frame(root, padx=10, pady=10)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH)

        # 현재 연결된 프린터 표시 레이블 생성
        self.connect_text = tk.StringVar(master=root)
        self.connect_text.set("연결된 프린터 없음")
        if(self.bluetooth.client is not None and self.bluetooth.client.is_connected):
            self.connect_text.set(f"연결된 프린터: {self.bluetooth.name}")
        connection_label = tk.Label(left_frame, textvariable=self.connect_text)
        connection_label.pack()

        # 현재 프린터 설정값을 표시할 레이블 생성
        self.current_settings_text = tk.StringVar(master=root)
        self.current_settings_text.set(f"현재 프린터 설정값: {self.connect.ZeroPoint}")
        current_settings_display = tk.Label(left_frame, textvariable=self.current_settings_text)
        current_settings_display.pack(pady=2)

        def init_test_callback():
            if(self.bluetooth.client is not None and self.bluetooth.client.is_connected):
                self.test_button.config(state=tk.DISABLED)
                self.update_button.config(state=tk.DISABLED)
                thread = InitTest(self)
                thread.start()
            else:
                messagebox.showinfo("연결 프린터 없음", "연결된 프린터가 없습니다.")

        # 설정값 테스트 버튼 생성
        self.test_button = tk.Button(left_frame, text="현재 설정값 테스트", command=init_test_callback)
        self.test_button.pack(pady=2)

        # 새로운 프린터 설정값 입력 엔트리 생성
        self.new_settings_entry = tk.Entry(left_frame, width=10)
        self.new_settings_entry.pack(pady=2)

        def init_set_callback():
            p = self.new_settings_entry.get()

            if(p == ""):
                messagebox.showinfo("Error", "설정값을 입력하세요.")
            elif (p.isnumeric()):
                if (self.bluetooth.client is not None and self.bluetooth.client.is_connected):
                    self.test_button.config(state=tk.DISABLED)
                    self.update_button.config(state=tk.DISABLED)
                    thread = SetInit(p, self)
                    thread.start()
                else:
                    messagebox.showinfo("연결 프린터 없음", "연결된 프린터가 없습니다.")
            else:
                messagebox.showinfo("Error", "정수를 입력하세요.")

        # 설정값 변경 버튼 생성
        self.update_button = tk.Button(left_frame, text="설정값 변경", command=init_set_callback)
        self.update_button.pack(pady=2)

        # 오른쪽 프레임 생성
        right_frame = tk.Frame(root, padx=10, pady=2)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH)

        # 설명 텍스트 생성
        description_text = """
        1. 점자 프린터를 연결해주세요.
           (설정 -> 블루투스 프린터 설정 -> 프린터 연결)          
           
        2. 테스트 버튼을 통해서 점자 프린터의 점필이
           첫번째 위치에 맞는지 확인하세요.
        
        3. 설정값을 변경하면서 점필이 첫번째 위치에
           맞게 설정하세요.
        """

        # 설명 텍스트 라벨 생성
        description_label = tk.Label(right_frame, text=description_text, justify=tk.LEFT)
        description_label.pack()

        # tkinter 창 실행
        return root


    def start(self):
        self.__window.mainloop()

    def __end(self):
        self.connect.print_init_ui = None
        self.__window.destroy()


# PrintInitialClass().start()