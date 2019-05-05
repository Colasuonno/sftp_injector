import yaml
import pysftp
import ftp_util
import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from watchdog.events import FileModifiedEvent
from watchdog.events import FileCreatedEvent

# infos needed for connection
infos = yaml.load(open("auth.yml"))
observed_file = yaml.load(open("observed.yml"))

# vars for auth

ftp_host = infos['host']
ftp_user = infos['username']
ftp_password = infos['password']

observed_path = observed_file['path']

upload_path = infos['upload-path']
current_path = None
file_directory = None

# connecting to ftp...

sftp = pysftp.Connection(host=ftp_host,username=ftp_user,password=ftp_password)
print("Connected as sftp:" + ftp_user + "@" + ftp_host) 
print("Observing " + observed_path)

# checking path...

class EventHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        if event.__class__ is FileModifiedEvent or FileCreatedEvent:
            with sftp.cd(upload_path):
                if ".swp" not in event.src_path and os.path.isfile(event.src_path):
                    print("file: " + event.src_path)
                    ftp_util.upload(sftp, event.src_path)
                    print("Uploaded changed files from " + observed_path)

if __name__ == "__main__":
    path = observed_path
    event_handler = EventHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

while(True):
    input_text = input()
    input_split = input_text.split(" ") 
    if input_split[0] == "upload":
        with sftp.cd(upload_path):
         
         if current_path is None: 
             file_directory = input_split[1]
         else:
             file_directory = current_path + input_split[1]

         print("current directory: " + sftp.pwd)
         print("uploading " + file_directory  + " to " + upload_path)
         ftp_util.upload(sftp,file_directory, len(input_split) >= 3 and input_split[2] == "-d")
         continue
    if input_split[0] == "set.current_path":
        current_path = input_split[1]
        print("the current path is now " + current_path) 
        continue
    if input_text == "exit":
        break
    else:
      print("Syntax Error")

