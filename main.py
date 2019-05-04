import yaml
import pysftp

# infos needed for connection
infos = yaml.load(open("auth.yml"))

# vars for auth

ftp_host = infos['host']
ftp_user = infos['username']
ftp_password = infos['password']

upload_path = infos['upload-path']
current_path = None

# connecting to ftp...

sftp = pysftp.Connection(host=ftp_host,username=ftp_user,password=ftp_password)

while(True):
    input_text = input()
    input_split = input_text.split(" ") 
    if input_split[0] == "upload":
        with sftp.cd(upload_path):
          
         file_directory = None
         
         if current_path is None:
             file_directoty = input_split[1]
         else:
             file_directory = current_path + input_split[1]

         print("current directory: " + sftp.pwd)
         print("uploading " + input_split[1]  + " to " + upload_path)
         sftp.put(file_directory)
         print("Done!")
         continue
    if input_split[0] == "set.current_path":
        current_path = input_split[1]
        print("the current path is now " + current_path) 
        continue
    if input_text == "exit":
        break
    else:
      print("Syntax Error")

