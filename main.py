import os
from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
import tkinter.messagebox
from PIL import Image, ImageTk
from pygame import mixer
import random


class SimpleMusicPlayer:
    def __init__(self, tkinter_app):
        self.tkinter_app = tkinter_app
        self.tkinter_app.geometry("420x640")
        self.tkinter_app.config(bg="darkgreen")
        self.tkinter_app.title("Simple Music Player")
        self.paused = False
        self.chosen_songs_paths = []
        self.current_song_index = 0

        mixer.init()

        img = ImageTk.PhotoImage(Image.open("notes1.jpg").resize((400, 170)))
        panel = Label(self.tkinter_app, image=img)
        panel.grid(row=0, column=0, sticky=W+E+N+S, padx=8, pady=5)

        self.upper_frame = Frame(self.tkinter_app, width=420, height=180)
        self.upper_frame.grid(row=1, column=0, padx=5, pady=5)

        self.label = Label(self.upper_frame, width=44, text='Choose songs to play', font=('Arial', 12), anchor="w")
        self.label.grid(row=0, columnspan=5)

        play_button = Button(self.upper_frame, text='Play', width=12, command=self.select_song)
        play_button.grid(row=2, column=0)

        pause_button = Button(self.upper_frame, text='Pause/Resume', width=12, command=self.pause_resume)
        pause_button.grid(row=2, column=1)

        next_button = Button(self.upper_frame, text='Next', width=12, command=self.select_next_song)
        next_button.grid(row=2, column=2)

        previous_button = Button(self.upper_frame, text='Previous', width=12, command=self.select_previous_song)
        previous_button.grid(row=2, column=3)

        random_button = Button(self.upper_frame, text='Random', width=12, command=self.select_random_song)
        random_button.grid(row=2, column=4)

        self.song_listbox = Listbox(self.tkinter_app, width=68, height=22, selectmode="browse")
        self.song_listbox.grid(row=3, column=0)

        clear_button = Button(self.tkinter_app, text='Clear playlist', width=20, command=self.clear_playlist)
        clear_button.grid(row=4, column=0)

        app_menu = Menu(self.tkinter_app)
        submenu = Menu(app_menu, tearoff=0)
        submenu.add_command(label="Browse files", command=self.add_songs_listbox)
        submenu.add_separator()
        submenu.add_command(label="Close App", command=self.tkinter_app.destroy)

        app_menu.add_cascade(label="Menu", menu=submenu)
        self.tkinter_app.config(menu=app_menu)

        self.tkinter_app.mainloop()

    def clear_playlist(self):
        self.song_listbox.delete(0, END)

    def update_text(self):
        # update label describing current song playing
        song_name = os.path.basename(self.chosen_songs_paths[self.current_song_index])
        self.label.configure(text=song_name)

    def add_songs_listbox(self):
        chosen_songs = filedialog.askopenfilenames()
        for song in chosen_songs:
            if song not in self.chosen_songs_paths:
                self.chosen_songs_paths.append(song)
            song_name = os.path.basename(song)
            listbox_current_list = self.song_listbox.get(0, self.song_listbox.size())
            if song_name not in listbox_current_list:
                self.song_listbox.insert(END, song_name)

    def select_song(self):
        # Select song using cursor or play first in listbox if none selected
        try:
            self.current_song_index = self.song_listbox.curselection()[0]
        except IndexError:
            pass
        self.play()

    def select_next_song(self):
        if not self.current_song_index == (len(self.chosen_songs_paths) - 1):
            self.current_song_index += 1
            self.play()

    def select_previous_song(self):
        if not self.current_song_index == 0:
            self.current_song_index -= 1
            self.play()

    def select_random_song(self):
        self.current_song_index = random.choice([index for index in range(0, len(self.chosen_songs_paths))])
        print(self.current_song_index)
        self.play()

    def play(self):
        mixer.stop()
        try:
            chosen_song = self.chosen_songs_paths[self.current_song_index]
            mixer.music.load(chosen_song)
            mixer.music.play()
            self.update_text()
        except FileNotFoundError:
            tkinter.messagebox.showerror('File not found', 'Could not find selected file.')
        except IndexError:
            tkinter.messagebox.showerror('No files selected', 'Browse songs to play, go Menu > Select files')

    def pause_resume(self):
        if not self.paused:
            mixer.music.pause()
            self.paused = True
        elif self.paused:
            mixer.music.unpause()
            self.paused = False


if __name__ == '__main__':
    root = Tk()
    app = SimpleMusicPlayer(root)
