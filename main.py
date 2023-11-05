#!/usr/bin/env python
from tkinter import *
from tkinter import ttk
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
from pathlib import Path
import musicplayer


root = Tk()
root.title("Music Player")
root.geometry("600x480")
root.maxsize(1400, 730)
root.config()


# Styles
style = ttk.Style()
style.configure("M.TButton", font="bold")


# Images
playimg = PhotoImage(file="images/play.png")
stopimg = PhotoImage(file="images/stop.png")
backimg = PhotoImage(file="images/back.png")
nextimg = PhotoImage(file="images/next.png")
addimg = PhotoImage(file="images/add.png")
sm_playimg = playimg.subsample(7,7)
sm_stopimg = stopimg.subsample(7,7)
sm_backimg = backimg.subsample(7,7)
sm_nextimg = nextimg.subsample(7,7)
sm_addimg = addimg.subsample(25,25)


# Album picture
image = PhotoImage(file="images/empty_album.png")
img = ttk.Label(root, image=image)
img.grid(column=1, row=1, rowspan=6, padx=5, pady=5, sticky="N")


# Music Library
addButton = ttk.Button(root, text="Add", image=sm_addimg, style="M.TButton",
                       command=root.destroy)
addButton.grid(column=0, row=0, padx=6, pady=5, sticky="SE")
musicFiles = Listbox(root, selectmode="single", width=20, height=10)
musicplayer.fetch_music_files(musicFiles)
musicFiles.grid(column=0, row=1, padx=5, pady=5, sticky="N")


# Music Title
def fetch_music_title(musicfiles):
    song = musicfiles.widget.curselection()
    index = musicfiles.widget.get(song[0])
    mp3file = Path(str(Path.cwd()) + f"/music/{index}")
    id3data = MP3(mp3file, ID3=EasyID3)
    title = f"\"{id3data['title'][0]}\" by {id3data['artist'][0]}"
    musicTitle = ttk.Label(root, text=title)
    musicTitle.grid(column=1, row=0)
    return

musicFiles.bind("<<ListboxSelect>>", fetch_music_title)


# Music controls
controlFrame = Frame(root, height=100)
controlFrame.grid(column=1, row=7)
backButton = ttk.Button(controlFrame, text="Previous",
                        image=sm_backimg, style="M.TButton",
                        command=root.destroy)
backButton.grid(column=0, row=0, padx=5)
playButton = ttk.Button(controlFrame, text="Play", image=sm_playimg,
                        style="M.TButton",
                        command=lambda:musicplayer.play_music(
                            musicFiles.get("active"), playButton))
playButton.grid(column=1, row=0, padx=5)
stopButton = ttk.Button(controlFrame, text="Stop", image=sm_stopimg,
                        style="M.TButton", command=root.destroy)
stopButton.grid(column=2, row=0, padx=5)
nextButton = ttk.Button(controlFrame, text="Next", image=sm_nextimg,
                        style="M.TButton", command=root.destroy)
nextButton.grid(column=3, row=0, padx=5)


# Run window
root.grid_columnconfigure(0, minsize=100)
root.mainloop()
