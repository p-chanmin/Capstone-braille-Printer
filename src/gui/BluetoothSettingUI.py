import tkinter as tk
from tkinter import messagebox
import asyncio
import threading
from bleak import BleakScanner
from bleak import BleakClient
import time
import datetime

from src.gui.serverFunction import alter_print_document


class SearchBluetooth(threading.Thread):
    def __init__(self, bluetooth_ui):
        super().__init__()
        self.bluetooth_ui = bluetooth_ui

    async def search_devices(self):
        print("Searching for devices...")
        devices = await BleakScanner.discover()
        print("Devices found complete")
        self.bluetooth_ui.devices = {}
        self.bluetooth_ui.device_listbox.delete(0, tk.END)
        for device in devices:
            address = str(device)[:17]
            name = str(device)[19:]
            self.bluetooth_ui.devices[name] = address
            if(name != "None"):
                self.bluetooth_ui.device_listbox.insert(tk.END, name)

    def run(self):
        loop = asyncio.new_event_loop()  # 이벤트 루프를 얻음
        loop.run_until_complete(self.search_devices())
        self.bluetooth_ui.search_button.config(state=tk.NORMAL)
        loop.close()

class ConnectBluetooth(threading.Thread):
    __instance = None  # Singleton 인스턴스를 저장할 클래스 변수

    def __new__(cls, bluetooth_ui, home_ui, print_init_ui):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            if (bluetooth_ui is not None):
                cls.__instance.bluetooth_ui = bluetooth_ui
            else:
                cls.__instance.bluetooth_ui = None
            if (home_ui is not None):
                cls.__instance.home_ui = home_ui
            else:
                cls.__instance.home_ui = None
            if (home_ui is not None):
                cls.__instance.print_init_ui = print_init_ui
            else:
                cls.__instance.print_init_ui = None
            cls.__instance.isPrinting = False
            cls.__instance.line = 0
            cls.__instance.current_line = 0
            cls.__instance.ZeroPoint = 0
            cls.__instance.start_time = None
            cls.__instance.end_time = None
        return cls.__instance

    def __init__(self, bluetooth_ui, home_ui, print_init_ui):
        super().__init__()
        if (bluetooth_ui is not None):
            self.bluetooth_ui = bluetooth_ui
        if (home_ui is not None):
            self.home_ui = home_ui
        if (print_init_ui is not None):
            self.print_init_ui = print_init_ui
        self.bluetooth = Bluetooth()
        self.isPrinting = False
        self.line = 0
        self.current_line = 0
        self.start_time = None
        self.end_time = None

    async def notify_callback(self, sender, data):
        print(f"Received notification :{data.decode()}")
        if("Send_Data" == data.decode()):
            print("Send_Data notify 수신, 데이터 전송")
            if(self.current_line % 78 == 0):
                if(self.current_line == 0):
                    messagebox.showinfo("인쇄 시작", "인쇄를 시작합니다.\n용지를 추가하고 확인을 누르면 인쇄가 시작됩니다.")
                    self.start_time = time.time()
                else:
                    messagebox.showinfo("용지 교체", "용지 교체를 해주세요.\n용지를 교체하면 확인을 눌러주세요.")
                self.isPrinting = False
            else:
                self.isPrinting = False
        if(len(data.decode()) >= 13 and "Complete_Print" == data.decode()[:14]):
            self.home_ui.print_button.config(state=tk.NORMAL)
            self.line = 0
            self.current_line = 0
            self.home_ui.p_var.set(0)
            self.home_ui.progress_bar.update()

            id = data.decode()[15:]
            
            # 서버 상태 변경
            alter_print_document(self.home_ui.user, id, "인쇄 완료")

            self.end_time = time.time()
            sec = (self.end_time - self.start_time)
            total_time = str(datetime.timedelta(seconds=sec)).split(".")[0]

            print(f"Complete_Print... id: {id}, time: {total_time}")
            messagebox.showinfo("인쇄 완료", f"인쇄가 완료되었습니다.\n인쇄 시간 : {total_time}")
        if("Line" == data.decode()[:4]):
            self.current_line = int(data.decode()[4:])
            self.home_ui.p_var.set(self.current_line/self.line*100)
            self.home_ui.progress_bar.update()
        if("Init" == data.decode()[:4]):
            self.ZeroPoint = int(data.decode()[4:])
            if (self.print_init_ui is not None):
                self.print_init_ui.current_settings_text.set(f"현재 프린터 설정값: {self.ZeroPoint}")
        if("TestEnd" == data.decode()):
            try:
                if(self.print_init_ui is not None):
                    self.print_init_ui.test_button.config(state=tk.NORMAL)
                    self.print_init_ui.update_button.config(state=tk.NORMAL)
            except Exception as e:
                print("err 발생")
                print(e)
                print(f"self.print_init_ui : {self.print_init_ui}")



    async def connect_device(self):
        if(self.bluetooth.client is not None and self.bluetooth.client.is_connected):
            try:
                print(f"Disonnecting to {self.bluetooth.client}")
                await self.bluetooth.client.disconnect()
            except Exception as e:
                print(f"Failed to disconnect to {self.bluetooth.client}: {e}")
        else:
            try:
                selected_device = self.bluetooth_ui.device_listbox.get(self.bluetooth_ui.device_listbox.curselection())
            except:
                print("리스트 선택 x")
                selected_device = ""
                self.bluetooth_ui.connect_button.config(state=tk.NORMAL)
            if selected_device in self.bluetooth_ui.devices:
                print(f"Connecting to {selected_device} - {self.bluetooth_ui.devices[selected_device]}")
                address = self.bluetooth_ui.devices[selected_device]
                try:
                    self.bluetooth.client = BleakClient(address, passkey=self.bluetooth_ui.password_entry.get())
                    await self.bluetooth.client.connect()
                    print(f"Connected to {selected_device}")
                    self.bluetooth.name = selected_device
                    # 연결 완료 시
                    self.bluetooth_ui.homeclassInstance.printer_text.set(f"프린터 : {selected_device}")
                    self.bluetooth_ui.connect_text.set("블루투스 연결 상태: 연결됨")
                    self.bluetooth_ui.printer_text.set(f"프린터 : {selected_device}")
                    self.bluetooth_ui.connect_button_text.set("연결 해제")
                    self.bluetooth_ui.connect_button.config(state=tk.NORMAL)
                    print(self.print_init_ui)
                    if(self.print_init_ui is not None):
                        self.print_init_ui.connect_text.set(f"연결된 프린터: {selected_device}")

                    services = await self.bluetooth.client.get_services()
                    # 서비스내에 있는 캐릭터리스틱 정보 보기
                    for service in services:
                        for characteristic in service.characteristics:
                            if ('write' in characteristic.properties):
                                self.bluetooth.write_uuid = characteristic.uuid
                            elif ('notify' in characteristic.properties):
                                self.bluetooth.notify_uuid = characteristic.uuid

                    print(f"write_uuid : {self.bluetooth.write_uuid}")
                    print(f"notify_uuid : {self.bluetooth.notify_uuid}")

                    # notify 수신
                    await self.bluetooth.client.start_notify(self.bluetooth.notify_uuid, self.notify_callback)

                    # ZeroPoint 정보 요청
                    send = ("Z").encode()
                    await self.bluetooth.client.write_gatt_char(self.bluetooth.write_uuid, bytes(send))

                    while self.bluetooth.client.is_connected:
                        await asyncio.sleep(1)

                    # notify 관찰이 종료되고 Disconnect 상황 표시
                    if not self.bluetooth.client.is_connected:
                        print("connect_device_notify await 종료")
                        print("Disonnecting Complete")
                        self.bluetooth_ui.connect_text.set("블루투스 연결 상태: 연결 없음")
                        self.bluetooth_ui.printer_text.set(f"프린터 : 없음")
                        self.bluetooth_ui.homeclassInstance.printer_text.set(f"프린터 : 없음")
                        self.bluetooth_ui.connect_button_text.set("연결")
                        self.bluetooth.client = None
                        self.bluetooth_ui.connect_button.config(state=tk.NORMAL)
                        self.ZeroPoint = 0
                        if(self.print_init_ui is not None):
                            self.print_init_ui.current_settings_text.set(f"현재 프린터 설정값: {self.ZeroPoint}")

                except Exception as e:
                        print(f"Failed to connect to {selected_device}: {e}")
                        self.bluetooth_ui.connect_button.config(state=tk.NORMAL)
                        messagebox.showwarning("Error", f"{selected_device} : 디바이스 연결에 실패했습니다.\n 재시도 해주세요.")
                        self.bluetooth_ui.connect_text.set("블루투스 연결 상태: 연결 없음")
            else:
                print(f"No device selected")
    def run(self):
        loop = asyncio.new_event_loop()  # 이벤트 루프를 얻음
        loop.run_until_complete(self.connect_device())
