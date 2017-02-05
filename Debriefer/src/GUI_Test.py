#Module: GUI_Test.pyimport os

from time import sleep
import os
import re


def GUI_OMXPlayer(playFile, playList):

    print("Playlist is",playList)
    for i in playList:
        print(i)
    print(playFile)
    print(playList[0][0])
    print(playList[0][1])


    def quitOMX(event):
        print("Escape HIT")
        try:
            player.quit()
        except:
            print("OMXPlayer not running")

    if os.name is not 'nt':             #Tkinter module has different name on RassPi
        import Tkinter as Tk
        from omxplayer import OMXPlayer
    else:
        import tkinter as Tk

    class OMX_user_interface(Tk.Tk):

        def __init__(self, parent):
            Tk.Tk.__init__(self, parent)
            self.parent = parent
            self.createbuttons()
            self.vidWin = vidWindow(self)
            self.playFile = playFile
            self.playList = playList

        def createbuttons(self):           # GUI Buttons created: Prev, rew, stop, play/pause, forw, next.
            self.grid()

            resetOMX = Tk.Button(self, text="RESET OMXPLAYER", command=self.resetOMXClicked)
            resetOMX.grid(column = 0, row = 1)

            prevButton = Tk.Button(self,text="< File",command = self.prevButtonClicked)
            prevButton.grid(column = 1, row = 1)

            rewButton = Tk.Button(self,text="Rewind")

            rewButton.bind("<ButtonPress-1>",self.rewButtonHeld)
            rewButton.grid(column=2, row=1)

            stopButton = Tk.Button(self,text = "Stop", command = self.stopButtonClicked)
            stopButton.grid(column=3, row=1)

            playbutton = Tk.Button(self,text="Pause",command = self.playButtonClicked)
            playbutton.grid(column = 4, row=1)

            forwButton = Tk.Button(self,text = "Forward", command = self.forwButtonHeld)
            forwButton.grid(column=5, row=1)

            nextButton = Tk.Button(self,text = "> File", command = self.nextButtonClicked)
            nextButton.grid(column=6, row=1)

            self.grid_columnconfigure(0,weight=1)
            self.resizable(False,False)      #resizeable only in the x-

        def resetOMXClicked(self):
            os.system("kill $(pgrep omxplayer)")

        def prevButtonClicked(self):
            print("prevButtonClicked")

            for i,k in enumerate(playList):
                if self.playFile in k:
                    self.playFile = self.playList[i-1][0]
           # self.openOMXPlayer(playFile)
            print(self.playFile)

        def rewButtonHeld(self,event):
            print("rewButtonHeld")
            try:
                sliderPos=OMXPlayer.position(player)
                OMXPlayer.set_position(player,sliderPos-5)
            except:
                print("Player not playing")

        def stopButtonClicked(self):
            print("stopButtonClicked")
            try:
                OMXPlayer.stop(player)
            except:
                pass

        def playButtonClicked(self):
            print("playButtonClicked")
            try:
                OMXPlayer.play_pause(player)
            except:
                print("OMXPlayer not running")
            sleep(0.2)

        def forwButtonHeld(self):
            print("forButtonHeld")
            try:
                sliderPos=OMXPlayer.position(player)
                OMXPlayer.set_position(player,sliderPos+5)
            except:
                print("Player not playing")

        def nextButtonClicked(self):
            print("nextButtonClicked")
            self.revplayList = list(reversed(self.playList))
            for i, k in enumerate(self.revplayList):
                if self.playFile in k:
                    self.playFile = self.revplayList[i-1][0]

          #  self.player = OMXPlayer(self.playFile)

            print(self.playFile)

    class vidWindow(Tk.Toplevel):
        def __init__(self,*args,**kwargs):
            Tk.Toplevel.__init__(self,*args,**kwargs)
            self.frame = Tk.Label(self, text="Click on the grip to move")
            self.frame.pack(side="bottom", fill="both", expand=True)

            self.frame.bind("<ButtonPress-1>", self.StartMove)
            self.frame.bind("<Double-Button-1>", self.OnDoubleClick)
          #  self.frame.bind("<ButtonRelease-1>", self.StopMove)
            self.frame.bind("<B1-Motion>", self.OnMotion)

            self.bind("<Configure>", self.Configure)
            self.bind("<Escape>", self.OnEscape)

            self.attributes("-topmost", 1)

            #Default Geometry (video resolution? Or at leats its ratio!)
            self.geometry("1200x700+20+20")

            #Video window & screen properties
            self.widget_geometry = self.geometry()
            self.vid_window_size = re.findall(r"\d+", self.widget_geometry)
            self.vid_window_geometry = list(map(int, self.vid_window_size))
            self.vid_window_size = self.vid_window_geometry[0:2]
            self.screensize = [(self.winfo_screenwidth()), (self.winfo_screenheight())]

            self.openOMXPlayer(playFile)  #opening OMXPlayer

        def openOMXPlayer(self,playFile):
            [width, height] = self.winfo_screenwidth(), self.winfo_screenheight()
            if os.name is not 'nt':
                #self.player = OMXPlayer("/home/pi/Desktop/vid2.MP4")
                self.player = OMXPlayer(self.playFile)
                OMXPlayer.set_video_pos(player, 0, 100, width, height - 100)
                OMXPlayer.set_aspect_mode(player, "letterbox")

        def frameParameters(self):

            self.vid_window_size = re.findall(r"\d+", self.geometry())
            self.vid_window_geomtery = list(map(int,self.vid_window_size))
            self.width = self.winfo_width()
            self.height = self.winfo_height()
            self.menuBarHeight = self.winfo_rooty()

        def StartMove(self, event):
            self.x = event.x
            self.y = event.y

        def StopMove(self):
            self.x = None
            self.y = None
            self.widget_geometry = self.geometry()
            self.vid_window_size = re.findall(r"\d+", self.widget_geometry)
            self.vid_window_geometry = list(map(int, self.vid_window_size))
            self.vid_window_size = self.vid_window_geometry[0:2]
            self.screensize = [(self.winfo_screenwidth()), (self.winfo_screenheight())]

            if set(self.vid_window_size) != set(self.screensize):
                self.location=self.geometry()

        def OnMotion(self, event):
            if set(self.vid_window_size) != set(self.screensize):
                deltax = event.x - self.x
                deltay = event.y - self.y
                x = self.winfo_x() + deltax
                y = self.winfo_y() + deltay

                self.geometry("+%s+%s" % (x, y))

        def Configure(self, event):
            #print(event)

            self.widget_geometry = self.geometry()
            self.vid_window_size = re.findall(r"\d+", self.widget_geometry)
            self.vid_window_geometry = list(map(int, self.vid_window_size))


            self.menuBarHeight = self.winfo_rooty()

        #  print(self.frameParameters)
            self.OMXformatOrder = [2, 3, 0, 1]
            self.OMXSizeParam = [self.vid_window_geometry[i] for i in self.OMXformatOrder]
            self.OMXSizeParam[2] += self.OMXSizeParam[0]
            self.OMXSizeParam[3] += (self.OMXSizeParam[1]+self.menuBarHeight)
            print(self.OMXSizeParam)
            try:
                OMXPlayer.set_video_pos(player, self.OMXSizeParam)
            except:
                pass


        def OnDoubleClick(self, event):

            self.widget_geometry = self.geometry()
            self.vid_window_size = re.findall(r"\d+", self.widget_geometry)
            self.vid_window_geometry = list(map(int, self.vid_window_size))
            self.vid_window_size = self.vid_window_geometry[0:2]

            if set(self.vid_window_size) == set(self.screensize):         #if in fullscreen
                #self.geometry(self.location)
                self.geometry("400x300+20+20")
                self.attributes('-fullscreen', False)
                self.Configure(event)
            else:                                               #if not in fullscreen
                self.geometry("%sx%s+0+0" % (width, height))
                self.attributes('-fullscreen', True)

        def OnEscape(self,event):
            try:
                player.quit()
            except:
                pass

    try:
        if os.name is not 'nt':
            player= OMXPlayer(playFile)
    except:
        pass

    app = OMX_user_interface(None)
    app.title('OMX_GUI_Test')
    app.attributes("-topmost", True)
    [width, height] = (app.winfo_screenwidth(),app.winfo_screenheight())
    app.mainloop()



