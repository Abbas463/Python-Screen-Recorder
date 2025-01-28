from tkinter import *
import pyscreenrec
import os
import pyaudio
import wave
import threading
import moviepy.editor as mp

# Create the main window
win = Tk()
win.geometry("400x600")
win.title("Abbas Screen Recorder")
win.config(bg="#fff")
win.resizable(False, False)

# Initialize ScreenRecorder
rec = pyscreenrec.ScreenRecorder()

# Initialize PyAudio for microphone access
p = pyaudio.PyAudio()

# Define global variables for microphone recording status
recording_active = False
mic_stream = None
audio_filename = None
video_filename = None
final_filename = None

# Functions for recording
def start_rec():
    global recording_active, mic_stream, audio_filename, video_filename, final_filename
    file = Filename.get().strip()
    if not file:
        file = "Recording"
    video_filename = os.path.join("C:/Users/SHC/Desktop/Project/screen recorder", f"{file}.mp4")
    audio_filename = os.path.join("C:/Users/SHC/Desktop/Project/screen recorder", f"{file}_audio.wav")
    final_filename = os.path.join("C:/Users/SHC/Desktop/Project/screen recorder", f"{file}_final.mp4")
    
    try:
        fps = 30  # Specify the frames per second
        print(f"Starting screen recording: {video_filename} at {fps} FPS")
        rec.start_recording(video_filename, fps)
        
        # Start microphone recording in a separate thread
        recording_active = True
        mic_thread = threading.Thread(target=start_mic_recording, args=(audio_filename,))
        mic_thread.daemon = True  # Ensure it ends with the program
        mic_thread.start()

    except Exception as e:
        print(f"Error starting recording: {e}")

def pause_rec():
    global recording_active
    try:
        print("Pausing recording...")
        rec.pause_recording()
        # Pause microphone recording as well
        stop_mic_recording()
        recording_active = False
    except Exception as e:
        print(f"Error pausing recording: {e}")

def resume_rec():
    global recording_active
    try:
        print("Resuming recording...")
        rec.resume_recording()
        # Resume microphone recording as well
        recording_active = True
        resume_mic_recording()
    except Exception as e:
        print(f"Error resuming recording: {e}")

def stop_rec():
    global recording_active, audio_filename, video_filename, final_filename
    try:
        print("Stopping screen recording...")
        rec.stop_recording()
        # Stop microphone recording as well
        stop_mic_recording()
        recording_active = False
        
        # Combine video and audio into one file
        combine_audio_video(video_filename, audio_filename, final_filename)

    except Exception as e:
        print(f"Error stopping recording: {e}")

# Microphone recording functions
def start_mic_recording(filename):
    global mic_stream
    mic_stream = p.open(format=pyaudio.paInt16,
                       channels=1,
                       rate=44100,
                       input=True,
                       frames_per_buffer=1024)
    frames = []
    print("Starting microphone recording...")

    while recording_active:
        data = mic_stream.read(1024)
        frames.append(data)

    save_mic_audio(filename, frames)
    print("Microphone recording saved.")

def save_mic_audio(filename, frames):
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(44100)
        wf.writeframes(b''.join(frames))

def stop_mic_recording():
    global mic_stream
    global recording_active
    if mic_stream:
        recording_active = False
        mic_stream.stop_stream()
        mic_stream.close()
        mic_stream = None
        print("Microphone recording stopped.")

def resume_mic_recording():
    global recording_active
    recording_active = True
    mic_filename = "C:/Users/SHC/Desktop/Project/screen recorder/audio.wav"
    mic_thread = threading.Thread(target=start_mic_recording, args=(mic_filename,))
    mic_thread.daemon = True
    mic_thread.start()

def combine_audio_video(video_path, audio_path, final_path):
    try:
        # Load video and audio
        video = mp.VideoFileClip(video_path)
        audio = mp.AudioFileClip(audio_path)

        # Resize video to HD (1920x1080) for better quality
        video = video.resize((1920, 1080))

        # Set the audio to the video clip
        video = video.set_audio(audio)

        # Write the final result with improved quality settings
        video.write_videofile(final_path, codec="libx264", audio_codec="aac", bitrate="5000k", threads=4, fps=30, preset="slow")

        # Clean up the audio and video files to avoid unnecessary extra files
        if os.path.exists(audio_path):
            os.remove(audio_path)
        if os.path.exists(video_path):
            os.remove(video_path)

        print(f"Final video saved: {final_path}")
    except Exception as e:
        print(f"Error combining video and audio: {e}")

# Load images safely
def load_image(path):
    try:
        return PhotoImage(file=path)
    except Exception as e:
        print(f"Error loading image {path}: {e}")
        return None

# Set up the app icon
image_icon = load_image("C:/Users/SHC/Desktop/Project/screen recorder/icon.png")
if image_icon:
    win.iconphoto(False, image_icon)

# Add UI elements
image1 = load_image("C:/Users/SHC/Desktop/Project/screen recorder/yelllow.png")
if image1:
    Label(win, image=image1, bg="#fff").place(x=-2, y=35)

image2 = load_image("C:/Users/SHC/Desktop/Project/screen recorder/blue.png")
if image2:
    Label(win, image=image2, bg="#fff").place(x=223, y=200)

lb1 = Label(win, text="Abbas Screen Recorder", bg="#fff", font="arial 15 bold")
lb1.pack(pady=20)

image3 = load_image("C:/Users/SHC/Desktop/Project/screen recorder/recording.png")
if image3:
    Label(win, image=image3, bd=0).pack(pady=30)

# Input field for file name
Filename = StringVar()
entry = Entry(win, textvariable=Filename, font="arial 15")
entry.place(x=100, y=350)
Filename.set("Recording")

# Buttons
start = Button(win, text="Start", font="arial 22", bd=0, command=start_rec)
start.place(x=140, y=250)

image4 = load_image("C:/Users/SHC/Desktop/Project/screen recorder/pause.png")
if image4:
    pause = Button(win, image=image4, bd=0, bg="#fff", command=pause_rec)
    pause.place(x=50, y=450)

image5 = load_image("C:/Users/SHC/Desktop/Project/screen recorder/resume.png")
if image5:
    resume = Button(win, image=image5, bd=0, bg="#fff", command=resume_rec)
    resume.place(x=150, y=450)

image6 = load_image("C:/Users/SHC/Desktop/Project/screen recorder/stop.png")
if image6:
    stop = Button(win, image=image6, bd=0, bg="#fff", command=stop_rec)
    stop.place(x=250, y=450)

# Automatically stop recording when closing the window
def on_close():
    try:
        stop_rec()
    except Exception:
        pass
    win.destroy()

win.protocol("WM_DELETE_WINDOW", on_close)

# Run the app
win.mainloop()