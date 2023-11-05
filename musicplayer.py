#!/usr/bin/env python
from pathlib import Path
from tkinter import *
from tkinter import ttk
from pydub import AudioSegment
from pydub.playback import play


def fetch_music_files(musicbox):
    musicPath = Path(str(Path.cwd()) + "/music")
    index = 1
    for file in musicPath.glob('*'):
        song = str(file).split("/")[-1]
        musicbox.insert(index, song)
        index += 1
    return


def play_music(song, button):
    pauseimg = PhotoImage(file="images/pause.png")
    sm_pauseimg = pauseimg.subsample(7, 7)
    button.config(image=sm_pauseimg)
    song = AudioSegment.from_mp3("music/" + song)
    play(song)
    return
