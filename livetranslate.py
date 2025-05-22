import sys
import os
from datetime import datetime
from dotenv import load_dotenv
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout,
    QComboBox, QSpinBox, QPushButton, QDialog, QSlider, QMessageBox
)
import azure.cognitiveservices.speech as speechsdk

# Language Mappings
SPEAKER_LANG_CODES = {
    "English (India)": "en-IN",
    "Hindi": "hi-IN",
    "Marathi": "mr-IN",
    "Gujarati": "gu-IN",
    "Bengali": "bn-IN",
    "Tamil": "ta-IN",
    "Telugu": "te-IN",
}

INDIAN_LANG_CODES = {
    "Hindi": "hi",
    "Marathi": "mr",
    "Gujarati": "gu",
    "Bengali": "bn",
    "Tamil": "ta",
    "Telugu": "te",
    "English": "en"
}


class LanguageSelectionDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Overlay Settings")
        layout = QVBoxLayout(self)

        self.source_lang_selector = QComboBox()
        self.source_lang_selector.addItems(SPEAKER_LANG_CODES.keys())
        layout.addWidget(QLabel("Speaker's Language:"))
        layout.addWidget(self.source_lang_selector)

        self.target_lang_selector = QComboBox()
        self.target_lang_selector.addItems(INDIAN_LANG_CODES.keys())
        layout.addWidget(QLabel("Translate to:"))
        layout.addWidget(self.target_lang_selector)

        self.font_size_selector = QSpinBox()
        self.font_size_selector.setRange(10, 72)
        self.font_size_selector.setValue(28)
        layout.addWidget(QLabel("Font Size:"))
        layout.addWidget(self.font_size_selector)

        self.font_color_selector = QComboBox()
        self.font_color_selector.addItems(["Red", "White", "Yellow", "Green", "Blue"])
        self.font_color_selector.setCurrentText("Red")
        layout.addWidget(QLabel("Font Color:"))
        layout.addWidget(self.font_color_selector)

        self.opacity_slider = QSlider(Qt.Horizontal)
        self.opacity_slider.setRange(0, 100)
        self.opacity_slider.setValue(0)  # Default: fully transparent
        layout.addWidget(QLabel("Background Opacity (%):"))
        layout.addWidget(self.opacity_slider)

        self.ok_button = QPushButton("Start")
        self.ok_button.clicked.connect(self.accept)
        layout.addWidget(self.ok_button)

    def get_selections(self):
        source = SPEAKER_LANG_CODES[self.source_lang_selector.currentText()]
        target = INDIAN_LANG_CODES[self.target_lang_selector.currentText()]
        font_size = self.font_size_selector.value()
        font_color = self.font_color_selector.currentText().lower()
        opacity_percent = self.opacity_slider.value()
        return source, target, font_size, font_color, opacity_percent


class InstantOverlay(QWidget):
    def __init__(self, source_lang_code, target_lang_code, font_size, font_color, bg_opacity_percent):
        super().__init__()
        self.source_lang_code = source_lang_code
        self.target_lang_code = target_lang_code

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("background: transparent;")

        screen_geometry = QApplication.primaryScreen().geometry()
        self.setGeometry(0, screen_geometry.height() - 150, screen_geometry.width(), 100)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)

        # Convert opacity % to 0–1 alpha value
        alpha = bg_opacity_percent / 100.0
        rgba_style = f"rgba(0, 0, 0, {alpha:.2f})"

        self.label = QLabel("", self)
        self.label.setStyleSheet(f"color: {font_color}; background-color: {rgba_style};")
        self.label.setFont(QFont("Arial", font_size))
        layout.addWidget(self.label)

        self.installEventFilter(self)
        self.start_translation()

    def update_text(self, new_text):
        screen_width = self.width()
        char_width = self.label.fontMetrics().averageCharWidth()
        max_chars = max(10, screen_width // char_width)
        if len(new_text) > max_chars:
            new_text = new_text[-max_chars:]

        self.label.setText(new_text)
        log_file = f"{datetime.now().date()}_{self.target_lang_code}.txt"
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"{datetime.now().strftime('%H:%M:%S')} → {new_text}\n")

    def eventFilter(self, source, event):
        if event.type() == event.KeyPress and event.key() == Qt.Key_Escape:
            if hasattr(self, "recognizer"):
                self.recognizer.stop_continuous_recognition()
            self.close()
            return True
        return super().eventFilter(source, event)

    def closeEvent(self, event):
        if hasattr(self, "recognizer"):
            self.recognizer.stop_continuous_recognition()
        event.accept()

    def start_translation(self):
        load_dotenv()
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
        source, target, font_size, font_color, opacity = dialog.get_selections()
        overlay = InstantOverlay(source, target, font_size, font_color, opacity)
        overlay.show()
    sys.exit(app.exec_())
