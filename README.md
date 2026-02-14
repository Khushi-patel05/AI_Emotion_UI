# 🎀 AI Pastel Emotion Recognizer (Real-Time)

A Real-Time AI-Based Face Emotion Recognition System with a Pastel Aesthetic UI, Live Camera Feed, and Stable Emotion Detection using Computer Vision and Deep Learning.

This project detects facial emotions (Happy, Sad, Surprise, Neutral, etc.) in real-time using a webcam and displays them inside a modern pastel-themed graphical interface.

---

## ✨ Key Features

* 🎥 Real-time webcam emotion detection
* 🎀 Pastel aesthetic GUI (PyQt5 based)
* 🧠 AI-powered facial emotion recognition
* 🔲 AI Face Scanner Grid Overlay (Futuristic UI)
* 📸 Screenshot capture functionality
* 📊 Stable emotion smoothing (less flickering)
* 🛡️ Isolated virtual environment (safe setup)
* 💻 GitHub-ready clean project structure

---

## 🧠 Technologies Used

* Python 3.11
* OpenCV (Computer Vision & Camera Handling)
* FER (Facial Emotion Recognition - Deep Learning Model)
* PyQt5 (Aesthetic Graphical User Interface)
* NumPy (Numerical Processing)

---

## 📂 Project Structure

AI_Emotion_UI/
│
├── main.py                # Pastel UI & Application Controller
├── emotion_engine.py      # Emotion Detection + Face Grid Logic
├── requirements.txt       # Project Dependencies
├── README.md              # Project Documentation
├── .gitignore             # Ignored Files (venv, cache, etc.)
└── screenshots/           # Captured screenshots (optional)

---

## 🎯 Project Objective

The main objective of this project is to develop an industry-style AI application that:

* Detects facial emotions in real-time
* Provides a smooth and aesthetic user interface
* Demonstrates practical use of AI & Computer Vision
* Maintains stability and accuracy for live demonstrations

---

## 🚀 How to Run the Project (Step-by-Step)

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/Khushi-patel05/AI_Emotion_UI.git
cd AI_Emotion_UI
```

### 2️⃣ Create & Activate Virtual Environment

```bash
python -m venv venv
```

For Windows:

```bash
venv\Scripts\activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run the Application

```bash
python main.py
```

Then:

* Click **Start Camera 🎥**
* Show your face
* Emotion will be detected in real-time

---

## 🎥 How It Works (System Workflow)

Camera Feed → Face Detection → Face Cropping → Emotion Model (FER) → Stable Emotion Output → Aesthetic UI Display

This pipeline improves accuracy and reduces flickering in real-time emotion prediction.

---

## 🎨 User Interface Highlights

* Soft pastel color theme
* Clean modern layout
* Real-time camera inside GUI (not external window)
* Emotion label with confidence percentage
* Futuristic AI face grid overlay

---

## 📸 Screenshot Feature

The application includes a built-in screenshot button that:

* Captures the live emotion frame
* Saves images automatically in the `screenshots/` folder
* Useful for reports and project documentation

---

## ⚠️ Accuracy Notes (Important)

* Works best in good lighting conditions 💡
* Face should be clearly visible to the camera
* Extreme fast movements may reduce accuracy
* FER model may show Neutral for subtle expressions (common in real-time AI systems)

---

## 🔮 Future Enhancements

* Face Mesh Landmark Mapping
* Emotion Analytics Dashboard
* Multi-face Emotion Detection
* Voice Feedback System
* Cloud Deployment (Web App)
* Emotion History Graph

---

## 🎓 Academic Relevance

This project is suitable for:

* AI & ML Mini Projects
* Computer Vision Lab Projects
* UI + AI Integrated Projects
* Portfolio & Resume Projects
* College Demonstrations & Viva

---

## 👩‍💻 Author

Developed by an AI & ML Engineering Student
Real-Time AI Emotion Recognition with Aesthetic Pastel UI

---

## ⭐ If you like this project

Give it a ⭐ on GitHub and use it for learning, research, and academic demonstrations!
