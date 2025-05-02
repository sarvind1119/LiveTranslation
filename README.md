# Speech Translation Overlay (Live Subtitles App)

This is a lightweight PyQt5 application that captures live speech through your microphone, translates it in real-time using Azure Cognitive Services, and displays the translated text as an overlay on your screen — perfect for multilingual classrooms, live sessions, and accessibility use cases.

---

## ✨ Features

- 🎙️ Real-time speech recognition
- 🌐 Instant translation to any official Indian language
- 🎞️ Live overlay subtitle display
- 🎛️ User-selectable:
  - Speaker's language
  - Translation language
  - Font size
- 📁 Auto-save translations to a dated `.txt` file
- ⌨️ Press `Esc` to exit the overlay quickly

---

## 🛠️ Prerequisites

- Python 3.7+
- Azure Speech resource (with a valid **SPEECH_KEY** and **SPEECH_REGION**)

---

## 📦 Installation

1. **Clone this repository:**

   ```bash
   git clone https://github.com/sarvind1119/speech-translation-overlay.git
   cd speech-translation-overlay
   ```

2. **Create a virtual environment and install dependencies:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Create your `.env` file:**

   In the root directory, create a `.env` file and paste:

   ```env
   SPEECH_KEY=your_azure_speech_key
   SPEECH_REGION=your_azure_region
   ```

---

## 🚀 Usage

To launch the app:

```bash
python overlay_final_fixed.py
```

- A dialog window will appear asking you to select:
  - The speaker's language (input)
  - The language you want translation in (output)
  - The font size for subtitles
- Once selected, an overlay will appear and display translated text in real-time.

---

## 📝 Output

All translations are saved in a text file named by the current date (e.g., `2025-05-02.txt`) in the same directory.

---

## 📌 Example Use Cases

- 🏫 Multilingual classrooms
- 🏛️ Government training at institutions like LBSNAA
- 🧏 Accessibility enhancement for public speaking or live sessions
- 🌐 Real-time translation for cross-language meetings

---

## 🙋‍♂️ Shortcuts

- Press `Esc` to exit the overlay window

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 🙌 Acknowledgements

- [Azure Cognitive Services – Speech](https://azure.microsoft.com/en-us/products/cognitive-services/speech-services/)
- [PyQt5](https://pypi.org/project/PyQt5/)