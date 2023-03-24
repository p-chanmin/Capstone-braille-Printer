import tkinter as tk
import asyncio
from bleak import BleakScanner


class BluetoothSettingUI:
    def __init__(self, homeclassInstance):
        self.devices = {}
        self.__window = self.__createUI(homeclassInstance)

    def __createUI(self, homeclassInstance):
        window = tk.Tk()
        window.geometry("400x300")
        window.title("Bluetooth Settings")

        # create a label for the Bluetooth device selection
        device_label = tk.Label(window, text="Select Bluetooth Device:")
        device_label.pack()

        def connect_device():
            selected_device = device_listbox.get(device_listbox.curselection())
            if(self.devices[selected_device]):
                print(f"{selected_device} - {self.devices[selected_device]}")

                # 연결 완료 시
                homeclassInstance.printer_text.set(f"print connect : {selected_device}")
            # Add code to connect to selected device here

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
            for device in devices:
                address = str(device)[:17]
                name = str(device)[19:]
                self.devices[name] = address
                device_listbox.insert(tk.END, name)

        async def search_button_callback():
            search_button.config(state=tk.DISABLED)
            await search_devices()
            search_button.config(state=tk.NORMAL)

        # create a button to search to the Bluetooth device
        search_button = tk.Button(button_frame, text="Search", command=lambda: asyncio.run(search_button_callback()))
        search_button.pack(side=tk.LEFT, padx=10)

        # create a button to connect to the selected Bluetooth device
        connect_button = tk.Button(button_frame, text="Connect", command=connect_device)
        connect_button.pack(side=tk.LEFT, padx=10)

        # create a label for the Bluetooth status
        status_label = tk.Label(window, text="Bluetooth Status: Disconnected")
        status_label.pack()

        return window

    def start(self):
        self.__window.mainloop()

    def __end(self):
        self.__window.destroy()



# BluetoothSettingUI().start()