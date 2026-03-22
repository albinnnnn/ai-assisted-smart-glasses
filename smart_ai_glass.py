import time
import cv2
import pytesseract
import pyttsx3
import RPi.GPIO as GPIO
from picamera2 import Picamera2
import subprocess

# ==========================
# CONFIGURATION
# ==========================
TOUCH_PIN             = 17
OCR_MIN_CHARS         = 3      
BT_DEVICE_MAC         = None   


TESS_CONFIG = "--psm 6 --oem 1"

# ==========================
# BLUETOOTH 
# ==========================
def connect_bluetooth():
    if not BT_DEVICE_MAC:
        return
    try:
        subprocess.run(
            ["bluetoothctl", "connect", BT_DEVICE_MAC],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True,
        )
        time.sleep(2)
    except subprocess.CalledProcessError:
        pass

# ==========================
# GPIO SETUP
# ==========================
GPIO.setmode(GPIO.BCM)
GPIO.setup(TOUCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# ==========================
# CAMERA SETUP
# ==========================
camera = Picamera2()
camera.configure(
    camera.create_still_configuration(
        main={"size": (640, 480)}
    )
)
camera.start()
time.sleep(1)  # warm-up

# ==========================
# TTS SETUP
# ==========================
connect_bluetooth()
engine = pyttsx3.init()
engine.setProperty("rate", 145)

# ==========================
# STATE
# ==========================
ocr_active      = True
last_touch_state = False

# ==========================
# IMAGE PREPROCESSING
# ==========================
def preprocess(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Resize to 480x360 — enough resolution for Tesseract, faster to process
    gray = cv2.resize(gray, (480, 360))

    # Adaptive threshold — binarizes the image locally, handles shadows well
    binary = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        blockSize=21,   # neighbourhood size — increase for larger text
        C=10,           # constant subtracted from mean
    )

    return binary

# ==========================
# OCR
# ==========================
def run_ocr(img) -> str:
    
    raw = pytesseract.image_to_string(img, config=TESS_CONFIG)

    # Clean up: strip whitespace, remove single stray characters
    lines = [
        line.strip()
        for line in raw.splitlines()
        if len(line.strip()) >= OCR_MIN_CHARS
    ]
    return " ".join(lines)

# ==========================
# SPEECH
# ==========================
def speak(text: str):
    if not text.strip():
        return
    engine.say(text)
    engine.runAndWait()

# ==========================
# MAIN LOOP
# ==========================
print("Smart AI Glass running")
print("Tap touch sensor  → Pause / Resume")
print("Hold touch sensor → Capture and read text")

try:
    while True:
        touch_state = GPIO.input(TOUCH_PIN)

        # Tap: toggle OCR active/paused
        if touch_state and not last_touch_state:
            ocr_active = not ocr_active
            speak("paused" if not ocr_active else "resumed")
            time.sleep(0.3)  # debounce

        last_touch_state = touch_state

        # Held: capture → OCR → speak
        if ocr_active and touch_state:
            frame  = camera.capture_array()
            img    = preprocess(frame)
            text   = run_ocr(img)

            if text:
                speak(text)
            else:
                speak("no text found")

            time.sleep(1)  # cooldown before next capture

        time.sleep(0.05)

except KeyboardInterrupt:
    print("Exiting...")
finally:
    camera.stop()
    GPIO.cleanup()