from tkinter import *  # importing this for making a window
from datetime import datetime # importing this to see total program running time
from pygame import mixer # importing this for playing music and controlling them
import tkinter.messagebox
from tkinter import filedialog
from ttkthemes import themed_tk as tk
from tkinter import ttk
from mutagen.mp3 import MP3
import os
import threading
import time
start_time=datetime.now()

root=tk.ThemedTk()
root.get_themes()
root.set_theme("breeze")

menubar= Menu(root)
root.config(menu=menubar)

status_bar= ttk.Label(root,text='Welcome to Tune !!', relief=SUNKEN, anchor=W, font='ComicSansMS 11')
status_bar.pack(side=BOTTOM, fill=X)

playlist=[]

def browse_file():
    global filename_path
    filename_path=filedialog.askopenfilename()
    add_to_playlist(filename_path)

def add_to_playlist(filename):
    filename=os.path.basename(filename)
    index=0;
    playlistbox.insert(index,filename)
    playlist.insert(index,filename_path)
    index+=1

subMenu=Menu(menubar, tearoff=0)
menubar.add_cascade(label='File', menu=subMenu)
subMenu.add_command(label='Open', command=browse_file)
subMenu.add_command(label='Exit', command=root.destroy)

def song_info():
    tkinter.messagebox.showinfo("About Song",os.path.basename(filename_path))


subMenu=Menu(menubar, tearoff=0)
menubar.add_cascade(label='View', menu=subMenu)
subMenu.add_command(label='About Song', command=song_info)

def about_me():
    tkinter.messagebox.showinfo('About Me','This software was created by Satvik Tata.')

def how_to_use():
    tkinter.messagebox.showinfo('How to use',' Click on "ADD" -- to add the song\n Select the Song\n Click on "Play Button" -- to play the song\n Click on "Pause Button" -- to pause the song\n Click on "Stop Button" -- to stop the song\n Click on "Revind Button" -- to revind the song\n Click on "DEL" -- to delete the song\n')
subMenu=Menu(menubar, tearoff=0)
menubar.add_cascade(label='Help', menu=subMenu)
subMenu.add_command(label='About Me',command= about_me)
subMenu.add_command(label='How To Use',command= how_to_use)

mixer.init() # initializing the mixer

root.title('Tune')
root.iconbitmap(r'images/tune.ico')

leftframe=Frame(root)
leftframe.pack(side=LEFT, padx=15, pady=30)

playlistbox=Listbox(leftframe)
playlistbox.pack()

addbtn=ttk.Button(leftframe, text='+ Add', command=browse_file)
addbtn.pack(side=LEFT,padx=3)

def del_song():
    selected_song=playlistbox.curselection()
    selected_song=int(selected_song[0])
    playlistbox.delete(selected_song)
    playlist.pop(selected_song)

delbtn=ttk.Button(leftframe,text='- Del', command=del_song)
delbtn.pack(side=LEFT,padx=3)

rightframe=Frame(root)
rightframe.pack(padx=15,pady=30)

topframe=Frame(rightframe)
topframe.pack()

lengthlabel= ttk.Label(topframe,text='Total Length:  --:--', relief=GROOVE, font='ComicSansMS 11 bold')
lengthlabel.pack(pady=5)

currenttimelabel= ttk.Label(topframe,text='Current time:  --:--', relief=GROOVE, font='ComicSansMS 11 bold')
currenttimelabel.pack(pady=3)

def show_details(play_song):
    file_data= os.path.splitext(play_song)
    if file_data[1]=='.mp3':
        audio=MP3(play_song)
        total_length=audio.info.length
    else:
        a=mixer.Sound(play_song)
        total_length=a.get_length()
    mins, secs=divmod(total_length,60)
    mins=round(mins)
    secs=round(secs)
    timeformat='{:02d}:{:02d}'.format(mins,secs)
    lengthlabel['text']='Total Length '+' - ' + timeformat
    t1=threading.Thread(target=start_count,args=(total_length,))
    t1.start()

def start_count(t):
    global paused
    current_time=0;
    while current_time<=t and mixer.music.get_busy():
        if paused:
            continue
        else:
            mins, secs=divmod(current_time,60)
            mins=round(mins)
            secs=round(secs)
            timeformat='{:02d}:{:02d}'.format(mins,secs)
            currenttimelabel['text']='Current Time: '+' - ' + timeformat
            time.sleep(1)
            current_time+=1

def play_music():
    global paused
    if paused:
        mixer.music.unpause()
        status_bar['text']='Music Resumed'+' '+os.path.basename(filename_path)
        paused=False
    else:
        try:
            stop_music()
            time.sleep(1)
            selected_song=playlistbox.curselection()
            selected_song=int(selected_song[0])
            play_it=playlist[selected_song]
            mixer.music.load(play_it)
            mixer.music.play()
            status_bar['text']='Playing Music'+' '+os.path.basename(play_it)
            show_details(play_it)
        except:
            tkinter.messagebox.showerror('Error !!','Please select a music file first !!')

def stop_music():
    mixer.music.stop()
    status_bar['text']='Music Stopped'

paused=False

def pause_music():
    global paused
    paused=True
    mixer.music.pause()
    status_bar['text']='Music Paused'

def rewind_music():
    play_music()
    status_bar['text']='Music Restarted'

def set_vol(val):
    global volume
    volume = float(val)/100
    mixer.music.set_volume(volume)

muted=False

def mute_music():
    global muted
    if muted:
        mixer.music.set_volume(0.07)
        volumeBtn.configure(image=volume_photo)
        scale.set(7)
        muted=False
    else:
        mixer.music.set_volume(0)
        volumeBtn.configure(image=mute_photo)
        scale.set(0)
        muted=True

middleframe= Frame(rightframe)
middleframe.pack(padx=15, pady=15)

play_photo= PhotoImage(file='images/play_btn.png')
playBtn=ttk.Button(middleframe, image=play_photo, command= play_music)
playBtn.grid(row=0, column=0, padx=7)

stop_photo= PhotoImage(file='images/stop_btn.png')
stopBtn=ttk.Button(middleframe, image=stop_photo, command=stop_music)
stopBtn.grid(row=0, column=1, padx=7)

pause_photo= PhotoImage(file='images/pause_btn.png')
pauseBtn=ttk.Button(middleframe, image=pause_photo, command=pause_music)
pauseBtn.grid(row=0, column=2, padx=7)

bottomframe= Frame(rightframe)
bottomframe.pack(padx=10,pady=15)

rewind_photo= PhotoImage(file='images/rewind_btn.png')
rewindBtn=ttk.Button(bottomframe, image=rewind_photo, command=rewind_music)
rewindBtn.grid(row=0, column=0, padx=13, pady=5)

mute_photo= PhotoImage(file='images/mute_btn.png')
volume_photo= PhotoImage(file='images/volume_btn.png')
volumeBtn=ttk.Button(bottomframe, image=volume_photo, command=mute_music)
volumeBtn.grid(row=0, column=1, padx=13, pady=5)

scale=ttk.Scale(bottomframe, from_=0,to=100, orient=HORIZONTAL, command= set_vol)
scale.set(7)
mixer.music.set_volume(.07)
scale.grid(row=0, column=2,pady=15)

def on_closing():
    stop_music()
    root.destroy()

root.protocol("WM_DELETE_WINDOW",on_closing)
root.mainloop()

end_time=datetime.now()
print (end_time-start_time)