class Send_Data(threading.Thread):
    def __init__(self, print_id, data):
        super().__init__()
        self.bluetooth = Bluetooth()
        self.print_id = print_id
        self.data = data

    async def send_data(self):
        try:
            connect = ConnectBluetooth(None, None, None)
            print("데이터 보내는 중...")

            data_list = self.data.split('+')
            connect.line = len(data_list)
            send_data_list = []
            for i in range(0, len(data_list), 3):
                data = data_list[i] + '+' + data_list[i + 1] + '+' + data_list[i + 2]
                send_data_list.append(data)

            send = ("P|" + str(self.print_id) + "|" + str(len("".join(send_data_list)))).encode()
            connect.isPrinting = True
            await self.bluetooth.client.write_gatt_char(self.bluetooth.write_uuid, bytes(send))

            print("noti 대기중...")
            while(connect.isPrinting):
                pass

            for data in send_data_list:
                encoded_data = data.encode()
                chunks = [encoded_data[i:i + 65] for i in range(0, len(encoded_data), 65)]
                for chunk in chunks:
                    result = await self.bluetooth.client.write_gatt_char(self.bluetooth.write_uuid, bytes(chunk))
                    print(f"{len(chunk)}바이트 데이터 보내기 완료... {result}")
                    time.sleep(0.1)
                print("전체 데이터 전송 완료")
                connect.isPrinting = True
                while (connect.isPrinting):
                    pass

            print("전체 데이터 전송 완료")
        except Exception as e:
            print(f"데이터 전송 중 오류 : {e}")


    def run(self):
        loop = asyncio.new_event_loop()  # 이벤트 루프를 얻음
        loop.run_until_complete(self.send_data())
        loop.close()

