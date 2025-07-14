import requests, time, os
import tkinter as tk
from tkinter import filedialog, ttk

current_scan = {"file_path": None, "scan_id": None}

def get_api_key():
    global api_key
    api_key = name_entry.get().strip()
    if not api_key:
        output("Error: API key is required.\n")
        return False
    return True

def select_file():
    if get_api_key():
        file_path = filedialog.askopenfilename()
        if file_path:
            scan_file(file_path)

def select_folder():
    if get_api_key():
        folder_path = filedialog.askdirectory()
        if folder_path:
            scan_folder(folder_path)

def output(text):
    output_box.config(state="normal")
    output_box.insert(tk.END, text)
    output_box.see(tk.END)
    output_box.config(state="disabled")

root = tk.Tk()
root.geometry("500x450")
root.configure(bg="#88adb0")
title_label = tk.Label(root,text="Virus Scanner",font=("Arial", 25, "bold"),bg="#88adb0",fg="white")
title_label.pack(pady=(20, 10))

input_frame = tk.Frame(root, bg="#f0f0f0")
input_frame.pack(pady=5)

input_label = tk.Label(input_frame, text="API Key:", bg="#7a9fa1",fg="white",font=("Arial", 12, "bold"))
input_label.pack(side="left", padx=(0, 10))

name_entry = tk.Entry(input_frame, width=40)
name_entry.pack(side="left")

style = ttk.Style()
style.configure("TButton", padding=10,bg="#7a9fa1")

file_button = tk.Button(root, text="Scan File", command=select_file, bg="#7a9fa1", fg="white",font=("Arial", 12, "bold"))
file_button.pack(pady=5, ipadx=10)

folder_button = tk.Button(root, text="Scan Folder", command=select_folder, bg="#7a9fa1", fg="white",font=("Arial", 12, "bold"))
folder_button.pack(pady=5, ipadx=10)

output_box = tk.Text(root, height=10, width=60, state="normal", wrap="word", bg="#7a9fa1",font=("Arial", 12, "bold"))
output_box.pack(pady=10)

api_key = ""
scan_url = "https://www.virustotal.com/vtapi/v2/file/scan"
report_url = "https://www.virustotal.com/vtapi/v2/file/report"
file_queue = -2

def scan_folder(folder_path):
    for file in os.listdir(folder_path):
        filename = os.fsdecode(file)
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            scan_file(file_path)
        else:
            scan_folder(file_path)

def scan_file(file_path):
    output(f"Scanning file: {file_path}\n")
    current_scan["file_path"] = file_path
    current_scan["scan_id"] = upload_file(file_path)
    poll_report()

def poll_report():
    file_path = current_scan["file_path"]
    scan_id = current_scan["scan_id"]
    report = get_report(scan_id)

    if "response_code" in report and report["response_code"] == file_queue:
        output("Waiting for report...\n")
        root.after(3000, poll_report)
    elif "positives" in report:
        result = f"File scan Results for '{file_path}' is: {report['positives']}\n"
        output(result)

def get_report(scan_id):
    params = {'apikey': api_key, 'resource': scan_id}
    response = requests.get(report_url, params=params)
    if not response:
        raise Exception("Unexpected error in response")
    if response.status_code == 204:
        return {"response_code": file_queue}
    else:
        return response.json()

def upload_file(file_path):
    with open(file_path, "rb") as f:
        files = { "file": (file_path, f) }
        response = requests.post(scan_url, files=files, params={'apikey': api_key})
        return response.json()["scan_id"]
    
if __name__ == "__main__":
    root.mainloop()
