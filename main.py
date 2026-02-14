import sys
import cv2
import os
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QHBoxLayout
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer, Qt
from emotion_engine import EmotionEngine


class EmotionApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("AI Pastel Emotion Recognizer 💖")
        self.setGeometry(200, 100, 900, 700)

        # Create screenshots folder safely
        if not os.path.exists("screenshots"):
            os.makedirs("screenshots")

        self.current_frame = None
        self.engine = EmotionEngine()

        # 🌸 Pastel UI Styling
        self.setStyleSheet("""
            QWidget {
                background-color: #FFF6FB;
                font-family: Segoe UI;
            }
            QLabel#title {
                color: #6D5B8C;
                font-size: 28px;
                font-weight: bold;
            }
            QLabel#emotion {
                color: #7A6C9D;
                font-size: 22px;
                font-weight: bold;
                background-color: #FDE2F3;
                border-radius: 15px;
                padding: 12px;
            }
            QPushButton {
                background-color: #E0BBE4;
                border-radius: 18px;
                padding: 12px;
                font-size: 16px;
                font-weight: bold;
                color: #4B3F72;
            }
            QPushButton:hover {
                background-color: #D291BC;
            }
        """)

        # Title
        self.title_label = QLabel("🎀 AI Face Emotion Recognizer")
        self.title_label.setObjectName("title")
        self.title_label.setAlignment(Qt.AlignCenter)

        # Camera Display
        self.camera_label = QLabel("Camera Feed Will Appear Here 📷")
        self.camera_label.setAlignment(Qt.AlignCenter)
        self.camera_label.setStyleSheet("""
            background-color: #FFE4EC;
            border-radius: 25px;
            padding: 10px;
        """)

        # Emotion Label
        self.emotion_label = QLabel("Detected Emotion: Waiting...")
        self.emotion_label.setObjectName("emotion")
        self.emotion_label.setAlignment(Qt.AlignCenter)

        # Buttons
        self.start_button = QPushButton("Start Camera 🎥")
        self.stop_button = QPushButton("Stop Camera ⛔")
        self.capture_button = QPushButton("Capture Screenshot 📸")

        self.start_button.clicked.connect(self.start_camera)
        self.stop_button.clicked.connect(self.stop_camera)
        self.capture_button.clicked.connect(self.capture_screenshot)

        # Button Layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        button_layout.addWidget(self.capture_button)

        # Main Layout
        layout = QVBoxLayout()
        layout.addWidget(self.title_label)
        layout.addWidget(self.camera_label)
        layout.addWidget(self.emotion_label)
        layout.addLayout(button_layout)

        self.setLayout(layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

    def start_camera(self):
        self.engine.start_camera()
        self.timer.start(30)

    def stop_camera(self):
        self.timer.stop()
        self.engine.stop_camera()
        self.camera_label.setText("Camera Stopped ⛔")

    def capture_screenshot(self):
        if self.current_frame is not None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshots/emotion_{timestamp}.png"
            cv2.imwrite(filename, self.current_frame)

    def update_frame(self):
        frame, emotion = self.engine.get_frame()

        if frame is not None:
            self.current_frame = frame.copy()
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_frame.shape
            bytes_per_line = ch * w
            qt_image = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qt_image)
            self.camera_label.setPixmap(pixmap)

        self.emotion_label.setText(f"Detected Emotion: {emotion}")

    def closeEvent(self, event):
        self.engine.stop_camera()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EmotionApp()
    window.show()
    sys.exit(app.exec_())