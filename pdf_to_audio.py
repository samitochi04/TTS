from gtts import gTTS
import PyPDF2


# --- Function to Extract Text from All Pages ---
def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as book:
        pdf_reader = PyPDF2.PdfReader(book)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text


# --- Function to Generate and Save Speech ---
def save_speech_as_audio(text, output_audio_file, lang='en'):
    if text.strip():  # Ensure there is text to convert
        print("Converting text to speech... This might take a while for a long PDF.")
        tts = gTTS(text=text, lang=lang, slow=False)
        tts.save(output_audio_file)
        print(f"Audio content written to {output_audio_file}")
    else:
        print("No text found to convert to speech.")


# --- Main Script ---
if __name__ == "__main__":
    # PDF file path
    pdf_path = "models-attract-women-through-honesty.pdf"

    # Output audio file path
    output_audio_file = "full_pdf_audio.mp3"

    # Extract text from the entire PDF
    print("Extracting text from PDF...")
    text = extract_text_from_pdf(pdf_path)

    # Save the text as speech in an audio file
    save_speech_as_audio(text, output_audio_file)