class Bluetooth:
    __instance = None  # Singleton 인스턴스를 저장할 클래스 변수
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.client = None
            cls.__instance.write_uuid = ''
            cls.__instance.notify_uuid = ''
            cls.__instance.name = ''
        return cls.__instance


class BluetoothSettingUI:
    __instance = None  # Singleton 인스턴스를 저장할 클래스 변수

    def __new__(cls, homeclassInstance):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.devices = {}
            cls.__instance.homeclassInstance = homeclassInstance
            cls.__instance.bluetooth = Bluetooth()
        cls.__instance.__window = cls.__instance.__createUI(homeclassInstance)
        return cls.__instance

    def __createUI(self, homeclassInstance):
        window = tk.Tk()
        window.geometry("400x300")
        window.title("블루투스 프린터 설정")
        window.resizable(False, False)

        device_label = tk.Label(window, text="검색된 블루투스 기기:")
        device_label.pack()

        def on_select(event):
            selected_device = self.device_listbox.get(self.device_listbox.curselection())
            print(f"Selected device: {selected_device}")

        self.device_listbox = tk.Listbox(window)
        self.device_listbox.pack()
        self.device_listbox.bind('<<ListboxSelect>>', on_select)

        password_frame = tk.Frame(window)
        password_frame.pack(padx=10, pady=10)

        password_label = tk.Label(password_frame, text="비밀번호:")
        password_label.pack(side=tk.LEFT)

        self.password_entry = tk.Entry(password_frame, show="*", width=10)
        self.password_entry.pack(side=tk.LEFT, padx=5)

        button_frame = tk.Frame(window)
        button_frame.pack()

        def search_button_callback():
            self.search_button.config(state=tk.DISABLED)
            thread = SearchBluetooth(self)
            thread.start()

        def connect_button_callback():
            self.connect_button.config(state=tk.DISABLED)
            thread = ConnectBluetooth(self, None, None)
            thread.start()

        self.search_button = tk.Button(button_frame, text="검색", command=search_button_callback)
        self.search_button.pack(side=tk.LEFT, padx=10)

        self.connect_button_text = tk.StringVar(master=window)
        if (self.bluetooth.client is not None and self.bluetooth.client.is_connected):
            self.connect_button_text.set("연결 해제")
        else:
            self.connect_button_text.set("연결")

        self.connect_button = tk.Button(button_frame, textvariable=self.connect_button_text, command=connect_button_callback)
        self.connect_button.pack(side=tk.LEFT, padx=10)

        self.connect_text = tk.StringVar(master=window)
        if(self.bluetooth.client is not None and self.bluetooth.client.is_connected):
            self.connect_text.set("블루투스 연결 상태: 연결됨")

        else:
            self.connect_text.set("블루투스 연결 상태: 연결 없음")
            self.homeclassInstance.printer_text.set(f"프린터 : 없음")

        status_label = tk.Label(window, textvariable=self.connect_text)
        status_label.pack()

        self.printer_text = tk.StringVar(master=window)
        self.printer_text.set(homeclassInstance.printer_text.get())

        status_label = tk.Label(window, textvariable=self.printer_text)
        status_label.pack()

        return window

    def start(self):
        self.__window.mainloop()

    def __end(self):
        self.__window.destroy()
