import tkinter as tk
import json
from tkinter import filedialog

class ECGRecordGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("ECG Record")

        # Create input fields
        tk.Label(self.master, text="time:").grid(row=0, column=0)
        self.time_entry = tk.Entry(self.master)
        self.time_entry.grid(row=0, column=1)

        tk.Label(self.master, text="CVDtype:").grid(row=1, column=0)
        self.cvd_type_entry = tk.Entry(self.master)
        self.cvd_type_entry.grid(row=1, column=1)

        tk.Label(self.master, text="ECGsignal").grid(row=2, column=0)
        self.ecg_signal_data_text = tk.Text(self.master, height=10, width=50)
        self.ecg_signal_data_text.grid(row=2, column=1)

        # Create buttons
        tk.Button(self.master, text="Add Record", command=self.add_record).grid(row=3, column=0)
        tk.Button(self.master, text="Download JSON", command=self.download_json).grid(row=3, column=1)

        # Create list box for records
        tk.Label(self.master, text="ECG Records:").grid(row=4, column=0)
        self.record_list = tk.Listbox(self.master, height=10, width=50)
        self.record_list.grid(row=5, column=0, columnspan=2)

    def add_record(self):
        # Get input field values
        time = self.time_entry.get()
        cvd_type = self.cvd_type_entry.get()
        ecg_signal_data = self.ecg_signal_data_text.get("1.0", "end-1c")

        # Create record dictionary
        record = {"time": time, "CVDtype": cvd_type, "ECGsignal": ecg_signal_data}

        # Add record to list box
        self.record_list.insert(tk.END, json.dumps(record))

        # Clear input fields
        self.time_entry.delete(0, tk.END)
        self.cvd_type_entry.delete(0, tk.END)
        self.ecg_signal_data_text.delete("1.0", tk.END)

    def download_json(self):
        # Get data from list box
        records = [json.loads(item) for item in self.record_list.get(0, tk.END)]

        # Prompt user to select a file name and location
        file_name = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON File", "*.json")])

        # Save data to file
        with open(file_name, "w") as f:
            json.dump(records, f, indent=4)

if __name__ == "__main__":
    root = tk.Tk()
    app = ECGRecordGUI(root)
    root.mainloop()
