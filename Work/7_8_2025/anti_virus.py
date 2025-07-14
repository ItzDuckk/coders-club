import requests
import time
import os


api_key = "884546c4dfb1f950685acb1e41f00401d8b70a739264302d4d43d50b953619b7" 
scan_url = "https://www.virustotal.com/vtapi/v2/file/scan"
report_url = "https://www.virustotal.com/vtapi/v2/file/report"

summary = []
file_queue = -2

def scan_folder(folder_path):
    global summary
    for file in os.listdir(folder_path):
        filename = os.fsdecode(file)
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            scan_file(file_path)
            continue
        else:
            scan_folder(file_path)
            continue


def scan_file(file_path):
    global summary
    print("Scanning file", file_path)
    scan_id = upload_file(file_path)
    while True:
            report = get_report(scan_id)
            if "response_code" in report and report["response_code"] == file_queue:
                print(f"Waiting for report...")
                time.sleep(3)
            elif "positives" in report:
                summary.append("File scan Results for '" + file_path + "' is: " + str(report["positives"]))
                return report["positives"]
    
def get_report(scan_id):
    params = {'apikey': api_key, 'resource': scan_id}
    response = requests.get(report_url, params=params)

    if not response:
        raise Exception("Unexpected error in response")
    
    if response.status_code == 204:
        response = {"response_code":file_queue} 
        return response
    else:
        return response.json()

def upload_file(file_path):
    files = { "file": (file_path, open(file_path, "rb")) }
    response = requests.post(scan_url, files=files, params={'apikey': api_key})
    response = response.json()
    return response["scan_id"]

def main():
   scan_folder(r"C:\Users\guysh\OneDrive\מסמכים\coders-club\Work\7_8_2025\test")

   print()
   for entry in summary:
        print(entry)

if __name__ == "__main__":
    main()