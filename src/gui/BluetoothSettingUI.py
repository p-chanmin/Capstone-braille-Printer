import tkinter as tk
import asyncio
import threading
from bleak import BleakScanner
from bleak import BleakClient
import time


class SearchBluetooth(threading.Thread):
    def __init__(self, search_button, device_listbox):
        super().__init__()
        self.search_button = search_button
        self.device_listbox = device_listbox
        self.devices = {}

    async def search_devices(self):
        print("Searching for devices...")
        devices = await BleakScanner.discover()
        print("Devices found complete")
        self.devices = {}
        self.device_listbox.delete(0, tk.END)
        for device in devices:
            address = str(device)[:17]
            name = str(device)[19:]
            self.devices[name] = address
            self.device_listbox.insert(tk.END, name)

    def run(self):
        loop = asyncio.new_event_loop()  # 이벤트 루프를 얻음
        loop.run_until_complete(self.search_devices())
        self.search_button.config(state=tk.NORMAL)
        loop.close()

class BluetoothSettingUI:
    __instance = None  # Singleton 인스턴스를 저장할 클래스 변수

    def __new__(cls, homeclassInstance):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.devices = {}
            cls.__instance.client = None
        cls.__instance.__window = cls.__instance.__createUI(homeclassInstance)
        return cls.__instance



    def __createUI(self, homeclassInstance):
        window = tk.Tk()
        window.geometry("400x300")
        window.title("Bluetooth Settings")

        # create a label for the Bluetooth device selection
        device_label = tk.Label(window, text="Select Bluetooth Device:")
        device_label.pack()

        async def connect_device():
            selected_device = device_listbox.get(device_listbox.curselection())
            if selected_device in self.devices:
                print(f"Connecting to {selected_device} - {self.devices[selected_device]}")
                address = self.devices[selected_device]
                try:
                    self.client = BleakClient(address)
                    await self.client.connect()
                    print(f"Connected to {selected_device}")
                    # 연결 완료 시
                    homeclassInstance.printer_text.set(f"print connect : {selected_device}")
                except Exception as e:
                    print(f"Failed to connect to {selected_device}: {e}")
            else:
                print(f"No device selected")

        def on_select(event):
            selected_device = device_listbox.get(device_listbox.curselection())
            print(f"Selected device: {selected_device}")

        # create a listbox for the Bluetooth devices
        device_listbox = tk.Listbox(window)
        device_listbox.pack()
        device_listbox.bind('<<ListboxSelect>>', on_select)

        # create a frame to hold the search and connect buttons
        button_frame = tk.Frame(window)
        button_frame.pack()

        async def search_devices():
            print("Searching for devices...")
            devices = await BleakScanner.discover()
            print("Devices found complete")
            self.devices = {}
            device_listbox.delete(0, tk.END)
            for device in devices:
                address = str(device)[:17]
                name = str(device)[19:]
                self.devices[name] = address
                device_listbox.insert(tk.END, name)

        async def search_button_callback():
            search_button.config(state=tk.DISABLED)
            # await search_devices()
            thread = SearchBluetooth(search_button, device_listbox)
            thread.start()

        # create a button to search to the Bluetooth device
        search_button = tk.Button(button_frame, text="Search", command=lambda: asyncio.run(search_button_callback()))
        search_button.pack(side=tk.LEFT, padx=10)

        # create a button to connect to the selected Bluetooth device
        connect_button = tk.Button(button_frame, text="Connect", command=lambda: asyncio.run(connect_device()))
        connect_button.pack(side=tk.LEFT, padx=10)

        self.connect_text = tk.StringVar(master=window)
        if(self.client is None):
            self.connect_text.set("Bluetooth Status: Disconnected")
        else:
            self.connect_text.set("Bluetooth Status: connected")
        # create a label for the Bluetooth status
        status_label = tk.Label(window, textvariable=self.connect_text)
        status_label.pack()

        return window

    def start(self):
        self.__window.mainloop()

    def __end(self):
        self.__window.destroy()
