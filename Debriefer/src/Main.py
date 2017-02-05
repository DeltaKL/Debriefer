import os
import time
import operator

import Scan_Storage
import OMXGUI
import GUI_Test

if os.name is not 'nt':     #If OS is not windows (implying  that we're running on RasPi)
    import sh

    while True:                             #check if a list excists in /media/pi (USB storage directories)
        lstdisk=format(sh.ls("/media/pi"))
        if (lstdisk):
            print("USB  mounted")
            break
        else:
            print("USB NOT mounted")
            time.sleep(2)


#Path and filetype to scan, if statement for testing purposes on laptop (windows) or raspberry (else)
if os.name == 'nt':
    path = r'C:\Users\saxion\Desktop\24 sept Ponne Eef'     #test folder on desktop
    #path = r'C:\Users\saxion\Desktop\test'                 #test folder 2 on desktop

else:
    path = r'/media'

filetype = r'\*.MP4'

#Calling function to scan path for files of (filetype) & printing
[file_list, latest_file] = Scan_Storage.latest_file_by_type(path,filetype)


if not latest_file:                             #if no values are returned, there are no MP4 files in the path
    print("There are no MP4 files in ", path)
else:
    sorted_file_list = sorted(file_list.items(), key = lambda t: t[0])
   # OMXGUI.GUI_OMXPlayer(latest_file,sorted_file_list)

    #FOR TESTING
    GUI_Test.GUI_OMXPlayer(latest_file, sorted_file_list)

