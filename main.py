import tkinter as tk
from tkinter import filedialog

def select_folder():
    dir = filedialog.askdirectory()
    print(dir)
    folder_path.set(dir)

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
download_button = tk.Button(root, text="Download")
download_button.pack(padx=20, pady=10)

#run app
root.mainloop()