# AI-Assisted Smart Glasses (On-Device OCR & Audio Assist)

Smart AI Glass is a compact, on-device vision system that performs optical character recognition (OCR) and audio feedback on a Raspberry Pi Zero W.  
The project runs fully offline and is designed for low-power, low-memory embedded hardware.

Interaction is handled using a single capacitive touch sensor, allowing intuitive control without the need for a display or keyboard.

---

## Features

- On-device OCR using a lightweight deep learning model
- Offline text-to-speech output
- Touch-based control:
  - Hold touch sensor → capture and read text
  - Tap touch sensor → pause / resume OCR
- Event-driven processing (no continuous polling)
- Optimized for Raspberry Pi Zero W
- Audio output via Bluetooth earbuds or wired speaker

---

## Hardware

- Raspberry Pi Zero W  
- Raspberry Pi Camera Module  
- Capacitive touch sensor  
- Bluetooth earbuds or wired audio output  

---

## Software Stack

- Python 3  
- EasyOCR (CPU-only, quantized)  
- OpenCV (headless)  
- pyttsx3  
- picamera2  
- RPi.GPIO  

---

## Running the Project

Refer to **SETUP.md** for installation and Bluetooth configuration.

```bash
python3 smart_ai_glass.py
