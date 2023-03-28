import tkinter as tk
from tkinter import messagebox
import asyncio
import threading
from bleak import BleakScanner
from bleak import BleakClient
import time

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
            self.bluetooth_ui.device_listbox.insert(tk.END, name)

    def run(self):
        loop = asyncio.new_event_loop()  # 이벤트 루프를 얻음
        loop.run_until_complete(self.search_devices())
        self.bluetooth_ui.search_button.config(state=tk.NORMAL)
        loop.close()

class ConnectBluetooth(threading.Thread):
    __instance = None  # Singleton 인스턴스를 저장할 클래스 변수

    def __new__(cls, bluetooth_ui):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.bluetooth_ui = bluetooth_ui
        return cls.__instance

    def __init__(self, bluetooth_ui):
        super().__init__()
        self.bluetooth_ui = bluetooth_ui
        self.bluetooth = Bluetooth()

    async def notify_callback(self, sender, data):
        print("Received notification : ", data.decode())

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
            if selected_device in self.bluetooth_ui.devices:
                print(f"Connecting to {selected_device} - {self.bluetooth_ui.devices[selected_device]}")
                address = self.bluetooth_ui.devices[selected_device]
                try:
                    self.bluetooth.client = BleakClient(address, passkey="1234")
                    await self.bluetooth.client.connect()
                    print(f"Connected to {selected_device}")
                    # 연결 완료 시
                    self.bluetooth_ui.homeclassInstance.printer_text.set(f"프린터 : {selected_device}")
                    self.bluetooth_ui.connect_text.set("블루투스 연결 상태: Connected")
                    self.bluetooth_ui.printer_text.set(f"프린터 : {selected_device}")
                    self.bluetooth_ui.connect_button_text.set("Disconnect")
                    self.bluetooth_ui.connect_button.config(state=tk.NORMAL)

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
                    while self.bluetooth.client.is_connected:
                        await asyncio.sleep(1)

                    # notify 관찰이 종료되고 Disconnect 상황 표시
                    if not self.bluetooth.client.is_connected:
                        print("connect_device_notify await 종료")
                        print("Disonnecting Complete")
                        self.bluetooth_ui.connect_text.set("블루투스 연결 상태: Disconnected")
                        self.bluetooth_ui.printer_text.set(f"프린터 : 없음")
                        self.bluetooth_ui.homeclassInstance.printer_text.set(f"프린터 : 없음")
                        self.bluetooth_ui.connect_button_text.set("Connect")
                        self.bluetooth.client = None
                        self.bluetooth_ui.connect_button.config(state=tk.NORMAL)

                except Exception as e:
                        print(f"Failed to connect to {selected_device}: {e}")
                        self.bluetooth_ui.connect_button.config(state=tk.NORMAL)
                        messagebox.showwarning("Error", f"{selected_device} : 디바이스 연결에 실패했습니다.\n재시도 해주세요.")
                        self.bluetooth_ui.connect_text.set("블루투스 연결 상태: Disconnected")
            else:
                print(f"No device selected")
    def run(self):
        loop = asyncio.new_event_loop()  # 이벤트 루프를 얻음
        loop.run_until_complete(self.connect_device())
class Send_Data(threading.Thread):
    def __init__(self, data):
        super().__init__()
        self.bluetooth = Bluetooth()
        self.data = data

    async def send_data(self):
        try:
            print("데이터 보내는 중...")
            encoded_data = self.data.encode()
            print(f"{encoded_data} : {len(encoded_data)}")
            chunks = [encoded_data[i:i + 65] for i in range(0, len(encoded_data), 65)]
            for chunk in chunks:
                result = await self.bluetooth.client.write_gatt_char(self.bluetooth.write_uuid, bytes(chunk))
                print(f"{len(chunk)}바이트 데이터 보내기 완료... {result}")
                time.sleep(0.1)
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
        window.title("Bluetooth Settings")

        # create a label for the Bluetooth device selection
        device_label = tk.Label(window, text="Select Bluetooth Device:")
        device_label.pack()

        def on_select(event):
            selected_device = self.device_listbox.get(self.device_listbox.curselection())
            print(f"Selected device: {selected_device}")

        # create a listbox for the Bluetooth devices
        self.device_listbox = tk.Listbox(window)
        self.device_listbox.pack()
        self.device_listbox.bind('<<ListboxSelect>>', on_select)

        # create a frame to hold the search and connect buttons
        button_frame = tk.Frame(window)
        button_frame.pack()

        def search_button_callback():
            self.search_button.config(state=tk.DISABLED)
            thread = SearchBluetooth(self)
            thread.start()

        def connect_button_callback():
            self.connect_button.config(state=tk.DISABLED)
            thread = ConnectBluetooth(self)
            thread.start()

        # create a button to search to the Bluetooth device
        self.search_button = tk.Button(button_frame, text="Search", command=search_button_callback)
        self.search_button.pack(side=tk.LEFT, padx=10)

        self.connect_button_text = tk.StringVar(master=window)
        if (self.bluetooth.client is not None and self.bluetooth.client.is_connected):
            self.connect_button_text.set("Disconnect")
        else:
            self.connect_button_text.set("Connect")
        # create a button to connect to the selected Bluetooth device
        self.connect_button = tk.Button(button_frame, textvariable=self.connect_button_text, command=connect_button_callback)
        self.connect_button.pack(side=tk.LEFT, padx=10)

        self.connect_text = tk.StringVar(master=window)
        if(self.bluetooth.client is not None and self.bluetooth.client.is_connected):
            self.connect_text.set("블루투스 연결 상태: Connected")

        else:
            self.connect_text.set("블루투스 연결 상태: Disconnected")
            self.homeclassInstance.printer_text.set(f"프린터 : 없음")
        # create a label for the Bluetooth status
        status_label = tk.Label(window, textvariable=self.connect_text)
        status_label.pack()

        self.printer_text = tk.StringVar(master=window)
        self.printer_text.set(homeclassInstance.printer_text.get())
        # create a label for the Bluetooth status
        status_label = tk.Label(window, textvariable=self.printer_text)
        status_label.pack()

        return window

    def start(self):
        self.__window.mainloop()

    def __end(self):
        self.__window.destroy()
