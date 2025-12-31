import tkinter as tk
from tkinter import filedialog, messagebox
from check_youtube_url import is_valid_url
from pytubefix import YouTube
import os
from moviepy import AudioFileClip
#movie editor outddated 


def select_folder():
    dir = filedialog.askdirectory()
    folder_path.set(dir)


def load_resolutions():
    url = url_entry.get()
    

    if not is_valid_url(url):
        messagebox.showerror("Error", "Invalid YouTube URL")
        return

    try:
        yt = YouTube(url)
        #didnt know youtube limit progressive streams. checking resolution
        # for s in yt.streams:
        #     print(s)
        streams = yt.streams.filter(progressive=True, file_extension='mp4')

        resolutions = sorted(
            {s.resolution for s in streams if s.resolution},
            key=lambda x: int(x.replace("p", ""))
        )

        menu = resolution_menu["menu"]
        menu.delete(0, "end")

        for res in resolutions:
            menu.add_command(
                label=res,
                command=lambda r=res: resolution_var.set(r)
            )

        if resolutions:
            resolution_var.set(resolutions[-1])  # default: highest available so will show 1 option

    except Exception as e:
        messagebox.showerror("Error", f"Failed to load resolutions: {e}")


def download_video():
    url = url_entry.get()
    save_path = folder_entry.get()

    if not save_path:
        messagebox.showerror("Error", "Please select a folder to save the video.")
        return

    if not is_valid_url(url):
        messagebox.showerror("Error", "Invalid YouTube URL")
        return

    try:
        yt = YouTube(url)
        

        if mp3_var.get():
            audio_stream = yt.streams.filter(only_audio=True).first()

            if audio_stream:
                out_file = audio_stream.download(output_path=save_path)
                base, ext = os.path.splitext(out_file)
                new_file = base + ".mp3"
                audio_clip = AudioFileClip(out_file)
                audio_clip.write_audiofile(new_file)
                audio_clip.close()
                os.remove(out_file)

    
        if mp4_var.get():
            selected_res = resolution_var.get()

            if selected_res == "Select resolution":
                messagebox.showerror("Error", "Please select an MP4 resolution")
                return

            video_stream = yt.streams.filter(progressive=True,file_extension="mp4", resolution=selected_res).first()

            if video_stream:
                video_stream.download(save_path)
            else:
                messagebox.showerror("Error", "Selected resolution not available")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to download video: {e}")


root = tk.Tk()
root.title("YouTube Video Downloader")

folder_path = tk.StringVar()
mp3_var = tk.BooleanVar()
mp4_var = tk.BooleanVar()
resolution_var = tk.StringVar(value="Select resolution")

tk.Label(root, text="YouTube URL:").pack(padx=20)
url_entry = tk.Entry(root, width=50)
url_entry.pack(padx=20)

tk.Checkbutton(root, text="Download MP4", variable=mp4_var).pack(padx=20)
tk.Checkbutton(root, text="Download MP3", variable=mp3_var).pack(padx=20)

tk.Label(root, text="MP4 Resolution:").pack(padx=20)
resolution_menu = tk.OptionMenu(root, resolution_var, ())
resolution_menu.pack(padx=20)


tk.Button(root, text="Load Resolutions", command=load_resolutions).pack(padx=20, pady=5)

tk.Button(root, text="Choose folder", command=select_folder).pack(padx=20, pady=10)
folder_entry = tk.Entry(root, textvariable=folder_path, width=50)
folder_entry.pack(padx=20)

tk.Button(root, text="Download", command=download_video).pack(padx=20, pady=10)

root.mainloop()
