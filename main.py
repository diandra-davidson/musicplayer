from tkinter import *
from tkinter import ttk
import musicplayer

root = Tk()
root.title("Music Player")
root.geometry("600x420")
root.maxsize(1400, 730)
root.config()

# Styles
style = ttk.Style()
style.configure("M.TButton", font="bold")

# Music Title
musicTitle = ttk.Label(root, text="Music Title")
musicTitle.grid(column=1, row=0)

# Album picture
image = PhotoImage(file="images/empty_album.png")
img = ttk.Label(root, image=image)
img.grid(column=1, row=1, rowspan=6, padx=5, pady=5)

# Images
playimg = PhotoImage(file="images/play.png")
stopimg = PhotoImage(file="images/stop.png")
backimg = PhotoImage(file="images/back.png")
nextimg = PhotoImage(file="images/next.png")
sm_playimg = playimg.subsample(7,7)
sm_stopimg = stopimg.subsample(7,7)
sm_backimg = backimg.subsample(7,7)
sm_nextimg = nextimg.subsample(7,7)

# Music controls
controlFrame = Frame(root, height=100)
controlFrame.grid(column=1, row=7)
backButton = ttk.Button(controlFrame, text="Previous", image=sm_backimg, style="M.TButton",
                        command=root.destroy)
backButton.grid(column=0, row=0, padx=5)
playButton = ttk.Button(controlFrame, text="Play", image=sm_playimg, style="M.TButton",
                        command=root.destroy)
playButton.grid(column=1, row=0, padx=5)
stopButton = ttk.Button(controlFrame, text="Stop", image=sm_stopimg, style="M.TButton",
                        command=root.destroy)
stopButton.grid(column=2, row=0, padx=5)
nextButton = ttk.Button(controlFrame, text="Next", image=sm_nextimg, style="M.TButton",
                        command=root.destroy)
nextButton.grid(column=3, row=0, padx=5)

# Run window
root.grid_columnconfigure(0, minsize=100)
root.mainloop()
