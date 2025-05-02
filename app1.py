import sys
import os
from datetime import datetime
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QComboBox, QVBoxLayout, QHBoxLayout, QSpinBox, QPushButton, QDialog
from dotenv import load_dotenv
import azure.cognitiveservices.speech as speechsdk

load_dotenv()

INDIAN_LANG_CODES = {
    "Hindi": "hi",
    "Bengali": "bn",
    "Telugu": "te",
    "Marathi": "mr",
    "Tamil": "ta",
    "Urdu": "ur",
    "Gujarati": "gu",
    "Kannada": "kn",
    "Odia": "or",
    "Punjabi": "pa",
    "Malayalam": "ml",
    "Assamese": "as",
    "Manipuri": "mni",
    "Sanskrit": "sa",
    "Konkani": "kok",
    "Kashmiri": "ks",
    "Sindhi": "sd",
    "Nepali": "ne",
    "Bodo": "brx",
    "Dogri": "doi",
    "Santali": "sat",
    "Maithili": "mai"
}

SPEAKER_LANG_CODES = {
    "English": "en-US",
    "Hindi": "hi-IN",
    "Punjabi": "pa-IN",
    "Tamil": "ta-IN",
    "Telugu": "te-IN"
}

class LanguageSelectionDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Select Languages")
        self.setStyleSheet("background-color: white; color: black;")
        layout = QVBoxLayout(self)

        self.source_lang_selector = QComboBox(self)
        self.source_lang_selector.addItems(SPEAKER_LANG_CODES.keys())
        layout.addWidget(QLabel("Speaker's Language:"))
        layout.addWidget(self.source_lang_selector)

        self.target_lang_selector = QComboBox(self)
        self.target_lang_selector.addItems(list(INDIAN_LANG_CODES.keys()) + ["English"])
        layout.addWidget(QLabel("Translation Required in:"))
        layout.addWidget(self.target_lang_selector)

        self.font_size_selector = QSpinBox(self)
        self.font_size_selector.setRange(10, 72)
        self.font_size_selector.setValue(24)
        layout.addWidget(QLabel("Font Size:"))
        layout.addWidget(self.font_size_selector)

        self.ok_button = QPushButton("Start Translation")
        self.ok_button.clicked.connect(self.accept)
        layout.addWidget(self.ok_button)

    def get_selections(self):
        selected_target = self.target_lang_selector.currentText()
        target_code = INDIAN_LANG_CODES.get(selected_target, "en")
        return (
            SPEAKER_LANG_CODES[self.source_lang_selector.currentText()],
            target_code,
            self.font_size_selector.value()
        )

from PyQt5.QtGui import QKeyEvent

class InstantOverlay(QWidget):
    def __init__(self, source_lang_code, target_lang_code, font_size):
        super().__init__()
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setStyleSheet("background-color: black; color: white;")
        self.source_lang_code = source_lang_code
        self.target_lang_code = target_lang_code

        screen_geometry = QApplication.primaryScreen().geometry()
        self.setGeometry(0, screen_geometry.height() - 150, screen_geometry.width(), 100)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)

        self.label = QLabel("", self)
        self.label.setStyleSheet("color: white; background: transparent;")
        self.label.setFont(QFont("Arial", font_size))
        layout.addWidget(self.label)

        self.start_translation()
        self.installEventFilter(self)

    def update_text(self, new_text):
        # Limit text length to fit screen width heuristically
        screen_width = self.width()
        char_width = self.label.fontMetrics().averageCharWidth()
        max_chars = max(10, screen_width // char_width)  # avoid too small values
        if len(new_text) > max_chars:
            new_text = new_text[-max_chars:]

        self.label.setText(new_text)
        filename = f"{datetime.now().date()}.txt"
        with open(filename, "a", encoding="utf-8") as f:
            f.write(new_text + "\n")

    def eventFilter(self, source, event):
        if event.type() == event.KeyPress:
            if event.key() == Qt.Key_Escape:
                self.close()
                return True
        return super().eventFilter(source, event)

    def start_translation(self):
        speech_key = os.getenv("SPEECH_KEY")
        region = os.getenv("SPEECH_REGION")
        if not speech_key or not region:
            print("❌ Missing Azure credentials in .env")
            return

        config = speechsdk.translation.SpeechTranslationConfig(
            subscription=speech_key,
            region=region
        )
        config.speech_recognition_language = self.source_lang_code
        config.add_target_language(self.target_lang_code)

        audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)

        recognizer = speechsdk.translation.TranslationRecognizer(
            translation_config=config,
            audio_config=audio_config
        )

        def on_partial_result(evt):
            translated = evt.result.translations.get(self.target_lang_code)
            if translated:
                self.update_text(translated)

        def on_result(evt):
            if evt.result.reason == speechsdk.ResultReason.TranslatedSpeech:
                translated = evt.result.translations.get(self.target_lang_code)
                if translated:
                    self.update_text(translated)

        recognizer.recognizing.connect(on_partial_result)
        recognizer.recognized.connect(on_result)
        recognizer.session_started.connect(lambda evt: print("🔵 Session started"))
        recognizer.canceled.connect(lambda evt: print("🔴 Canceled:", evt.reason, evt.error_details))
        recognizer.session_stopped.connect(lambda evt: print("🟠 Session stopped"))

        recognizer.start_continuous_recognition()
        self.recognizer = recognizer

if __name__ == "__main__":
    app = QApplication(sys.argv)

    dialog = LanguageSelectionDialog()
    if dialog.exec_() == QDialog.Accepted:
        source_lang, target_lang, font_size = dialog.get_selections()
        overlay = InstantOverlay(source_lang, target_lang, font_size)
        overlay.show()

    sys.exit(app.exec_())
