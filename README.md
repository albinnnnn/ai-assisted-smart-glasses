# AI-Assisted Smart Glasses — On-Device OCR & Audio Assist

Smart AI Glass is a compact, fully offline vision system that performs optical character recognition (OCR) and audio feedback on a Raspberry Pi Zero W.  
It is designed for low-power, low-memory embedded hardware with no internet connection required.

Interaction is handled using a single capacitive touch sensor, allowing intuitive control without a display or keyboard.

---

## Features

- On-device OCR using Tesseract — a lightweight C++ engine with no neural network overhead
- Offline text-to-speech output via pyttsx3
- Touch-based control:
  - **Hold** touch sensor → capture image and read text aloud
  - **Tap** touch sensor → pause / resume
- Adaptive image preprocessing for real-world lighting conditions
- Optimised for Raspberry Pi Zero W (single-core, 512 MB RAM)
- Audio output via Bluetooth earbuds or wired speaker

---

## Hardware

| Component | Details |
|-----------|---------|
| Raspberry Pi Zero W | Single-core 1GHz, 512MB RAM |
| Raspberry Pi Camera Module | CSI interface |
| Capacitive touch sensor | GPIO 17, active HIGH |
| Audio output | Bluetooth earbuds or 3.5mm jack |

---

## Software Stack

| Component | Library |
|-----------|---------|
| OCR engine | Tesseract 4+ (C++ binary via `pytesseract`) |
| Image processing | OpenCV (headless) |
| Text-to-speech | pyttsx3 + espeak |
| Camera | picamera2 |
| GPIO | RPi.GPIO |

> **Note:** EasyOCR was evaluated and rejected for this hardware.  
> It uses PyTorch under the hood and takes 4–8 seconds per inference on Pi Zero W.  
> Tesseract achieves the same task in 300–800 ms with no model loading overhead.

---

## Performance (Pi Zero W)

| Stage | Time |
|-------|------|
| Camera capture | 200–400 ms |
| Preprocessing | 50–80 ms |
| Tesseract OCR | 300–800 ms |
| TTS + playback | 1–4 s |
| **Total capture → speech** | **~2–6 s** |

---

## Project Structure

```
smart-ai-glass/
├── smart_ai_glass.py   main application
└── README.md           this file
```

---

## Installation & Running

```bash
# System dependencies
sudo apt install -y tesseract-ocr python3-picamera2 python3-opencv espeak

# Python dependencies
pip3 install pytesseract pyttsx3 RPi.GPIO

# Run
python3 smart_ai_glass.py
```

---

## Completed Project

This project is part of a broader embedded AI portfolio including:

- **HelmetGuard** — YOLOv11s helmet detection with Streamlit UI
- **TomatoScan** — YOLOv8s + MobileNetV3-Large tomato disease classifier
- **Edge RFID Attendance** — ESP32/ESP8266 MQTT attendance system