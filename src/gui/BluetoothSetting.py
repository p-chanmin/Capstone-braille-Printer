import tkinter as tk


class CreateUser:
    def __init__(self):
        self.__window = self.__createUI()

    def __createUI(self):
        window = tk.Tk()
        window.geometry("400x300")
        window.title("프린터 블루투스 연결")

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

        # create a button to connect to the selected Bluetooth device
        connect_button = tk.Button(window, text="연결", command=connect_device)
        connect_button.pack()

        # create a label for the Bluetooth status
        status_label = tk.Label(window, text="Bluetooth Status: Disconnected")
        status_label.pack()

        # run the main loop
        return window

    def start(self):
        self.__window.mainloop()

    def __end(self):
        self.__window.destroy()
        return

CreateUser().start()