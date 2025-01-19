import tkinter as tk
from tkinter import filedialog
from gtts import gTTS
import PyPDF2
from threading import Thread
from tkinter import messagebox
from PIL import Image, ImageTk
import time
import pyttsx3

# --- Function to Extract Text from All Pages ---
def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as book:
        pdf_reader = PyPDF2.PdfReader(book)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text


# --- Function to Generate and Save Speech ---
def save_speech_as_audio(text, output_audio_file):
    if text.strip():  # Ensure there is text to convert
        print("Converting text to speech... This might take a while for a long PDF.")
        
        # Initialize pyttsx3 engine
        engine = pyttsx3.init()

        # Set properties for speech (optional)
        engine.setProperty('rate', 150)  # Speed of speech
        engine.setProperty('volume', 1)  # Volume (0.0 to 1.0)

        # Saving the speech to an audio file
        engine.save_to_file(text, output_audio_file)
        engine.runAndWait()
        print(f"Audio content written to {output_audio_file}")
    else:
        print("No text found to convert to speech.")


# --- Function to Handle File Selection ---
def select_pdf():
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if file_path:
        pdf_path_var.set(file_path)


# --- Function to Process PDF and Convert to Speech ---
def process_pdf():
    # Disable the "Select PDF" and "Convert" buttons while processing
    select_button.config(state=tk.DISABLED)
    convert_button.config(state=tk.DISABLED)

    # Show loading text instead of GIF
    loading_label.grid(row=3, column=0, pady=10)

    # Extract text from the selected PDF
    pdf_path = pdf_path_var.get()
    if not pdf_path:
        messagebox.showerror("Error", "Please select a PDF file.")
        return

    output_audio_file = "full_pdf_audio.mp3"
    
    # Extract text and save audio in a separate thread to avoid freezing the GUI
    def conversion_task():
        print("Extracting text from PDF...")
        text = extract_text_from_pdf(pdf_path)
        print("Converting text to speech...")
        save_speech_as_audio(text, output_audio_file)
        print(f"Audio saved to {output_audio_file}")
        
        # Update the GUI after processing is done
        loading_label.grid_forget()  # Hide loading text
        download_button.grid(row=4, column=0, pady=10)  # Show download button
        select_button.config(state=tk.NORMAL)  # Re-enable Select PDF button
        convert_button.config(state=tk.NORMAL)  # Re-enable Convert button

    # Start the conversion in a separate thread
    thread = Thread(target=conversion_task)
    thread.start()


# --- Function to Download the Generated Audio ---
def download_audio():
    # This simply opens the folder where the audio is saved
    print("Downloading audio...")
    messagebox.showinfo("Download", "Your audio is ready! The MP3 file is saved as 'full_pdf_audio.mp3'.")
    # If you want to open the directory where the file is saved:
    import os
    os.startfile(os.path.dirname(os.path.abspath("full_pdf_audio.mp3")))


# --- Setup GUI Window ---
root = tk.Tk()
root.title("TTS - PDF to Audio")
root.geometry("500x350")
root.config(bg="#f4f4f4")

# --- Add a Title Label ---
title_label = tk.Label(root, text="TTS - PDF to Audio", font=("Helvetica", 18, "bold"), bg="#f4f4f4")
title_label.grid(row=0, column=0, columnspan=2, pady=20)

# --- PDF Path Entry ---
pdf_path_var = tk.StringVar()

label = tk.Label(root, text="Select a PDF file to convert to speech:", bg="#f4f4f4", font=("Helvetica", 12))
label.grid(row=1, column=0, pady=10)

entry = tk.Entry(root, textvariable=pdf_path_var, width=40, font=("Helvetica", 12))
entry.grid(row=2, column=0, pady=5)

select_button = tk.Button(root, text="Browse", command=select_pdf, font=("Helvetica", 12), bg="#4CAF50", fg="white", relief="raised", padx=10)
select_button.grid(row=2, column=1, padx=10)

# --- Convert Button ---
convert_button = tk.Button(root, text="Convert to Audio", command=process_pdf, font=("Helvetica", 12), bg="#2196F3", fg="white", relief="raised", padx=10)
convert_button.grid(row=3, column=0, columnspan=2, pady=20)

loading_label = tk.Label(root, text="Processing... Please wait.", bg="#f4f4f4", font=("Helvetica", 12))
loading_label.grid_forget()  # Initially hidden

# --- Download Button ---
download_button = tk.Button(root, text="Download Audio", command=download_audio, font=("Helvetica", 12), bg="#FF5722", fg="white", relief="raised", padx=10)
download_button.grid(row=4, column=0, pady=10)
download_button.grid_forget()  # Initially hidden

root.mainloop()
