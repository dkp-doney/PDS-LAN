import tkinter as tk
from tkinter import ttk
import tkinter.filedialog as fd
import urllib.request
import urllib.response
import os
from tempfile import NamedTemporaryFile




def directoryBox():
    global Dpath
    text=fd.askdirectory(title='Download path')
    text=text+"/"
    print(text)
    Dpath=str(text)
def copyfileobj(fsrc, fdst, length,filesize):
    """copy data from file-like object fsrc to file-like object fdst"""
    progress=progressbar(filesize)
    global file
    while 1:
        try:
            buf = fsrc.read(length)
            if not buf:
                break
            fdst.write(buf)
            file=fdst.tell()
            progress["value"] = file
            progress.update()
            print(file)
            #progress.destroy()
            #if file >=(filesize-5000000):
            #    raise Exception
        finally:
            pass
            #progress.destroy()
def copyfileobjr(fsrc, fdst, length,filesize):
    """copy data from file-like object fsrc to file-like object fdst"""
    global file
    progress=progressbar(filesize)
    
    while 1:
        try:
            buf = fsrc.read(length)
            if not buf:
                break
            
            fdst.write(buf)
            file=fdst.tell()
            progress["value"] = file
            progress.update()
            print(file)
        finally:
            pass
            #progress.destroy()
def progressbar(filesize):
    progress = ttk.Progressbar(RootWindow, orient="horizontal",length=300, mode="determinate")
    progress.pack()
    progress["value"] = 0
    maxbytes = filesize
    progress["maximum"] = filesize
    return progress
def Downloader():
    global file
    print("Commencing download")
    inputValue=link.get("1.0","end-1c")
    print(inputValue)
    x='bytes=0-'#getting wrong file size
    remaining_download_tries = 5
    #url="https://download.netbeans.org/netbeans/8.0.2/final/bundles/netbeans-8.0.2-javase-windows.exe"
    #https://www.codesector.com/files/teracopy.exe
    downloadname =str(inputValue.split('/')[-1])#gives proper filename
    downloadpath=Dpath+downloadname
    print(downloadpath)
    req = urllib.request.Request(inputValue, headers={'Range':x})
    response=urllib.request.urlopen(req)
    response.close()
    contentlength=int(response.getheader("Content-Length"))
    print(contentlength)

    try:
        print("starting download")
        with urllib.request.urlopen(req) as fsrc,open(downloadpath,'w+b')as fdst: #NamedTemporaryFile(delete=False) replace open () with Named..() for temp file download
            copyfileobj(fsrc,fdst,16*1024,contentlength)
            print("complete")
    except:
        #file=file+1
        
        fdst.close()
        while remaining_download_tries > 0:
            try:
                if file >= contentlength :
                    break
                remaining_download_tries=remaining_download_tries-1
                print("retrying download")
        
                x='bytes='+str(file)+'-'+str(contentlength)
                print(x)
                requ = urllib.request.Request(inputValue, headers={'Range':x})
                print("hello")
                with urllib.request.urlopen(requ) as fsrc,open(downloadpath,'a+b')as fdst: #NamedTemporaryFile(delete=False) replace open () with Named..() for temp file download
                    copyfileobjr(fsrc, fdst,16*1024,contentlength)
                    print("complete")
            except:
                fdst.close()
Dpath="C:/Users/KINDY kuttan/Desktop/"
file=0

RootWindow = tk.Tk() 
RootWindow.geometry("500x500")
RootWindow.resizable(0,0)

#background_image=tk.PhotoImage(file = "C:/Users/KINDY kuttan/Desktop/gy.gif")
#background_label = tk.Label(RootWindow, image=background_image)
#background_label.place(x=0, y=0, relwidth=1, relheight=1)

FrameLink = tk.Frame(master=RootWindow,bg='black')
FrameLink.pack_propagate(0) #Don't allow the widgets inside to determine the frame's width / height
FrameLink.pack(fill=tk.BOTH,padx=100,pady=100,ipady=30,ipadx=100) #Expand the frame to fill the root window

var = tk.StringVar()
LabelLink = tk.Label( FrameLink, textvariable=var )
var.set("Enter Download LINK")
LabelLink.pack()
#Changed variables so you don't have these set to None from .pack()

StartButton = tk.Button(master=RootWindow, text='Start Download', command=Downloader)
StartButton.pack()

link=tk.Text(master=FrameLink)
link.pack()
menu = tk.Menu(RootWindow) 
RootWindow.config(menu=menu) 
filemenu = tk.Menu(menu) 
menu.add_cascade(label='File', menu=filemenu) 
filemenu.add_command(label='New') 
text=filemenu.add_command(label='Download directory',command=directoryBox)
print(text)
filemenu.add_separator() 
filemenu.add_command(label='Exit', command=RootWindow.destroy) 
helpmenu = tk.Menu(menu) 
menu.add_cascade(label='Help', menu=helpmenu) 
helpmenu.add_command(label='About') 
RootWindow.title('Downloader') 
button = tk.Button(RootWindow, text='Stop', width=25, command=RootWindow.destroy) 
button.pack(side='bottom') 
RootWindow.mainloop() 
