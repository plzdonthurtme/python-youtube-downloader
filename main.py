import tkinter as tk
from tkinter import filedialog
import re
from check_youtube_url import is_valid_url
from tkinter import messagebox
from pytubefix import YouTube
import os
from moviepy import AudioFileClip

def select_folder():
    dir = filedialog.askdirectory()
    print(dir)
    folder_path.set(dir)
    url = url_entry.get()
    yt = YouTube(url)
    print(yt.streams.get_by_resolution())


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
        
        # print(yt.streams)
        if mp3_var.get():
            audio_stream = yt.streams.filter(only_audio=True).first()
            
            if audio_stream:
                out_file = audio_stream.download(output_path=save_path)
                base, ext = os.path.splitext(out_file)
                new_file = base + '.mp3'
                audio_clip = AudioFileClip(out_file)
                audio_clip.write_audiofile(new_file)
                audio_clip.close()
                os.remove(out_file)
                
        if mp4_var.get():
            video_stream = yt.streams.filter(progressive=True,file_extension='mp4').order_by('resolution').desc().first()
            
            if video_stream: 
                video_stream.download(save_path)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to download video: {e}")
    
root = tk.Tk()
root.title("Youtube Video Downloader")
folder_path = tk.StringVar()
mp3_var = tk.BooleanVar()
mp4_var = tk.BooleanVar()


#UI
url_label = tk.Label(root, text="Youtube URL:")
url_label.pack(padx=20)
url_entry = tk.Entry(root, width=50)
url_entry.pack(padx=20)
mp4_checkbox = tk.Checkbutton(root, text="Download MP4", variable=mp4_var)
mp4_checkbox.pack(padx=20)
mp3_checkbox = tk.Checkbutton(root, text="Download MP3", variable=mp3_var)
mp3_checkbox.pack(padx=20)
folder_label = tk.Button(root, text="Choose folder", command=select_folder)
folder_label.pack(padx=20, pady=10)
folder_entry = tk.Entry(root, textvariable=folder_path, width=50)
folder_entry.pack(padx=20)
download_button = tk.Button(root, text="Download",command=download_video)
download_button.pack(padx=20, pady=10)

#run app
root.mainloop()