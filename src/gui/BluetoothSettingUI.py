import tkinter as tk
import asyncio
from bleak import BleakScanner


class BluetoothSettingUI:
    def __init__(self, hoemClassInstance):
        self.devices = []
        self.__window = self.__createUI(hoemClassInstance)

    def __createUI(self, hoemClassInstance):
        window = tk.Tk()
        window.geometry("400x300")
        window.title("Bluetooth Settings")

        # create a label for the Bluetooth device selection
        device_label = tk.Label(window, text="Select Bluetooth Device:")
        device_label.pack()

        def connect_device():
            selected_device = device_listbox.get(device_listbox.curselection())
            print(f"Connecting to device: {selected_device}")
            # Add code to connect to selected device here

        def on_select(event):
            selected_device = device_listbox.get(device_listbox.curselection())
            print(f"Selected device: {selected_device}")

        # create a listbox for the Bluetooth devices
        # devices = ["Device 1", "Device 2", "Device 3"]
        device_listbox = tk.Listbox(window)
        for device in self.devices:
            device_listbox.insert(tk.END, device)
        device_listbox.pack()
        device_listbox.bind('<<ListboxSelect>>', on_select)

        # create a frame to hold the search and connect buttons
        button_frame = tk.Frame(window)
        button_frame.pack()

        async def search_devices():
            print("검색 시작")
            # 검색 시작 (검색이 종료될때까지 대기)
            # 기본 검색 시간은 5초
            devices = await BleakScanner.discover()
            # 검색된 장치들 리스트 출력
            device_listbox.delete(0, tk.END)
            for device in devices:
                print(device)
                # device_listbox.insert(tk.END, device)

        async def search_button_callback():
            loop = asyncio.get_event_loop()
            loop.call_soon_threadsafe(asyncio.create_task, search_devices())

        # create a button to search to the Bluetooth device
        search_button = tk.Button(button_frame, text="Search", command=search_button_callback)
        search_button.pack(side=tk.LEFT, padx=10)

        # create a button to connect to the selected Bluetooth device
        connect_button = tk.Button(button_frame, text="Connect", command=connect_device)
        connect_button.pack(side=tk.LEFT, padx=10)

        # create a label for the Bluetooth status
        status_label = tk.Label(window, text="Bluetooth Status: Disconnected")
        status_label.pack()

        # run the main loop
        return window

    def start(self):
        self.__window.mainloop()

    def __end(self):
        self.__window.destroy()



# BluetoothSettingUI().start()