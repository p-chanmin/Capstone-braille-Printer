import tkinter as tk


class BluetoothSettingUI:
    def __init__(self, hoemClassInstance):
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
        devices = ["Device 1", "Device 2", "Device 3"]
        device_listbox = tk.Listbox(window)
        for device in devices:
            device_listbox.insert(tk.END, device)
        device_listbox.pack()
        device_listbox.bind('<<ListboxSelect>>', on_select)

        # create a frame to hold the search and connect buttons
        button_frame = tk.Frame(window)
        button_frame.pack()

        # create a button to search to the Bluetooth device
        search_button = tk.Button(button_frame, text="Search")
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