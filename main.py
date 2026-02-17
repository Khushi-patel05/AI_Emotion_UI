import sys
import cv2
from PyQt5.QtWidgets import (
    QApplication, QLabel, QPushButton, QVBoxLayout,
    QHBoxLayout, QWidget, QProgressBar, QFrame
)
from PyQt5.QtGui import QImage, QPixmap, QFont
from PyQt5.QtCore import QTimer, Qt
from emotion_engine import EmotionEngine


class EmotionApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🤖 AI Emotion Scanner - Futuristic UI")
        self.setGeometry(100, 100, 1100, 750)

        # 🧠 Emotion Engine (Your existing FER backend)
        self.engine = EmotionEngine()

        # ⏱ Timer for live camera feed
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

        # 📸 Store last frame & emotion (for freeze feature)
        self.last_frame = None
        self.last_emotion = "No Data"

        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)

        # 🤖 Title
        self.title_label = QLabel("AI EMOTION ANALYSIS SYSTEM")
        self.title_label.setFont(QFont("Segoe UI", 24, QFont.Bold))
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("color: #d6b3ff; letter-spacing: 2px;")

        # 🎥 Futuristic Camera Frame
        self.video_label = QLabel("Camera Feed Will Appear Here")
        self.video_label.setFixedSize(760, 500)
        self.video_label.setAlignment(Qt.AlignCenter)
        self.video_label.setStyleSheet("""
            QLabel {
                border-radius: 25px;
                border: 3px solid #9d7bff;
                background-color: rgba(20, 20, 40, 200);
                color: #ccccff;
                font-size: 18px;
            }
        """)

        # 🧠 Emotion Display
        self.emotion_label = QLabel("Emotion: Waiting for Scan...")
        self.emotion_label.setFont(QFont("Segoe UI", 20, QFont.Bold))
        self.emotion_label.setAlignment(Qt.AlignCenter)
        self.emotion_label.setStyleSheet("color: #ffffff;")

        # 📊 Confidence Progress Bar (Futuristic)
        self.confidence_bar = QProgressBar()
        self.confidence_bar.setValue(0)
        self.confidence_bar.setFixedHeight(28)
        self.confidence_bar.setStyleSheet("""
            QProgressBar {
                border-radius: 14px;
                background-color: rgba(40, 40, 80, 180);
                color: white;
                font-weight: bold;
                text-align: center;
                border: 2px solid #9d7bff;
            }
            QProgressBar::chunk {
                border-radius: 14px;
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #c8a2ff,
                    stop:1 #7b5cff
                );
            }
        """)

        # 🧾 Glassmorphism Status Panel
        self.status_card = QFrame()
        self.status_card.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.08);
                border-radius: 20px;
                border: 1px solid rgba(200, 162, 255, 0.5);
            }
        """)

        status_layout = QVBoxLayout()

        self.status_label = QLabel("● AI Status: Idle 🟡")
        self.model_label = QLabel("● Model: FER Neural Engine")
        self.camera_label = QLabel("● Camera: Offline")

        for lbl in [self.status_label, self.model_label, self.camera_label]:
            lbl.setFont(QFont("Segoe UI", 13, QFont.Bold))
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setStyleSheet("color: #e6ccff;")

        status_layout.addWidget(self.status_label)
        status_layout.addWidget(self.model_label)
        status_layout.addWidget(self.camera_label)
        self.status_card.setLayout(status_layout)

        # 🎮 Futuristic Buttons
        button_layout = QHBoxLayout()

        self.start_button = QPushButton("▶ START AI SCAN")
        self.stop_button = QPushButton("■ STOP SCAN")

        for btn in [self.start_button, self.stop_button]:
            btn.setFixedHeight(50)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #7b5cff;
                    border-radius: 15px;
                    color: white;
                    font-size: 16px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #9d7bff;
                }
            """)

        self.start_button.clicked.connect(self.start_camera)
        self.stop_button.clicked.connect(self.stop_camera)

        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)

        # 🎨 Futuristic Gradient Background
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 #0f0c29,
                    stop:0.5 #1a1a40,
                    stop:1 #2a0845
                );
            }
        """)

        # Layout Assembly
        main_layout.addWidget(self.title_label)
        main_layout.addWidget(self.video_label, alignment=Qt.AlignCenter)
        main_layout.addWidget(self.emotion_label)
        main_layout.addWidget(self.confidence_bar)
        main_layout.addWidget(self.status_card)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def start_camera(self):
        self.engine.start_camera()
        self.timer.start(30)
        self.status_label.setText("● AI Status: Scanning 🟢")
        self.camera_label.setText("● Camera: Active")

    def stop_camera(self):
        self.timer.stop()
        self.engine.stop_camera()

        # 📸 Freeze last frame instead of black screen
        if self.last_frame is not None:
            frame = self.last_frame
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            qt_image = QImage(rgb_image.data, w, h, ch * w, QImage.Format_RGB888)
            self.video_label.setPixmap(QPixmap.fromImage(qt_image))

            # 🧠 Show final emotion snapshot
            self.emotion_label.setText(f"Final Emotion Snapshot: {self.last_emotion}")
            self.status_label.setText("● AI Status: Scan Complete 📸")
            self.camera_label.setText("● Camera: Stopped (Snapshot Frozen)")
        else:
            self.video_label.setText("No Snapshot Available")
            self.status_label.setText("● AI Status: Stopped 🔴")
            self.camera_label.setText("● Camera: Offline")

    def update_frame(self):
        frame, emotion_text = self.engine.get_frame()

        if frame is not None:
            # 📸 Store last frame & emotion continuously
            self.last_frame = frame.copy()
            self.last_emotion = emotion_text

            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            qt_image = QImage(rgb_image.data, w, h, ch * w, QImage.Format_RGB888)
            self.video_label.setPixmap(QPixmap.fromImage(qt_image))

            self.emotion_label.setText(f"Detected Emotion: {emotion_text}")

            # 📊 Update confidence bar
            if "(" in emotion_text:
                try:
                    confidence = float(emotion_text.split("(")[1].replace("%)", ""))
                    self.confidence_bar.setValue(int(confidence))
                except:
                    self.confidence_bar.setValue(0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EmotionApp()
    window.show()
    sys.exit(app.exec_())
