processing = False

def upload(sftp, path, directory=False):
    global processing
    if processing:
      print("We are busy... retry")
      return
    processing = True
    print("Uploading... to -> " + sftp.pwd)
    if directory:
        sftp.put_r(path, sftp.pwd)
    else:
        sftp.put(path)
    print("Done!")
    processing = False

