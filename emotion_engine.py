import cv2
from fer import FER
from collections import deque


class EmotionEngine:
    def __init__(self):
        self.detector = FER()
        self.cap = None

        # Buffer for stable emotion (last 15 frames)
        self.emotion_buffer = deque(maxlen=15)

    def start_camera(self):
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 720)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    def stop_camera(self):
        if self.cap is not None:
            self.cap.release()
            self.cap = None

    def draw_ai_grid(self, frame, x, y, w, h):
        box_color = (255, 182, 193)
        grid_color = (200, 170, 255)

        cv2.rectangle(frame, (x, y), (x + w, y + h), box_color, 2)

        # Vertical grid
        for i in range(1, 4):
            vx = x + int(w * i / 4)
            cv2.line(frame, (vx, y), (vx, y + h), grid_color, 1)

        # Horizontal grid
        for i in range(1, 4):
            hy = y + int(h * i / 4)
            cv2.line(frame, (x, hy), (x + w, hy), grid_color, 1)

    def get_stable_emotion(self):
        if not self.emotion_buffer:
            return "Detecting..."
        return max(set(self.emotion_buffer), key=self.emotion_buffer.count)

    def preprocess_face(self, face_img):
        """
        Enhance face for better emotion accuracy
        """
        # Resize face to standard size (VERY IMPORTANT for FER)
        face_img = cv2.resize(face_img, (224, 224))

        # Improve brightness & contrast
        face_img = cv2.convertScaleAbs(face_img, alpha=1.2, beta=15)

        return face_img

    def get_frame(self):
        if self.cap is None:
            return None, "Camera not started"

        ret, frame = self.cap.read()
        if not ret:
            return None, "Camera Error"

        frame = cv2.flip(frame, 1)

        # Detect faces + emotions
        results = self.detector.detect_emotions(frame)

        if results:
            # Take the biggest face (main user)
            face = max(results, key=lambda x: x["box"][2] * x["box"][3])
            (x, y, w, h) = face["box"]

            # Ensure coordinates are valid
            x, y = max(0, x), max(0, y)
            face_crop = frame[y:y + h, x:x + w]

            if face_crop.size > 0:
                # 🔥 CRITICAL: Preprocess cropped face
                processed_face = self.preprocess_face(face_crop)

                # Re-run emotion detection ONLY on face (major accuracy boost)
                refined_result = self.detector.detect_emotions(processed_face)

                if refined_result:
                    emotions = refined_result[0]["emotions"]
                    top_emotion = max(emotions, key=emotions.get)
                    confidence = emotions[top_emotion]

                    # Ignore weak predictions (reduces neutral bias)
                    if confidence > 0.35:
                        self.emotion_buffer.append(top_emotion)

                    stable_emotion = self.get_stable_emotion()
                    emotion_text = f"{stable_emotion.capitalize()} ({confidence*100:.1f}%)"
                else:
                    emotion_text = "Analyzing..."

            else:
                emotion_text = "Face Error"

            # Draw aesthetic grid
            self.draw_ai_grid(frame, x, y, w, h)

            return frame, emotion_text

        return frame, "No Face Detected"
