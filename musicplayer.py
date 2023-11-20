#!/usr/bin/env python
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
from mutagen import File
from pathlib import Path
from pydub import AudioSegment
from pydub.playback import play
from subprocess import check_output
from subprocess import CalledProcessError
from shutil import copy2
from PIL import Image, ImageTk
import multiprocessing
import time
import os
import queue
import signal


# Global vars
playing = False


# Create a queue
mq = multiprocessing.Queue()
proc = None
after_id = None


# Create root window
root = Tk()
root.title("Music Player")
root.geometry("600x480")
root.maxsize(1400, 730)
root.config()


# Functionality
def add():
    fextensions = ["*.mp3", "*.wav"]
    ftypes = [("audio files", fextensions)]
    filename = filedialog.askopenfilename(title="Select file",
                                          filetypes=ftypes)
    if filename:
        filepath = Path(filename)
        musicpath = Path(str(Path.cwd()) + "/music")
        index = musicFiles.size() - 1
        song = filename.split("/")[-1]
        copy2(filepath, musicpath)
        musicFiles.insert(index + 1, song)
    else:
        pass
    return


def album_art():
    file = musicFiles.get("active")
    filepath = Path(str(Path.cwd()) + f"/music/{file}")
    artpath = "images/image.png"
    musicfile = File(filepath)
    artwork = musicfile.tags["APIC:"].data
    with open(artpath, "wb") as img:
        img.write(artwork)
    albumart = Path(str(Path.cwd()) + f"/{artpath}")
    return albumart


def back(event):
    try:
        stop_music()
    except CalledProcessError:
        pass
    finally:
        index = musicFiles.curselection()[0] - 1
        if index >= 0:
            song = musicFiles.get(index)
        elif index < 0:
            song = musicFiles.get("active")
        play_callback(song)
        fetch_music_title(song)
    return


def fetch_music_files():
    musicPath = Path(str(Path.cwd()) + "/music")
    index = 1
    for file in musicPath.glob('*'):
        song = str(file).split("/")[-1]
        musicFiles.insert(index, song)
        index += 1
    return


def fetch_music_title(musicfiles):
    if musicfiles == str(musicfiles):
        filename = musicfiles
    else:
        song = musicfiles.widget.curselection()
        filename = musicfiles.widget.get(song[0])
    mp3file = Path(str(Path.cwd()) + f"/music/{filename}")
    id3data = MP3(mp3file, ID3=EasyID3)
    title = f"\"{id3data['title'][0]}\" by {id3data['artist'][0]}"
    musicTitle = ttk.Label(root, text=title)
    musicTitle.grid(column=1, row=0)
    return


def forward():
    try:
        stop_music()
        index = musicFiles.curselection()[0] + 1
        if index <= (musicFiles.size() - 1):
            song = musicFiles.get(index)
        elif index > (musicFiles.size() - 1):
            song = musicFiles.get("active")
    except CalledProcessError:
        pass
    finally:
        play_callback(song)
        fetch_music_title(song)
    return


def play_callback(songname):
    # Create new thread for playing music
    global artwork, proc
    try:
        progress()
    except CalledProcessError:
        pass
    except AttributeError:
        pass
    finally:
        artwork = ImageTk.PhotoImage(Image.open(album_art()).resize((320,320)))
        albumart.config(image=artwork)
        proc = multiprocessing.Process(target=play_music, args=(songname,))
        proc.start()
    return


def play_music(songname):
    global mq
    song = AudioSegment.from_mp3("music/" + songname)
    mq.put(play(song))
    mq.put(progress())
    return


def stop_music():
    global proc, after_id
    if after_id:
        progbar.stop()
        root.after_cancel(after_id)
    proc.terminate()
    proc.join()
    childProc = check_output(["pidof", "ffplay"])
    childPid = int(childProc.decode().strip("\n"))
    os.kill(childPid, signal.SIGTERM)
    return


def replay_callback(event):
    replay()
    return


def replay():
    try:
        stop_music()
    except TypeError:
        pass
    finally:
        play_callback(musicFiles.get("active"))
    return


def progress():
    global after_id
    audio = AudioSegment.from_file("music/" + musicFiles.get("active"))
    songlength = int(len(audio) / 1000)
    if progbar["value"] != 100:
        progbar.step((1/songlength) * 100)
    after_id = root.after(5, progress)
    return


# Styles
style = ttk.Style()
style.configure("M.TButton", font="bold")


# Images
playimg = PhotoImage(file="images/play.png")
stopimg = PhotoImage(file="images/stop.png")
backimg = PhotoImage(file="images/back.png")
nextimg = PhotoImage(file="images/next.png")
addimg = PhotoImage(file="images/add.png")
sm_playimg = playimg.subsample(20, 20)
sm_stopimg = stopimg.subsample(20, 20)
sm_backimg = backimg.subsample(20, 20)
sm_nextimg = nextimg.subsample(20, 20)
sm_addimg = addimg.subsample(20, 20)


# Album picture
artwork = None
emptyalb = ImageTk.PhotoImage(Image.open("images/disc.png").resize((320,320)))
albumart = ttk.Label(root, image=emptyalb)
albumart.grid(column=1, row=1, rowspan=6, padx=5, pady=5, sticky="N")


# Progress Bar
progbar = ttk.Progressbar(root, orient="horizontal", mode="determinate", length=320)
progbar.grid(column=1, row=7, padx=5)


# Music Library
addButton = ttk.Button(root, text="Add", image=sm_addimg, command=add)
addButton.grid(column=0, row=0, padx=6, pady=5, sticky="SE")
musicFiles = Listbox(root, selectmode="single", width=20, height=10)
musicFiles.grid(column=0, row=1, padx=5, pady=5, sticky="N")
## Fetch music files
fetch_music_files()


# Music Title
musicFiles.bind("<<ListboxSelect>>", fetch_music_title)


# Music controls
controlFrame = Frame(root, height=100)
controlFrame.grid(column=1, row=8, pady=5)
backButton = ttk.Button(controlFrame, text="Previous",
                        image=sm_backimg)
backButton.grid(column=0, row=0, padx=5)
backButton.bind('<Button-1>', replay_callback)
backButton.bind('<Double-Button-1>', back)
playButton = ttk.Button(controlFrame, text="Play", image=sm_playimg,
                        style="M.TButton",
                        command=lambda: play_callback(musicFiles.get("active")))
playButton.grid(column=1, row=0, padx=5)
stopButton = ttk.Button(controlFrame, text="Stop", image=sm_stopimg,
                        style="M.TButton", command=stop_music)
stopButton.grid(column=2, row=0, padx=5)
nextButton = ttk.Button(controlFrame, text="Next", image=sm_nextimg,
                        style="M.TButton", command=forward)
nextButton.grid(column=3, row=0, padx=5)


if __name__ == "__main__":
    # Run window
    root.grid_columnconfigure(0, minsize=100)
    root.mainloop()
